from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, viewsets

from .serializers import *
from .models import *
from shop_settings.models import *

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q, Case, CharField, QuerySet, \
    Subquery, Min, Max

from channels.layers import get_channel_layer
from mptt.templatetags.mptt_tags import cache_tree_children
from rest_framework.pagination import PageNumberPagination

import math


class PaginationProducts(PageNumberPagination):
    page_size = 2
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'paginate': {
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                },
                'count': self.page.paginator.count,
                'count_page': math.ceil(self.page.paginator.count / self.page_size),
                'current_page': self.page.number,
            },
            'results': data,
            # 'filters': {
            #     'price_spread': search_min_max_price(data),
            # },
        })


# def search_min_max_price(data):
#     prices = []
#     for item in data:
#         prices.append(item['price'])
#     result = [
#         int(min(prices)),
#         int(max(prices))
#     ]
#     return result


def sort_by_choice(request):
    if (request.data.get('sort_by')):
        sort_by = ProductSortType.objects.get(id=request.data.get('sort_by'))
    else:
        sort_by = ProductSortType.objects.get(order=1)
    return sort_by.field


def get_product_annotate(object):
    price_min = min(object.values_list('price', flat=True))
    price_max = max(object.values_list('price', flat=True))

    object = object.annotate(
        rating_avg=Avg("reviews__star__value", filter=Q(reviews__star__value__in=[1, 2, 3, 4, 5]),
                       output_field=FloatField()),
        count_reviews=Count("reviews", output_field=IntegerField()),
    )
    return object


def get_cart_annotate(object):
    object = object.annotate(
        totals=Sum(F('price') * F('cartproduct__quantity'), output_field=FloatField()),
        qty=Sum(F('cartproduct__quantity'))
    )
    return object


def check_404(object):
    if (object):
        return object
    else:
        return Response(status=404)


def get_image_crop(object):
    print(object)
    return 0


def get_user(request):
    if (request.headers.get('Authorization')):
        token = request.headers['Authorization'].replace('Token ', '')
        customer = Customer.objects.get(auth_token__key=token)
        return {'customer': customer}
    elif (request.data.get('anonymous')):
        anonymous = AnonymousCustomer.objects.get(id=request.data.get('anonymous'))
        return {'anonymous': anonymous}
    else:
        return {}
