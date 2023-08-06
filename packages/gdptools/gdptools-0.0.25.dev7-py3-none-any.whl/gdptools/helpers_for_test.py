"""Helper functions for testing area-weighted aggragation."""
import logging
import time
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import geopandas as gpd
import numpy as np
import numpy.typing as npt
import pandas as pd
import xarray as xr
from pygeos import GEOSException

from .ancillary import _check_for_intersection
from .ancillary import _get_cells_poly
from .ancillary import _get_crs
from .ancillary import _get_data_via_catalog
from .ancillary import _get_print_on
from .ancillary import _get_shp_file
from .ancillary import _quadrat_cut_geometry
from .ancillary import _read_shp_file
from .gdp_data_class import CatGrids
from .gdp_data_class import CatParams

# from numba import jit

logger = logging.getLogger(__name__)


def generate_weights_test(
    poly: gpd.GeoDataFrame,
    poly_idx: str,
    grid_cells: gpd.GeoDataFrame,
    wght_gen_crs: str,
    filename: Optional[str] = None,
) -> Tuple[pd.DataFrame, List[npt.NDArray[np.double]], List[pd.DataFrame]]:
    """Generate weights for aggragations of poly-to-poly mapping with extra output.

    Args:
        poly (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        grid_cells (gpd.GeoDataFrame): _description_
        wght_gen_crs (str): _description_
        filename (Optional[str], optional): _description_. Defaults to None.

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        Tuple[pd.DataFrame, List[npt.NDArray[np.double]], List[pd.DataFrame]]: _description_
    """
    # check if poly_idx in in poly
    if poly_idx not in poly.columns:
        error_string = (
            f"Error: poly_idx ({poly_idx}) is not found in the poly ({poly.columns})"
        )
        raise ValueError(error_string)

    if not poly.crs:
        error_string = f"polygons don't contain a valid crs: {poly.crs}"
        raise ValueError(error_string)

    if not grid_cells.crs:
        error_string = f"grid_cells don't contain a valid crs: {grid_cells.crs}"
        raise ValueError(error_string)

    grid_out_crs = _get_crs(wght_gen_crs)

    start = time.perf_counter()
    grid_cells.to_crs(grid_out_crs, inplace=True)

    npoly = poly.to_crs(grid_out_crs)
    end = time.perf_counter()
    print(
        f"Reprojecting to epsg:{wght_gen_crs} finished in  {round(end-start, 2)} second(s)"
    )

    start = time.perf_counter()
    spatial_index = grid_cells.sindex
    # print(type(spatial_index))
    end = time.perf_counter()
    print(f"Spatial index generations finished in {round(end-start, 2)} second(s)")
    start = time.perf_counter()
    tcount = 0

    numrows = len(poly.index)
    print_on = _get_print_on(numrows)

    # in order, i_index, j_index, poly_index, weight values
    i_index = []
    j_index = []
    p_index = []
    wghts = []
    pm = []
    resint = []

    for index, row in npoly.iterrows():
        # hru_area = poly.loc[poly[poly_idx] == row[poly_idx]].geometry.area.sum()
        hru_area = row.geometry.area
        if possible_matches_index := list(
            spatial_index.intersection(row["geometry"].bounds)
        ):
            possible_matches = grid_cells.iloc[possible_matches_index]
            precise_matches = possible_matches[
                possible_matches.intersects(row["geometry"])
            ]
            pm.append(precise_matches)
            if len(precise_matches) != 0:
                res_intersection = gpd.overlay(
                    npoly.loc[[index]], precise_matches, how="intersection"
                )
                resint.append(res_intersection)
                for nindex, row in res_intersection.iterrows():
                    tmpfloat = float(res_intersection.area.iloc[nindex] / hru_area)
                    i_index.append(int(row["i_index"]))
                    j_index.append(int(row["j_index"]))
                    p_index.append(str(row[poly_idx]))
                    wghts.append(tmpfloat)
                tcount += 1
                if tcount % print_on == 0:
                    print(tcount, index, flush=True)

        else:
            print("no intersection: ", index, flush=True)

    wght_df = pd.DataFrame(
        {
            poly_idx: p_index,
            "i": i_index,
            "j": j_index,
            "wght": wghts,
        }
    )
    if filename:
        wght_df.to_csv(filename)
    end = time.perf_counter()
    logger.info(f"Weight generations finished in {round(end-start, 2)} second(s)")
    return wght_df, pm, resint


