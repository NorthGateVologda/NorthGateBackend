from typing import List

from django.contrib.gis.geos import Point
from apps.api.models import ObjectTourism, BufferObjectTourism
from apps.api.mappers import to_buffer_object_tourism
from apps.api.services.converter_service import convert_from_4326_to_3857

def get_tourist_objects(center_lat: float, center_lon: float, radius: float) -> List[ObjectTourism]:
    lat, lon = convert_from_4326_to_3857(center_lat, center_lon)
    point = Point(lat, lon, srid=3857)
    circle = point.buffer(radius)
    found_tourist_objects = ObjectTourism.objects.filter(wkb_geometry__intersects=circle)
    return found_tourist_objects

def save_tourist_object(tourist_objects: List[ObjectTourism], username: str) -> None:
    for tourist_object in tourist_objects:
        buffer_object_tourism = to_buffer_object_tourism(tourist_object, username)
        BufferObjectTourism.objects.create(**buffer_object_tourism)

def del_all_from_buf_by_username(username: str) -> None:
    BufferObjectTourism.objects.filter(username=username).delete()