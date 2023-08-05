"""Datapipe and utils to load PV data from NetCDF for training"""
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

import fsspec
import numpy as np
import pandas as pd
import xarray as xr
from torchdata.datapipes import functional_datapipe
from torchdata.datapipes.iter import IterDataPipe

from ocf_datapipes.load.pv.utils import (
    intersection_of_pv_system_ids,
    put_pv_data_into_an_xr_dataarray,
)
from ocf_datapipes.utils.geospatial import lat_lon_to_osgb

_log = logging.getLogger(__name__)


@functional_datapipe("open_pv_netcdf")
class OpenPVFromNetCDFIterDataPipe(IterDataPipe):
    """Datapipe to load NetCDF"""

    def __init__(
        self,
        pv_power_filename: Union[str, Path],
        pv_metadata_filename: Union[str, Path],
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
    ):
        """
        Datapipe to load PV from NetCDF

        Args:
            pv_power_filename: Filename of the power file
            pv_metadata_filename: Filename of the metadata file
            start_datetime: start datetime that the dataset is limited to
            end_datetime: end datetime that the dataset is limited to
        """
        super().__init__()
        self.pv_power_filename = pv_power_filename
        self.pv_metadata_filename = pv_metadata_filename
        self.start_dateime = start_datetime
        self.end_datetime = end_datetime

    def __iter__(self):
        data: xr.DataArray = load_everything_into_ram(
            self.pv_power_filename,
            self.pv_metadata_filename,
            start_dateime=self.start_dateime,
            end_datetime=self.end_datetime,
        )
        while True:
            yield data


def load_everything_into_ram(
    pv_power_filename,
    pv_metadata_filename,
    start_dateime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
) -> xr.DataArray:
    """Open AND load PV data into RAM."""

    # load metadata
    pv_metadata = _load_pv_metadata(pv_metadata_filename)

    # Load pd.DataFrame of power and pd.Series of capacities:
    (
        pv_power_watts,
        pv_capacity_watt_power,
        pv_system_row_number,
    ) = _load_pv_power_watts_and_capacity_watt_power(
        pv_power_filename, start_date=start_dateime, end_date=end_datetime,
    )
    # Ensure pv_metadata, pv_power_watts, and pv_capacity_watt_power all have the same set of
    # PV system IDs, in the same order:
    pv_metadata, pv_power_watts = intersection_of_pv_system_ids(pv_metadata, pv_power_watts)
    pv_capacity_watt_power = pv_capacity_watt_power.loc[pv_power_watts.columns]
    pv_system_row_number = pv_system_row_number.loc[pv_power_watts.columns]

    data_in_ram = put_pv_data_into_an_xr_dataarray(
        pv_power_watts=pv_power_watts,
        y_osgb=pv_metadata.y_osgb.astype(np.float32),
        x_osgb=pv_metadata.x_osgb.astype(np.float32),
        capacity_watt_power=pv_capacity_watt_power,
        pv_system_row_number=pv_system_row_number,
    )

    # Sanity checks:
    time_utc = pd.DatetimeIndex(data_in_ram.time_utc)
    assert time_utc.is_monotonic_increasing
    assert time_utc.is_unique

    return data_in_ram


