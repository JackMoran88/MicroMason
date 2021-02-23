from django_filters import rest_framework as filters, OrderingFilter
from product.models import *
from django.db.models import Q


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    context = ['price', 'sort_by']

    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')



    sort_by = OrderingFilter(
        fields=(
            ('name', 'name'),
            ('rating_avg', 'rating_avg'),
            ('price', 'price'),
        ),
    )

    count_cores = filters.CharFilter(method='get_filter_queryset')
    count_sims = filters.CharFilter(method='get_filter_queryset')
    brand = filters.CharFilter(method='get_filter_queryset')
    tip_noutbuka = filters.CharFilter(method='get_filter_queryset')





    def get_filter_queryset(self, queryset, name, value):
        options = OptionProduct.objects.filter(id__in=value.split(',')).values('name')
        option_names = []
        for i in options:
            option_names.append(i['name'])
        option_names = list(dict.fromkeys(option_names))
        return queryset.filter(options__parameter__request_name=name, options__name__in=option_names)


    class Meta:
        model = Product
        fields = ['price', 'sort_by', 'brand', 'min_price', 'max_price']

