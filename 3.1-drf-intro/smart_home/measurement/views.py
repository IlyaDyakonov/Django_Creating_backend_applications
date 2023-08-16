# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework import generics
from .models import  Sensor, Measurement
from .serializers import MeasurementSerializer, SensorDetailSerializer, MeasurementSerializerCreate


class SensorListCreateView(generics.ListCreateAPIView):
    """Создание датчиков и просмотр"""
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

class SensorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Получение и обновление информации о датчике"""
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

class TemperatureMeasurementListCreateView(generics.ListCreateAPIView):
    """Создание и просмотр списка изменений температуры"""
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        sensor_pk = self.kwargs.get('sensor_pk')
        if sensor_pk:
            return Measurement.objects.filter(sensor_id=sensor_pk)
        return Measurement.objects.all()

class SensorTemperatureMeasurementListCreateView(generics.ListCreateAPIView):
    """Создание и просмотр списка изменений температуры для конкретного датчика"""
    serializer_class = MeasurementSerializerCreate

    def get_queryset(self):
        sensor_pk = self.kwargs.get('sensor_pk')
        return Measurement.objects.filter(sensor_id=sensor_pk)

    def perform_create(self, serializer):
        sensor_pk = self.kwargs.get('sensor_pk')
        sensor = Sensor.objects.get(pk=sensor_pk)
        serializer.save(sensor=sensor)
