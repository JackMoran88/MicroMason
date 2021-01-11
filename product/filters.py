from django_filters import rest_framework as filters, OrderingFilter
from product.models import *
from django.db.models import Q


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass



class ProductFilter(filters.FilterSet):
    context = ['price', 'sort_by']

    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    brand = CharFilterInFilter(field_name='brand__id', lookup_expr='in')


    sort_by = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('rating_avg', 'rating_avg'),
            ('price', 'price'),
        ),
    )

    count_cores = filters.CharFilter(method='get_filter_queryset')
    count_sims = filters.CharFilter(method='get_filter_queryset')


    def get_filter_queryset(self, queryset, name, value):
        return queryset.filter(options__parameter__request_name=name, options__id__in=value.split(','))


    class Meta:
        model = Product
        fields = ['price', 'sort_by', 'brand', 'min_price', 'max_price']

