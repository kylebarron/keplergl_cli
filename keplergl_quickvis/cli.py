"""Console script for kepler_quickvis."""
import sys
from pathlib import Path

import click
import geopandas as gpd

from keplergl_quickvis import Visualize


@click.command()
@click.option(
    '--api_key',
    type=str,
    default=None,
    help=
    'Mapbox API Key. Must be provided on the command line or exist in the MAPBOX_API_KEY environment variable.'
)
@click.option(
    '--style',
    type=str,
    default='streets',
    show_default=True,
    help=
    'Mapbox style. Accepted values are: streets, outdoors, light, dark, satellite, satellite-streets, or a custom style URL.'
)
@click.argument('files', nargs=-1, required=True, type=click.Path(exists=True))
def main(api_key, style, files):
    """Interactively view geospatial data using kepler.gl"""
    vis = Visualize(api_key=api_key, style=style)

    # For each file, try to load data with GeoPandas
    for file_name in files:
        layer_name = Path(file_name).stem
        gdf = gpd.read_file(file_name)

        # Try to automatically reproject to epsg 4326
        # For some reason, it takes forever to call gdf.crs, so I don't want to
        # first check the crs, then reproject. Anyways, reprojecting from epsg
        # 4326 to epsg 4326 should be instant
        try:
            gdf = gdf.to_crs(epsg=4326)
        except:
            pass

        vis.add_data(gdf, layer_name)

    vis.render(open_browser=True, read_only=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
