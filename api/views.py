"""Модуль, содержащий основные точки доступа"""
from typing import Any
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

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