def generate_weights_test2(
    poly: gpd.GeoDataFrame,
    poly_idx: str,
    grid_cells: gpd.GeoDataFrame,
    wght_gen_crs: str,
    filename: Optional[str] = None,
) -> Tuple[pd.DataFrame, List[pd.DataFrame]]:
    """Generate weights for aggragations of poly-to-poly mapping with extra output.

    Args:
        poly (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        grid_cells (gpd.GeoDataFrame): _description_
        wght_gen_crs (str): _description_
        filename (Optional[str], optional): _description_. Defaults to None.

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        Tuple[pd.DataFrame, List[npt.NDArray[np.double]], List[pd.DataFrame]]: _description_
    """
    # check if poly_idx in in poly
    if poly_idx not in poly.columns:
        msg = f"Error: poly_idx ({poly_idx}) is not found in the poly ({poly.columns})"
        raise ValueError(msg)

    if not poly.crs:
        error_string = f"polygons don't contain a valid crs: {poly.crs}"
        raise ValueError(error_string)

    if not grid_cells.crs:
        error_string = f"grid_cells don't contain a valid crs: {grid_cells.crs}"
        raise ValueError(error_string)

    grid_out_crs = _get_crs(wght_gen_crs)

    start = time.perf_counter()
    grid_cells.to_crs(grid_out_crs, inplace=True)
    gc_meanarea = grid_cells.area.mean()
    npoly = poly.to_crs(grid_out_crs)
    end = time.perf_counter()
    print(
        f"Reprojecting to epsg:{wght_gen_crs} finished in  {round(end-start, 2)} second(s)"
    )

    start = time.perf_counter()
    spatial_index = grid_cells.sindex
    # print(type(spatial_index))
    end = time.perf_counter()
    print(f"Spatial index generations finished in {round(end-start, 2)} second(s)")
    start = time.perf_counter()

    numrows = len(poly.index)
    print_on = _get_print_on(numrows)

    # in order, i_index, j_index, poly_index, weight values
    i_index = []
    j_index = []
    p_index = []
    wghts = []
    res_int = []

    for index in np.arange(numrows):
        # tstart = time.perf_counter()
        tp, ti, tj, tw, resint = generate_feature_weight2_test(
            spind=spatial_index,
            grid_cells=grid_cells,
            row=npoly.iloc[[index]],
            poly_idx=poly_idx,
            row_index=index,
            quadrat_width=np.sqrt(10.0 * gc_meanarea),
        )
        # tend = time.perf_counter()
        # print(f"   feature: {index}, {tend - tstart:0.4f} seconds")
        p_index.extend(tp)
        i_index.extend(ti)
        j_index.extend(tj)
        wghts.extend(tw)
        res_int.append(resint)

        if index % print_on == 0:
            print(
                f"Calculating weights index: {index} and for \
                    feature {npoly.loc[index, poly_idx]}",
                flush=True,
            )

    wght_df = pd.DataFrame(
        {
            poly_idx: p_index,
            "i": i_index,
            "j": j_index,
            "wght": wghts,
        }
    )
    wght_df = wght_df.astype({"i": int, "j": int, "wght": float, poly_idx: str})
    if filename:
        wght_df.to_csv(filename)
    end = time.perf_counter()
    logger.info(f"Weight generations finished in {round(end-start, 2)} second(s)")
    return wght_df, res_int


