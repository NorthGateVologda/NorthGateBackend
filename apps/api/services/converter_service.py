from typing import Tuple
from pyproj import Transformer

def convert_from_4326_to_3857(lon: float, lat: float) -> Tuple[float, float]:
    lonlat_to_webmercator = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    converted_lon, converted_lat = lonlat_to_webmercator.transform(lon, lat)
    return converted_lon, converted_lat