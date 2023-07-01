from typing import Tuple
from pyproj import Transformer

def convert_from_4326_to_3857(lat: float, lon: float) -> Tuple[float, float]:
    lonlat_to_webmercator = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
    converted_lat, converted_lon = lonlat_to_webmercator.transform(lat, lon)
    return converted_lat, converted_lon