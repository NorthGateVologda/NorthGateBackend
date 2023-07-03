import logging

from typing import List
from django.contrib.gis.geos import Point
from apps.api.models import ObjectTourism, BufferObjectTourism
from apps.api.mappers import to_buffer_object_tourism

def get_tourist_objects(center_lon: float, center_lat: float,  radius: float) -> List[ObjectTourism]:
    point = Point(center_lon, center_lat, srid=3857)
    logging.info("Точка сформирована: %s", point)
    circle = point.buffer(radius)
    logging.info("Окружность сформирована: %s", circle)
    found_tourist_objects = ObjectTourism.objects.filter(wkb_geometry__intersects=circle)
    return found_tourist_objects

def save_tourist_object(tourist_objects: List[ObjectTourism], username: str) -> None:
    for tourist_object in tourist_objects:
        buffer_object_tourism = to_buffer_object_tourism(tourist_object, username)
        buffer_object_tourism.save()

def del_all_from_buf_by_username(username: str) -> None:
    BufferObjectTourism.objects.filter(username=username).delete()