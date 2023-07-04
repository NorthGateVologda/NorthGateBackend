import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.api.exceptions import InvalidRequestException
from .services.converter_service import convert_from_4326_to_3857
from .services.object_tourism_service import get_tourist_objects, save_tourist_object, del_all_from_buf_by_username
from .services.username_service import is_exists_username, save_username


class ObjectTourismView(APIView):
    def post(self, request):
        if not request.data:
            return InvalidRequestException("Missing required body")

        center_lat = request.data.get("center_lat")
        center_lon = request.data.get("center_lon")
        radius = request.data.get("radius")
        username = request.data.get("username")

        logging.info("center_lat=%s, center_lon=%s, radius=%s, username=%s", center_lat, center_lon, radius, username)

        if not all([center_lat, center_lon, radius, username]):
            raise InvalidRequestException("Missing required parameters: center or radius or username")

        if not is_exists_username(username):
            logging.info("Имя пользователя не существует, сохраняю имя в базу")
            save_username(username)
        else:
            logging.info("Имя пользователя существует, удаляю из буфера")
            del_all_from_buf_by_username(username)

        center_lon, center_lat = convert_from_4326_to_3857(float(center_lon), float(center_lat))
        tourist_objects = get_tourist_objects(float(center_lon), float(center_lat), float(radius))
        logging.info("Получено %s туристических объектов, происходит их сохранение", len(tourist_objects))
        save_tourist_object(tourist_objects, username)

        return Response(status=status.HTTP_201_CREATED)
