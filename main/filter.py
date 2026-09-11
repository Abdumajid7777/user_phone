import django_filters
from .models import Phone,  Accessory
import django_filters

class AccessoryFilter(django_filters.FilterSet):
    accessory_type = django_filters.CharFilter(field_name='accessory_type', lookup_expr='exact')

    class Meta:
        model = Accessory
        fields = ['accessory_type']


# class AccessoryFilter(django_filters.FilterSet):
#     min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
#     max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

#     class Meta:
#         model = Accessory
#         fields = ['accessory_type', 'phone', 'min_price', 'max_price']


class PhoneFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(
        field_name='reviews__rating', lookup_expr='gte'
    )

    class Meta:
        model = Phone
        fields = [
            'brand', 'color', 'condition', 'memory', 
            'battery', 'internet', 'diagonal', 'created_at'
        ]






































# import django_filters
# from .models import Phone, Accessory

# class AccessoryFilter(django_filters.FilterSet):
#     min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
#     max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

#     class Meta:
#         model = Accessory
#         fields = ['accessory_type', 'phone', 'brand', 'min_price', 'max_price']

# class PhoneFilter(django_filters.FilterSet):
#     min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
#     max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

#     class Meta:
#         model = Phone
#         fields = [
#             'brand', 
#             'color', 
#             'condition', 
#             'memory', 
#             'battery', 
#             'internet', 
#             'diagonal', 
#             'created_at'
#         ]