def calc_weights_catalog_test(
    params_json: CatParams,
    grid_json: CatGrids,
    shp_file: Union[str, gpd.GeoDataFrame],
    shp_poly_idx: str,
    date: str,
    wght_gen_proj: Any,
    wght_gen_file: str,
) -> Tuple[
    Union[xr.Dataset, xr.DataArray],
    gpd.GeoDataFrame,
    list[gpd.GeoDataFrame],
    pd.DataFrame,
]:
    """Calculate area-intersected weights of grid to feature."""
    # run check on intersection of shape features and gridded data
    gdf = _read_shp_file(shp_file)
    is_intersect, is_degrees, is_0_360 = _check_for_intersection(
        params_json=params_json, grid_json=grid_json, gdf=gdf
    )
    # read shapefile, calculate total_bounds, and project to grid's projection
    gdf, gdf_bounds = _get_shp_file(
        shp_file=gdf, grid_json=grid_json, is_degrees=is_degrees
    )

    ds_proj = grid_json.proj
    # only need one time step for generating weights so choose the first time from the param_cat
    # date = params_json.duration.split("/")[0]

    # get sub-setted xarray dataset
    rotate_ds = bool((not is_intersect) & is_degrees & (not is_0_360))
    ds_ss = _get_data_via_catalog(
        params_json=params_json,
        grid_json=grid_json,
        bounds=gdf_bounds,
        begin_date=date,
        rotate_lon=rotate_ds,
    )
    tsrt = time.perf_counter()
    ds_ss.load()
    tend = time.perf_counter()

    print(f"loading {params_json.varname} in {tend-tsrt:0.4f} seconds")
    # get grid polygons to calculate intersection with polygon of interest - shp_file
    xname = grid_json.X_name
    yname = grid_json.Y_name
    var = params_json.variable
    gdf_grid = _get_cells_poly(ds_ss, x=xname, y=yname, var=var, crs_in=ds_proj)
    # gdf_grid = gpd.GeoDataFrame.from_features(gridpoly)

    # calculate the intersection weights and generate weight_file
    # assumption is that the first column in the shp_file is the id to use for
    # calculating weights
    if shp_poly_idx not in gdf.columns[:]:
        raise ValueError(
            f"shp_poly_idx: {shp_poly_idx} not in gdf columns: {gdf.columns}"
        )
    else:
        apoly_idx = shp_poly_idx

    wght_gen, inter_sect = generate_weights_test2(
        poly=gdf,
        poly_idx=apoly_idx,
        grid_cells=gdf_grid,
        filename=wght_gen_file,
        wght_gen_crs=wght_gen_proj,
    )

    return ds_ss, gdf_grid, inter_sect, wght_gen


def generate_feature_weight2_test(
    spind: gpd.GeoSeries.sindex,
    grid_cells: gpd.GeoDataFrame,
    row: gpd.GeoDataFrame,
    poly_idx: str,
    row_index: int,
    quadrat_width: Any,
) -> Tuple[List[str], List[int], List[int], List[float], List[pd.DataFrame]]:
    """Generate feature weights and return intersections for testing.

    Args:
        spind (gpd.GeoSeries.sindex): _description_
        grid_cells (gpd.GeoDataFrame): _description_
        row (gpd.GeoDataFrame): _description_
        poly_idx (str): _description_
        row_index (int): _description_
        quadrat_width (Any): _description_

    Returns:
        Tuple[ List[str], List[int], List[int], List[float], List[pd.DataFrame], ]:
        _description_
    """
    hru_area = row["geometry"].area
    multipoly = _quadrat_cut_geometry(
        row["geometry"].values[0], quadrat_width=quadrat_width
    )
    geoms = set()

    # print(f'Number of sub-polygons {len(multipoly.geoms)}')
    for spindex, poly in enumerate(multipoly.geoms):

        try:
            possible_matches_index = list(spind.intersection(poly.bounds))
        except AttributeError:
            print(
                f"User feature Attribute error index: {row_index} \
                    subpoly_index: {spindex} has an error"
            )

        if possible_matches_index:
            possible_matches = grid_cells.iloc[possible_matches_index]
            try:
                precise_matches = possible_matches[possible_matches.intersects(poly)]
                # pm.extend(precise_matches)
            except GEOSException:
                print(
                    f"User feature GEOSException error: index={row_index}, \
                    sub_poly={spindex}"
                )
            except TypeError:
                print(
                    f"User feature Type error: index={row_index}, \
                    sub_poly={spindex}"
                )
            geoms.update(precise_matches.index)
        else:
            print("no intersection: ", row_index, spindex, flush=True)
    i_index = []
    j_index = []
    p_index = []
    wghts = []
    if len(precise_matches) != 0:
        res_intersection = row.overlay(grid_cells.iloc[list(geoms)], how="intersection")
        wghts.extend(res_intersection.geometry.area.values / hru_area.values[0])
        i_index.extend(res_intersection["i_index"].astype(int).to_list())
        j_index.extend(res_intersection["j_index"].astype(int).to_list())

    num_cells = len(wghts)
    p_index = [row[poly_idx].values[0]] * num_cells
    return p_index, i_index, j_index, wghts, res_intersection
