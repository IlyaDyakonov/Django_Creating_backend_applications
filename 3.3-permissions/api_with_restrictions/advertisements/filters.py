from django_filters import rest_framework as filters
from django_filters import DateFromToRangeFilter, FilterSet
from advertisements.models import Advertisement


class AdvertisementFilter(FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = DateFromToRangeFilter()
    status = filters.CharFilter(field_name='status')
    creator = filters.NumberFilter(field_name='creator_id')


    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator',]