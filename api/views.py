"""Модуль, содержащий основные точки доступа"""
import os
import requests
import h3
import pandas as pd
import geojson
import logging
from typing import Any
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings as conf_settings
from .serializers import UserSerializer, FacilitySerializer
from .models import Facility, ObjectTourism
from pyproj import Transformer
from typing import Tuple, List
from django.contrib.gis.geos import Point

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
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_residential_hexagons(request: Any) -> Response:
    # Получение данных из модели Django и преобразование их в DataFrame
    houses = Facility.objects.all()
    
    logging.info('Обьекты: %s', houses)
    
    house_data = [{'x': house.x, 'y': house.y, 'population': house.number_of_inhabitants} for house in houses]
    df = pd.DataFrame(house_data)

    # Размер гексагона (в метрах) - можно изменить в зависимости от нужной плотности гексагонов
    hex_size = 500  # Примерный размер гексагона в метрах

    # Преобразование координат в индексы гексагонов
    df['h3_index'] = df.apply(lambda row: h3.geo_to_h3(row['y'], row['x'], 9), axis=1)
    
    df['population'] = df['population'].astype(float)

    # Группировка по индексам гексагонов и суммирование населения в каждом гексагоне
    hex_population = df.groupby('h3_index')['population'].sum().reset_index()
    
    logging.info('Обьекты: %s', hex_population)

    # Создание GeoJSON объекта для гексагонов
    features = []
    for h3_index, population in zip(hex_population['h3_index'], hex_population['population']):
        coords = h3.h3_to_geo_boundary(h3_index)
        polygon = geojson.Polygon([coords])
        properties = {'population': population}
        feature = geojson.Feature(geometry=polygon, properties=properties)
        features.append(feature)

    feature_collection = geojson.FeatureCollection(features)

    return Response(feature_collection)

@api_view(["POST"])
@permission_classes([AllowAny])
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

def get_tourist_objects(center_lon: float, center_lat: float,  radius: float) -> List[ObjectTourism]:
    point = Point(center_lon, center_lat, srid=3857)
    logging.info("Точка сформирована: %s", point)
    circle = point.buffer(radius)
    logging.info("Окружность сформирована: %s", circle)
    found_tourist_objects = ObjectTourism.objects.filter(wkb_geometry__intersects=circle)
    return found_tourist_objects