import json
import os
import tempfile
import webbrowser
from pathlib import Path

import dotenv
import geojson
import shapely.geometry
from keplergl import KeplerGl
from shapely.geometry import mapping

SHAPELY_GEOJSON_CLASSES = [
    shapely.geometry.LineString,
    shapely.geometry.LinearRing,
    shapely.geometry.MultiLineString,
    shapely.geometry.MultiPoint,
    shapely.geometry.MultiPolygon,
    shapely.geometry.Point,
    shapely.geometry.Polygon,
    geojson.Feature,
    geojson.FeatureCollection,
    geojson.GeoJSON,
    geojson.GeoJSONEncoder,
    geojson.GeometryCollection,
    geojson.LineString,
    geojson.MultiLineString,
    geojson.MultiPoint,
    geojson.MultiPolygon,
    geojson.Point,
    geojson.Polygon,
]


class Visualize:
    """Quickly visualize data in browser over Mapbox tiles with the help of the AMAZING kepler.gl.
    """
    def __init__(self, data=None, names=None, read_only=False):
        """Visualize data using kepler.gl

        Args:
            data Optional[Union[List[]]]:
                either None, a List of data objects, or a single data object. If
                data is not None, then Visualize(data) will perform all steps,
                including rendering and opening a browser.
        """
        super(Visualize, self).__init__()

        dotenv.load_dotenv()
        self.MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY')
        assert self.MAPBOX_API_KEY is not None, ''

        self.map = KeplerGl(config=self.config)

        if data is not None:
            self.add_data(data=data, names=names)
            self.render(read_only=read_only)

    @property
    def config(self):
        """Load kepler.gl config and insert Mapbox API Key"""

        import os
        current_directory = os.path.dirname(os.path.abspath(__file__))
        config_file = Path(current_directory) / 'keplergl_config.json'

        with open(config_file) as f:
            keplergl_config = json.load(f)

        # Replace redacted API key with actual API key
        keplergl_config['config']['config']['mapStyle']['mapStyles']['aobtafp'][
            'accessToken'] = self.MAPBOX_API_KEY
        keplergl_config['config']['config']['mapStyle']['mapStyles']['aobtafp'][
            'icon'] = keplergl_config['config']['config']['mapStyle'][
                'mapStyles']['aobtafp']['icon'].replace(
                    'access_token=redacted',
                    f'access_token={self.MAPBOX_API_KEY}')

        # Remove map state in the hope that it'll auto-center based on data
        # keplergl_config['config']['config'].pop('mapState')
        return keplergl_config['config']

    def add_data(self, data, names=None):
        """Add data to kepler map

        Data should be either GeoJSON or GeoDataFrame. Kepler isn't aware of the
        geojson or shapely package, so if I supply an object from one of these
        libraries, first convert it to a GeoJSON dict.
        """
        # Make `data` iterable
        if not isinstance(data, list):
            data = [data]

        # Make `names` iterable and of the same length as `data`
        if isinstance(names, list):
            # Already iterable, make sure they're the same length
            msg = 'data and names are iterables different length'
            assert len(data) == len(names), msg
        else:
            # `names` not iterable, make sure it's the same length as `data`
            name_stub = 'data' if names is None else names
            names = [f'{name_stub}_{x}' for x in range(len(data))]

        for datum, name in zip(data, names):
            if any(isinstance(datum, c) for c in SHAPELY_GEOJSON_CLASSES):
                datum = dict(mapping(datum))

            self.map.add_data(data=datum, name=name)

    def render(self, open_chrome=True, read_only=False):
        """Export kepler.gl map to HTML file and open in Chrome
        """
        # Generate path to a temporary file
        path = os.path.join(tempfile.mkdtemp(), 'vis.html')
        self.map.save_to_html(file_name=path, read_only=read_only)

        # Open Chrome to saved page
        # Note, path to Chrome executable likely different on Windows/Linux
        # 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        # chrome_path = '/usr/bin/google-chrome %s'
        chrome_bin = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        if Path(chrome_bin).exists() and open_chrome:
            # Add \ to spaces
            s = 'open -a ' + chrome_bin.replace(' ', '\ ') + ' %s'
            webbrowser.get(s).open(path)
        else:
            print('Warning: Chrome binary not found; path ')
