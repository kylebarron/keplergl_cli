# Changelog

## 0.3.4 (2022-09-01)

- Arguments to save maps at user-defined location and use a custom configuration file
- Respect `open_browser=False` even during the class instantiation with data

## 0.3.3 (2022-06-27)

- Revert usage of `__geo_interface__`

## 0.3.2 (2022-06-27)

- Use `__geo_interface__` when possible
- Respect `open_browser=False`
- Fix centering map

## 0.3.1 (2020-02-26)

- Fix for stdin

## 0.3.0 (2020-02-26)

- Support GeoJSON on stdin
- Rename `keplergl_quickvis` to `keplergl_cli`
- Rename CLI entry point to `kepler`
- CLI option for which layers from file to display

## 0.2.0 (2019-12-09)

- Automatically attempt to reproject to EPSG 4326

## 0.1.0 (2019-12-05)

- First release on PyPI.