def _load_pv_power_watts_and_capacity_watt_power(
    filename: Union[str, Path],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Return pv_power_watts, pv_capacity_watt_power, pv_system_row_number.

    The capacities and pv_system_row_number are computed across the *entire* dataset,
    and so is independent of the `start_date` and `end_date`. This ensures the PV system
    row number and capacities stay constant across training and validation.
    """

    _log.info(f"Loading solar PV power data from {filename} from {start_date=} to {end_date=}.")

    # Load data in a way that will work in the cloud and locally:
    if ".parquet" in str(filename):
        _log.debug(f"Loading PV parquet file {filename}")
        pv_power_df = pd.read_parquet(filename, engine="fastparquet")
        _log.debug("Loading PV parquet file: done")
        pv_power_df["generation_w"] = pv_power_df["generation_wh"] * 12
        if end_date is not None:
            pv_power_df = pv_power_df[pv_power_df["timestamp"] < end_date]
        if start_date is not None:
            pv_power_df = pv_power_df[pv_power_df["timestamp"] >= start_date]

        # pivot on ss_id
        _log.debug("Pivoting PV data")
        pv_power_watts = pv_power_df.pivot(
            index="timestamp", columns="ss_id", values="generation_w"
        )
        _log.debug("Pivoting PV data: done")
        pv_capacity_watt_power = pv_power_watts.max().astype(np.float32)

    else:
        with fsspec.open(filename, mode="rb") as file:
            pv_power_ds = xr.open_dataset(file, engine="h5netcdf")
            pv_capacity_watt_power = pv_power_ds.max().to_pandas().astype(np.float32)
            pv_power_watts = pv_power_ds.sel(datetime=slice(start_date, end_date)).to_dataframe()
            pv_power_watts = pv_power_watts.astype(np.float32)

            del pv_power_ds

        if "passiv" not in str(filename):
            _log.warning("Converting timezone. ARE YOU SURE THAT'S WHAT YOU WANT TO DO?")
            try:
                pv_power_watts = (
                    pv_power_watts.tz_localize("Europe/London").tz_convert("UTC").tz_convert(None)
                )
            except Exception as e:
                _log.warning(
                    "Could not convert timezone from London to UTC. "
                    "Going to try and carry on anyway"
                )
                _log.warning(e)

    pv_capacity_watt_power.index = [np.int32(col) for col in pv_capacity_watt_power.index]
    pv_power_watts.columns = pv_power_watts.columns.astype(np.int64)

    # Create pv_system_row_number. We use the index of
    # `pv_capacity_watt_power` because that includes
    # the PV system IDs for the entire dataset (independent of `start_date` and `end_date`).
    # We use `float32` for the ID because we use NaN to indicate a missing PV system,
    # or that this whole example doesn't include PV.
    all_pv_system_ids = pv_capacity_watt_power.index
    pv_system_row_number = np.arange(start=0, stop=len(all_pv_system_ids), dtype=np.float32)
    pv_system_row_number = pd.Series(pv_system_row_number, index=all_pv_system_ids)

    _log.info(
        "After loading:"
        f" {len(pv_power_watts)} PV power datetimes."
        f" {len(pv_power_watts.columns)} PV power PV system IDs."
    )

    pv_power_watts = pv_power_watts.clip(lower=0, upper=5e7)
    pv_power_watts = _drop_pv_systems_which_produce_overnight(pv_power_watts)

    # Resample to 5-minutely and interpolate up to 15 minutes ahead.
    # TODO: Issue #74: Give users the option to NOT resample (because Perceiver IO
    # doesn't need all the data to be perfectly aligned).
    pv_power_watts = pv_power_watts.resample("5T").interpolate(method="time", limit=3)
    pv_power_watts.dropna(axis="index", how="all", inplace=True)
    pv_power_watts.dropna(axis="columns", how="all", inplace=True)

    # Drop any PV systems whose PV capacity is too low:
    PV_CAPACITY_THRESHOLD_W = 100
    pv_systems_to_drop = pv_capacity_watt_power.index[
        pv_capacity_watt_power <= PV_CAPACITY_THRESHOLD_W
    ]
    pv_systems_to_drop = pv_systems_to_drop.intersection(pv_power_watts.columns)
    _log.info(
        f"Dropping {len(pv_systems_to_drop)} PV systems because their max power is less than"
        f" {PV_CAPACITY_THRESHOLD_W}"
    )
    pv_power_watts.drop(columns=pv_systems_to_drop, inplace=True)

    # Ensure that capacity and pv_system_row_num use the same PV system IDs as the power DF:
    pv_system_ids = pv_power_watts.columns
    pv_capacity_watt_power = pv_capacity_watt_power.loc[pv_system_ids]
    pv_system_row_number = pv_system_row_number.loc[pv_system_ids]

    _log.info(
        "After filtering & resampling to 5 minutes:"
        f" pv_power = {pv_power_watts.values.nbytes / 1e6:,.1f} MBytes."
        f" {len(pv_power_watts)} PV power datetimes."
        f" {len(pv_power_watts.columns)} PV power PV system IDs."
    )

    # Sanity checks:
    assert not pv_power_watts.columns.duplicated().any()
    assert not pv_power_watts.index.duplicated().any()
    assert np.isfinite(pv_capacity_watt_power).all()
    assert (pv_capacity_watt_power >= 0).all()
    assert np.isfinite(pv_system_row_number).all()
    assert np.array_equal(pv_power_watts.columns, pv_capacity_watt_power.index)
    return pv_power_watts, pv_capacity_watt_power, pv_system_row_number


# Adapted from nowcasting_dataset.data_sources.pv.pv_data_source
def _load_pv_metadata(filename: str) -> pd.DataFrame:
    """Return pd.DataFrame of PV metadata.

    Shape of the returned pd.DataFrame for Passiv PV data:
        Index: ss_id (Sheffield Solar ID)
        Columns: llsoacd, orientation, tilt, kwp, operational_at,
            latitude, longitude, system_id, x_osgb, y_osgb
    """
    _log.info(f"Loading PV metadata from {filename}")

    if "passiv" in str(filename):
        index_col = "ss_id"
    else:
        index_col = "system_id"

    pv_metadata = pd.read_csv(filename, index_col=index_col)

    if "Unnamed: 0" in pv_metadata.columns:
        pv_metadata.drop(columns="Unnamed: 0", inplace=True)

    _log.info(f"Found {len(pv_metadata)} PV systems in {filename}")

    # drop any systems with no lon or lat:
    pv_metadata.dropna(subset=["longitude", "latitude"], how="any", inplace=True)

    _log.debug(f"Found {len(pv_metadata)} PV systems with locations")

    pv_metadata["x_osgb"], pv_metadata["y_osgb"] = lat_lon_to_osgb(
        latitude=pv_metadata["latitude"], longitude=pv_metadata["longitude"]
    )

    return pv_metadata


def _drop_pv_systems_which_produce_overnight(pv_power_watts: pd.DataFrame) -> pd.DataFrame:
    """Drop systems which produce power over night.

    Args:
        pv_power_watts: Un-normalised.
    """
    # TODO: Of these bad systems, 24647, 42656, 42807, 43081, 51247, 59919
    # might have some salvagable data?
    NIGHT_YIELD_THRESHOLD = 0.4
    night_hours = [22, 23, 0, 1, 2]
    pv_power_normalised = pv_power_watts / pv_power_watts.max()
    night_mask = pv_power_normalised.index.hour.isin(night_hours)
    pv_power_at_night_normalised = pv_power_normalised.loc[night_mask]
    pv_above_threshold_at_night = (pv_power_at_night_normalised > NIGHT_YIELD_THRESHOLD).any()
    bad_systems = pv_power_normalised.columns[pv_above_threshold_at_night]
    _log.info(f"{len(bad_systems)} bad PV systems found and removed!")
    return pv_power_watts.drop(columns=bad_systems)
