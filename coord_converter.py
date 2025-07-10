# import pandas as pd
from osgeo import osr


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