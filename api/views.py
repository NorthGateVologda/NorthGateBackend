"""Модуль, содержащий основные точки доступа"""
import logging
from typing import Any
from typing import List

import geojson
import requests
from django.conf import settings as conf_settings
from django.contrib.gis.geos import Point
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ObjectTourism
from .serializers import UserSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def registration(request: Any) -> Response:
    """Метод, используемый для регистрации пользователя в системе и получения токена доступа"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

    return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request: Any) -> Response:
    """Метод, используемый для выхода из системы"""
    if request.data.get("all"):
        token: OutstandingToken
        for token in OutstandingToken.objects.filter(user=request.user):
            BlacklistedToken.objects.get_or_create(token=token)
        return Response({"data": "All tokens have been successfully removed from the system"},
                        status=status.HTTP_200_OK)
    refresh_token = request.data.get("refresh_token")
    token = RefreshToken(token=refresh_token)
    token.blacklist()
    return Response({"data": "The token was successfully removed from the system"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_coordinates(request: Any) -> Response:
    url = conf_settings.YANDEX_URL
    api_key = conf_settings.YANDEX_KEY

    geocode = request.GET.get("geocode", "")

    params = {
        "apikey": api_key,
        "geocode": geocode,
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()
        coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return Response(coordinates)
    else:
        return Response("Failed to get coordinates", status=response.status_code)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_location_name(request: Any) -> Response:
    url = conf_settings.YANDEX_URL
    api_key = conf_settings.YANDEX_KEY

    latitude = request.GET.get('lat', '')
    longitude = request.GET.get('lon', '')

    if not latitude or not longitude:
        return Response("Please provide both latitude and longitude parameters.", status=400)

    geocode_param = f"{longitude},{latitude}"
    params = {
        "apikey": api_key,
        "geocode": geocode_param,
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()
        location_name = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
        return Response(location_name)
    else:
        return Response("Failed to get location name", status=response.status_code)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_object_tourism(request) -> Response:
    if not request.data:
        return Response({"error": "Missing required body"}, status=status.HTTP_400_BAD_REQUEST)

    center_lat = request.data.get("center_lat")
    center_lon = request.data.get("center_lon")
    radius = request.data.get("radius")
    username = request.data.get("username")

    logging.info("center_lat=%s, center_lon=%s, radius=%s", center_lat, center_lon, radius)

    if not all([center_lat, center_lon, radius]):
        return Response({"error": "Missing required parameters: center or radius"}, status=status.HTTP_400_BAD_REQUEST)

    tourist_objects = get_tourist_objects(float(center_lon), float(center_lat), float(radius))

    features = []
    for obj in tourist_objects:
        # Формируем геометрию Point для GeoJSON
        geometry = {"type": "Point", "coordinates": [obj.x, obj.y]}

        # Создаем свойства объекта GeoJSON
        properties = {
            "id": obj.id,
            "name": obj.name,
            "city": obj.city,
            "street": obj.street,
            "house": obj.house,
            "post": obj.post,
        }

        # Создаем объект Feature для каждого объекта
        feature = geojson.Feature(geometry=geometry, properties=properties)

        features.append(feature)

    # Создаем FeatureCollection из всех объектов
    feature_collection = geojson.FeatureCollection(features)

    return Response(feature_collection)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_residential_hexagons(request: Any) -> Response:
    return Response(execute_query("fnc_get_hexagons_geoJson"))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_facilities(request: Any) -> Response:
    return Response(execute_query("fnc_get_facilities_geoJson"))


def execute_query(function: str) -> str:
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {function}()")
        geoJson = cursor.fetchone()[0]

    return geoJson


def get_tourist_objects(center_lon: float, center_lat: float, radius: float) -> List[ObjectTourism]:
    point = Point(center_lon, center_lat, srid=3857)
    logging.info("Точка сформирована: %s", point)
    circle = point.buffer(radius)
    logging.info("Окружность сформирована: %s", circle)
    return ObjectTourism.objects.filter(wkb_geometry__intersects=circle)