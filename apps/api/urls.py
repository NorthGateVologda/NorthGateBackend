from django.urls import path

from apps.api.views import ObjectTourismView

urlpatterns = [
    path('object_tourism', ObjectTourismView.as_view(), name='object_tourism')
]