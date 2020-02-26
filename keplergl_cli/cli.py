"""Console script for keplergl_cli."""
import json
# Some imports are loaded conditionally later to try to make the CLI more
# responsive
import sys
from pathlib import Path

import click
import fiona
import geojson
import geopandas as gpd

from .keplergl_cli import Visualize


# https://stackoverflow.com/a/45845513
def get_stdin(ctx, param, value):
    if not value and not click.get_text_stream('stdin').isatty():
        return (click.get_text_stream('stdin').read().strip(), )
    else:
        return value


@click.command()
@click.option(
    '-l',
    '--layer',
    type=str,
    default=None,
    required=False,
    multiple=True,
    help='Layer names. If not provided, will display all layers')
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
@click.argument('files', nargs=-1, callback=get_stdin, type=str)
def main(layer, api_key, style, files):
    """Interactively view geospatial data using kepler.gl"""
    vis = Visualize(api_key=api_key, style=style)

    # For each file, try to load data with GeoPandas
    for item in files:
        # If body exists as a path; assume it represents a Path
        try:
            path = Path(item)
            if path.exists():
                layers = fiona.listlayers(path)

                if layer:
                    layers = [x for x in layers if x in layer]

                click.echo(f'Loading layers from {path}')
                for l in layers:
                    click.echo(l)
                    vis.add_data(*load_file(path, l))
                    # layer = ('NHDFlowline', )
                continue

        except OSError:
            # Otherwise, it should be GeoJSON
            # First try to parse entire stdin as single GeoJSON
            # If this fails, assume it's newline delimited where each feature is
            # on a single line
            try:
                vis.add_data(geojson.loads(item))

            except json.JSONDecodeError:
                lines = item.split('\n')
                features = [geojson.loads(l) for l in lines]
                vis.add_data(geojson.FeatureCollection(features))

    vis.render(open_browser=True, read_only=False)
    return 0


def load_file(path, layer=None):
    """Load geospatial data at path

    Loads data with GeoPandas; reprojects to 4326
    """
    layer_name = layer or path.stem
    gdf = gpd.read_file(path, layer=layer)

    # Remove null geometries
    gdf = gdf[gdf.geometry.notna()]

    # Try to automatically reproject to epsg 4326
    # For some reason, it takes forever to call gdf.crs, so I don't want
    # to first check the crs, then reproject. Anyways, reprojecting from
    # epsg 4326 to epsg 4326 should be instant
    try:
        gdf = gdf.to_crs(epsg=4326)
    except:
        pass

    return gdf, layer_name


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
