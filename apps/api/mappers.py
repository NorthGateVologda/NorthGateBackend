import logging

from apps.api.models import ObjectTourism, BufferObjectTourism
from apps.api.services.converter_service import convert_geometry_coords_from_3857_to_4326


def to_buffer_object_tourism(object_tourism: ObjectTourism, username: str):
    logging.info("Преобразование объекта в буфер")
    buffer_object_tourism = BufferObjectTourism()
    buffer_object_tourism.name = object_tourism.name
    buffer_object_tourism.city = object_tourism.city
    buffer_object_tourism.street = object_tourism.street
    buffer_object_tourism.house = object_tourism.house
    buffer_object_tourism.post = object_tourism.post
    buffer_object_tourism.x = object_tourism.x
    buffer_object_tourism.y = object_tourism.y
    buffer_object_tourism.username = username
    buffer_object_tourism.wkb_geometry = str(convert_geometry_coords_from_3857_to_4326(object_tourism.wkb_geometry))
    logging.info("Буфер сформирован: %s", buffer_object_tourism)
    return buffer_object_tourism