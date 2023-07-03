import logging

from typing import Tuple
from django.contrib.gis.db.models import GeometryField
from pyproj import Transformer

def convert_from_3857_to_4326(lon: float, lat: float) -> Tuple[float, float]:
    logging.info("Происходит конвертация lon=%s и lat=%s", lon, lat)
    lonlat_to_webmercator = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
    converted_lon, converted_lat = lonlat_to_webmercator.transform(lon, lat)
    logging.info("Координаты сконвертированы converted_lon=%s и converted_lat=%s", converted_lon, converted_lat)
    return converted_lon, converted_lat

def convert_from_4326_to_3857(lon: float, lat: float) -> Tuple[float, float]:
    logging.info("Происходит конвертация lon=%s и lat=%s", lon, lat)
    lonlat_to_webmercator = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    converted_lon, converted_lat = lonlat_to_webmercator.transform(lon, lat)
    logging.info("Координаты сконвертированы converted_lon=%s и converted_lat=%s", converted_lon, converted_lat)
    return converted_lon, converted_lat

def convert_geometry_coords_from_3857_to_4326(geometry: GeometryField):
    logging.info("Преобразование кординат Geometry: %s из 3857 в 4326", geometry)
    coordinates = list(geometry.coords)
    logging.info("Координаты из геометрии: %s", coordinates)

    converted_coordinates = []
    if geometry.geom_type == 'Point':
        logging.info("Тип геометрии - Point")
        converted_lon, converted_lat = convert_from_3857_to_4326(coordinates[0], coordinates[1])
        converted_coordinates.append(converted_lat)
        converted_coordinates.append(converted_lon)
    elif geometry.geom_type == 'LineString' or geometry.geom_type == 'MultiPoint':
        logging.info("Тип геометрии - LineString или MultiPoint")
        for coordinate in coordinates:
            converted_lon, converted_lat = convert_from_3857_to_4326(coordinate[0], coordinate[1])
            converted_coordinates.append([converted_lat, converted_lon])
    elif geometry.geom_type == 'Polygon':
        logging.info("Тип геометрии - Polygon")
        for coordinate in coordinates[0]:
            converted_lon, converted_lat = convert_from_3857_to_4326(coordinate[0], coordinate[1])
            converted_coordinates.append([converted_lat, converted_lon])
    elif geometry.geom_type == 'MultiLineString':
        logging.info("Тип геометрии - MultiLineString")
        for line in coordinates:
            converted_line = []
            for coordinate in line:
                converted_lon, converted_lat = convert_from_3857_to_4326(coordinate[0], coordinate[1])
                converted_line.append([converted_lat, converted_lon])
            converted_coordinates.append(converted_line)
    elif geometry.geom_type == 'MultiPolygon':
        logging.info("Тип геометрии - MultiPolygon")
        for polygon in coordinates:
            converted_polygon = []
            for line in polygon:
                converted_line = []
                for coordinate in line:
                    converted_lon, converted_lat = convert_from_3857_to_4326(coordinate[0], coordinate[1])
                    converted_line.append([converted_lat, converted_lon])
                converted_polygon.append(converted_line)
            converted_coordinates.append(converted_polygon)

    return converted_coordinates