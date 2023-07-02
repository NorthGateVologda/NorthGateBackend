from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.api.exceptions import InvalidRequestException
from .services.object_tourism_service import *
from .services.username_service import *


class ObjectTourismView(APIView):
    def post(self, request):
        if not request.data:
            return InvalidRequestException("Missing required body")

        center_lat = request.data.get("center_lat")
        center_lon = request.data.get("center_lon")
        radius = request.data.get("radius")
        username = request.data.get("username")

        if not all([center_lat, center_lon, radius, username]):
            raise InvalidRequestException("Missing required parameters: center or radius or username")

        if not is_exists_username(username):
            save_username(username)
        else:
            del_all_from_buf_by_username(username)

        tourist_objects = get_tourist_objects(float(center_lon), float(center_lat), float(radius))
        save_tourist_object(tourist_objects, username)

        return Response(status=status.HTTP_201_CREATED)

