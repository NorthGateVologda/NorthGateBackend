"""Модуль, содержащий основные пути к конечным точкам"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from api.views import (
    registration,
    logout
)

urlpatterns = [
    path('api/user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/user/registration/', registration, name='registration'),
    path('api/user/logout/', logout, name='logout'),
    path('api/user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
