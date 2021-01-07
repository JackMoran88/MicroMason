from django_filters import rest_framework as filters, OrderingFilter
from product.models import *



class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    context = ['price', 'sort_by']

    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    context.append(['min_price', 'max_price'])


    sort_by = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('rating_avg', 'rating_avg'),
            ('price', 'price'),
        ),
    )

    brand = CharFilterInFilter(field_name='brand__name', lookup_expr='in')



    class Meta:
        model = Product
        fields = ['price', 'sort_by', 'brand', 'min_price', 'max_price']
