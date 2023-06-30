from django.urls import path
from .views import something
urlpatterns = [
    path('', something),
]
