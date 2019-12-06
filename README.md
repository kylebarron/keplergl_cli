# keplergl_quickvis

## Overview

Uber's open-source [kepler.gl](https://kepler.gl/) is a great browser-based
platform for interactively visualizing geospatial data. The `keplergl` Python package's [included
documentation](https://github.com/keplergl/kepler.gl/blob/master/docs/keplergl-jupyter/user-guide.md)
is almost entirely directed at use within Jupyter, and it took a little bit of
work to figure out how to use it from a non-Jupyter Python environment.

`keplergl_quickvis` is a simple wrapper to quickly get your geospatial objects from Python into kepler.gl in the browser. It's as simple as

```
keplergl_quickvis --style=outdoors data.geojson
```

from the command line, or from Python

```py
from keplergl_quickvis import Visualize
Visualize(data)
```

![Example gif](https://raw.githubusercontent.com/kylebarron/kepler_quickvis/master/assets/example.gif)

## Features

-   One-line data visualization
-   Automatically converts Shapely objects to GeoJSON
-   No configuration needed

## Install

**Mapbox API key**: in order to display Mapbox-hosted maps, you need to provide
a Mapbox API key. Go to [Mapbox.com](https://account.mapbox.com/access-tokens)
to get an API key.

**Package install**:

```
pip install keplergl_quickvis
```

This package has dependencies on `geojson`, `shapely`, and `geopandas`. If you
get errors when installing this package through pip, it may be easier to first
install dependencies through Conda, then installing this package. I.e.:

```
conda install geojson shapely geopandas -c conda-forge
pip install keplergl_quickvis
```

## Usage

### CLI

The CLI is installed under the name `keplergl_quickvis`:

```
export MAPBOX_API_KEY=...
keplergl_quickvis --style=outdoors data.geojson
keplergl_quickvis --style=dark data1.geojson shapefile.shp geodatabase.gdb
```

You can supply data in any [vector format readable by GeoPandas/GDAL](https://gdal.org/drivers/vector/index.html).

Supply `--help` to see the CLI's help menu:

```
> keplergl_quickvis --help

Usage: keplergl_quickvis [OPTIONS] FILES...

  Interactively view geospatial data using kepler.gl

Options:
  --reproject     Attempt to reproject source data to WGS84 (EPSG 4326). Data
                  must be in WGS84 to be visualized correctly. This will only
                  work if the source files include metadata on their
                  projection  [default: False]
  --api_key TEXT  Mapbox API Key. Must be provided on the command line or
                  exist in the MAPBOX_API_KEY environment variable.
  --style TEXT    Mapbox style. Accepted values are: streets, outdoors, light,
                  dark, satellite, satellite-streets, or a custom style URL.
                  [default: streets]
  --help          Show this message and exit.
```

### Python API

Simplest usage:

```py
import geopandas as gpd
from keplergl_quickvis import Visualize

# Create your geospatial objects
gdf = gpd.GeoDataFrame(...)

# Visualize one or multiple objects at a time
Visualize(gdf, api_key=MAPBOX_API_KEY)
Visualize([gdf, shapely_object, geojson_string], api_key=MAPBOX_API_KEY)
```

More detail over the objects in your map:

```py
from keplergl_quickvis import Visualize
vis = Visualize(api_key=MAPBOX_API_KEY)
vis.add_data(data=data, names='name of layer')
vis.add_data(data=data2, names='name of layer')
html_path = vis.render(open_browser=True, read_only=False)
```

**Visualize**

```py
Visualize(data=None, names=None, read_only=False, api_key=None, style=None)
```

-   `data` (either `None`, a single data object, or a list of data objects):

    A data object may be a GeoDataFrame from the
    [GeoPandas](http://geopandas.org/) library, any geometry from the
    [Shapely](https://shapely.readthedocs.io/en/stable/manual.html) library, any
    object from the [GeoJSON](https://github.com/jazzband/geojson) library, or
    any GeoJSON string or dictionary. You can also provide a CSV file as a
    string or a Pandas DataFrame if the DataFrame has `Latitude` and `Longitude`
    columns. Full documentation on the accepted data formats is
    [here](https://github.com/keplergl/kepler.gl/blob/master/docs/keplergl-jupyter/user-guide.md#3-data-format).

    You can provide either a single data object, or an iterable containing
    multiple allowed data objects.

    If data is not `None`, then Visualize(data) will perform all steps, including
    rendering the data to an HTML file and opening it in a new browser tab.

-   `names` (either `None`, a string, or a list of strings):

    This defines the names shown for each layer in Kepler.gl. If `None`, the
    layers will be named `data_0`, `data_1`, and so on. Otherwise, if `data` is
    a single object, `names` should be a string, and if `data` is an iterable,
    then `names` should be an iterable of strings.

-   `read_only` (`boolean`): If `True`, hides side panel to disable map customization
-   `api_key` (`string`): Mapbox API key. Go to [Mapbox.com](https://account.mapbox.com/access-tokens)
    to get an API key. If not provided, the `MAPBOX_API_KEY` environment
    variable must be set, or the `style_url` must point to a `style.json` file
    that does not use Mapbox map tiles.
-   `style` (`string`): The basemap style to use. Standard Mapbox options are:

    -   `streets`
    -   `outdoors`
    -   `light`
    -   `dark`
    -   `satellite`
    -   `satellite-streets`

    The default is `streets`. Alternatively, you can supply a path to a custom
    style. A custom style created from Mapbox Studio should have a url that
    starts with `mapbox://`. Otherwise, a custom style using third-party map
    tiles should be a URL to a JSON file that conforms to the [Mapbox Style
    Specification](https://docs.mapbox.com/mapbox-gl-js/style-spec/).

**Visualize.add_data()**

```py
Visualize.add_data(data, names=None):
```

-   `data` (either a single data object, or a list of data objects):

    A data object may be a GeoDataFrame from the
    [GeoPandas](http://geopandas.org/) library, any geometry from the
    [Shapely](https://shapely.readthedocs.io/en/stable/manual.html) library, any
    object from the [GeoJSON](https://github.com/jazzband/geojson) library, or
    any GeoJSON string or dictionary. You can also provide a CSV file as a
    string or a Pandas DataFrame if the DataFrame has `Latitude` and `Longitude`
    columns. Full documentation on the accepted data formats is
    [here](https://github.com/keplergl/kepler.gl/blob/master/docs/keplergl-jupyter/user-guide.md#3-data-format).

    You can provide either a single data object, or an iterable containing
    multiple allowed data objects.

-   `names` (either `None`, a string, or a list of strings):

    This defines the names shown for each layer in Kepler.gl. If `None`, the
    layers will be named `data_0`, `data_1`, and so on. Otherwise, if `data` is
    a single object, `names` should be a string, and if `data` is an iterable,
    then `names` should be an iterable of strings.

**Visualize.render()**

```py
Visualize.render(open_browser=True, read_only=False)
```

-   `read_only` (`boolean`): If `True`, hides side panel to disable map customization
-   `open_browser` (`boolean`): If `True`, opens the saved HTML file in the default browser

## Troubleshooting

The most common reasons why a map is not displayed are:

-   Missing Mapbox API Key: in order to display Mapbox-hosted maps, you need get [an API key from Mapbox](https://account.mapbox.com/access-tokens) to pass an API key
-   Data projection: Kepler.gl works only with data projected into standard WGS84 (latitude, longitude) coordinates. If you have your data in a projected coordinate system, first reproject your data into WGS84 (EPGS 4326), then try again

If your data seems to be "floating" above the map, this is likely because your
input data have Z coordinates, so kepler.gl displays them in 3-dimensional space.
