from django.urls import path
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorListCreateView, SensorRetrieveUpdateView, TemperatureMeasurementListCreateView, SensorTemperatureMeasurementListCreateView


urlpatterns = [
    path('sensors/', SensorListCreateView.as_view()),
    path('sensors/<pk>/', SensorRetrieveUpdateView.as_view()),
    path('measurements/', TemperatureMeasurementListCreateView.as_view()),
    path('measurements/', SensorTemperatureMeasurementListCreateView.as_view()),
]
