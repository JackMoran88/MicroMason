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
import re
from django.core.mail import send_mail


# Mailer
def mailer_send(subject, body, recipients):
    send_mail(subject, body, settings.EMAIL_HOST_USER, recipients, fail_silently=False)


def mailer_html_send(subject, body='', recipients='', html=''):
    send_mail(subject, body, settings.EMAIL_HOST_USER, recipients, fail_silently=False, html_message=html)

class PaginationProducts(PageNumberPagination):
    page_size = 24
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        """
        Переписанный клас, для обработки ошибки, которая появляется при фильтрации - страница не найдена
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except Exception as exc:
            try:
                self.page = paginator.page(1)
            except:
                msg = {
                    "code": 400,
                    "error": "Page out of range",
                }
                from rest_framework.exceptions import NotFound
                raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

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
        })

def clear_token(request):
    token = re.sub('^[\w]+ ', '', request.headers['Authorization'])
    return token

def sort_by_choice(request):
    if (request.data.get('sort_by')):
        sort_by = ProductSortType.objects.get(field=request.data.get('sort_by'))
    elif(request.GET.get('sort_by')):
        sort_by = ProductSortType.objects.get(field=request.GET.get('sort_by'))
    else:
        sort_by = ProductSortType.objects.get(order=1)
    return sort_by.field

def get_product_annotate(object):
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

def get_user(request):
    if (request.headers.get('Authorization')):
        token = clear_token(request)
        customer = Customer.objects.filter(auth_token__key=token).first()
        if not (customer):
            customer = Customer.objects.filter(oauth2_provider_accesstoken__token=token).first()
        return {'customer': customer}
    elif (request.data.get('anonymous')):
        anonymous = AnonymousCustomer.objects.get(token=request.data.get('anonymous'))
        return {'anonymous': anonymous}
    elif (request.GET.get('anonymous')):
        anonymous = AnonymousCustomer.objects.get(token=request.GET.get('anonymous'))
        return {'anonymous': anonymous}
    else:
        return {}
