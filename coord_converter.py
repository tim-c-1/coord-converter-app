"""
    This Coordinate Conversion application offers multiple tools to 
    convert and transform coordinate formats and projections.
    Source code is available on https://github.com/tim-c-1/coord-converter-app.

    Copyright (C) 2025 Timothy Cooney

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# import pandas as pd
from osgeo import osr
osr.UseExceptions()

# input_file = input("file to convert: ")
# output_file = input_file[:-4] + "_reduced.csv"

# df = pd.read_csv(input_file)

class Conversions():
    def __init__(self):
        super().__init__()
        
    def ddm_to_dd(ddm):
        try:
            parts = ddm.strip().split()
            degrees = float(parts[0])
            minutes = float(parts[1][:-1])  # Remove the last character (N/S/E/W)
            direction = parts[1][-1]  # Get the N/S/E/W

            dd = degrees + (minutes / 60)
            if direction in ['S', 'W']:  # Negative for South/West
                dd *= -1
            return dd
        except Exception as e:
            print(f"Error converting '{ddm}': {e}")
            return None
    
    def transform_coords(lon, lat, source_epsg="4326", target_epsg="26918"):
        source_srs = osr.SpatialReference()
        source_srs.ImportFromEPSG(int(source_epsg))

        target_srs = osr.SpatialReference()
        target_srs.ImportFromEPSG(int(target_epsg))

        transform = osr.CoordinateTransformation(source_srs, target_srs)

        utm_x, utm_y, _ = transform.TransformPoint(lon,lat)

        return utm_x, utm_y