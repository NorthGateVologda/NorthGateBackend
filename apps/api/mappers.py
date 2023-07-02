from apps.api.models import ObjectTourism, BufferObjectTourism


def to_buffer_object_tourism(object_tourism: ObjectTourism, username: str):
    buffer_object_tourism = BufferObjectTourism()
    buffer_object_tourism.name = object_tourism.name
    buffer_object_tourism.city = object_tourism.city
    buffer_object_tourism.street = object_tourism.street
    buffer_object_tourism.house = object_tourism.house
    buffer_object_tourism.post = object_tourism.post
    buffer_object_tourism.x = object_tourism.x
    buffer_object_tourism.y = object_tourism.y
    buffer_object_tourism.wkb_geometry = object_tourism.wkb_geometry
    buffer_object_tourism.username = username
    return buffer_object_tourism
