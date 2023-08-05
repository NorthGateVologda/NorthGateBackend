"""Модуль, содержащий основные пути к конечным точкам"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from api.views import (
    registration,
    logout,
    get_coordinates,
    get_location_name,
    get_residential_hexagons,
    get_object_tourism,
    get_facilities
)

urlpatterns = [
    path('api/user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/user/registration/', registration, name='registration'),
    path('api/user/logout/', logout, name='logout'),
    path('api/user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/get_coordinates/', get_coordinates, name='get_coordinates'),
    path('api/get_location_name/', get_location_name, name='get_location_name'),
    path('api/get_residential_hexagons/', get_residential_hexagons, name='get_residential_hexagons'),
    path('api/get_object_tourism/', get_object_tourism, name='get_object_tourism'),
    path('api/get_facilities/', get_facilities, name='get_facilities'),
]