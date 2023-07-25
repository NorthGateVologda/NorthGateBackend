"""Модуль содержит все сериализаторы системы"""
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Facility


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с сущностью Пользователь в системе"""
    class Meta:
        """Основные поля для сериализации"""
        model = User
        fields = ('username', 'password', 'token')

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, user):
        """Используется для подстановки токена при использовании текущего сериализатора"""
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        """Используется для сохранения пользователя в БД, если у него указан пароль"""
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance
        
class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ('address', 'x', 'y', 'numberOfInhabitants')