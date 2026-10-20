import django_filters
from .models import Phone,  Accessory
import django_filters

class AccessoryFilter(django_filters.FilterSet):
    accessory_type = django_filters.CharFilter(field_name='accessory_type', lookup_expr='exact')

    class Meta:
        model = Accessory
        fields = ['accessory_type']

class PhonePriceFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Phone
        fields = ['min_price', 'max_price']

class PhoneFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte') # >=
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte') # <=

    class Meta:
        model = Phone
        fields = ['brand', 'color', 'min_price', 'max_price']