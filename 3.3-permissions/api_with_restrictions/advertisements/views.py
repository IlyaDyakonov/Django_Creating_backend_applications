from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from django_filters import rest_framework as django_filters
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import IsOwnerOrReadOnly

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [django_filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "delete"]:
            return [IsAuthenticated()]
        return []

    def perform_destroy(self, instance):
        """
        Переопределенный метод для удаления объявления.
        Удалять объявление может только его автор.
        """
        user = self.request.user

        if instance.creator != user:
            raise serializers.ValidationError("Вы не являетесь автором этого объявления.")

        instance.delete()