"""Statistical Functions."""
from typing import Any

import netCDF4
import numpy as np
import numpy.typing as npt


def get_average_wtime(data: npt.NDArray[Any], wghts: npt.NDArray[np.double]) -> Any:
    """Get average of array (data) using weights (wghts).

    Args:
        data (npt.NDArray[Any]): _description_
        wghts (npt.NDArray[np.double]): _description_

    Returns:
        Any: _description_
    """
    try:
        v_ave = np.average(data, weights=wghts, axis=1)
    except ZeroDivisionError:
        print("zero division error")
        v_ave = netCDF4.default_fillvals["f8"]
    return v_ave


def get_stddev_wtime(data: npt.NDArray[Any], wghts: npt.NDArray[np.double]) -> Any:
    """Get standard deviation of array (data) using weights (wghts).

    Args:
        data (npt.NDArray[Any]): _description_
        wghts (npt.NDArray[np.double]): _description_

    Returns:
        Any: _description_
    """
    try:
        v_ave = np.average(data, weights=wghts, axis=1)
        variance = np.average((data - v_ave) ** 2, weights=wghts, axis=1)
        stddev = np.sqrt(variance)
    except ZeroDivisionError:
        print("zero division error")
        stddev = netCDF4.default_fillvals["f8"]
    return stddev


def get_average(data: npt.NDArray[Any], wghts: npt.NDArray[np.double]) -> Any:
    """Get average of array (data) using weights (wghts).

    Args:
        data (npt.NDArray[Any]): _description_
        wghts (npt.NDArray[np.double]): _description_

    Returns:
        Any: _description_
    """
    try:
        v_ave = np.average(data, weights=wghts)
    except ZeroDivisionError:
        print("zero division error")
        v_ave = netCDF4.default_fillvals["f8"]
    return v_ave


def get_ma_average_wtime(ndata: npt.NDArray[Any], wghts: npt.NDArray[np.double]) -> Any:
    """Get masked average.

    Args:
        ndata (npt.NDArray[Any]): _description_
        wghts (npt.NDArray[np.double]): _description_

    Returns:
        Any: _description_
    """
    mdata = np.ma.masked_array(ndata, np.isnan(ndata))  # type:ignore
    return np.ma.average(mdata, weights=wghts, axis=1)


def get_ma_stddev_wtime(ndata: npt.NDArray[Any], wghts: npt.NDArray[np.double]) -> Any:
    """Get masked standard deviation.

    Args:
        ndata (npt.NDArray[Any]): _description_
        wghts (npt.NDArray[np.double]): _description_

    Returns:
        Any: _description_
    """
    mdata = np.ma.masked_array(ndata, np.isnan(ndata))  # type:ignore
    v_avg = np.ma.average(mdata, weights=wghts, axis=1)  # type:ignore
    variance = np.ma.average((mdata - v_avg) ** 2, weights=wghts, axis=1)  # type:ignore
    return np.sqrt(variance)


def get_ma_average(ndata: npt.NDArray[Any], wghts: npt.NDArray[np.double]) -> Any:
    """Get masked average.

    Args:
        ndata (npt.NDArray[Any]): _description_
        wghts (npt.NDArray[np.double]): _description_

    Returns:
        Any: _description_
    """
    mdata = np.ma.masked_array(ndata, np.isnan(ndata))  # type:ignore
    return np.ma.average(mdata, weights=wghts)
