from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, viewsets, mixins

from .serializers import *
from .models import *
from shop_settings.models import *

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q, Case, CharField

from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from mptt.templatetags.mptt_tags import cache_tree_children
import json

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page



class ProductViewSet(viewsets.GenericViewSet):
    pagination_class = PaginationProducts

    def retrieve(self, request):
        if request.data.get('id'):
            product = Product.objects.all()
            product = get_product_annotate(product)
            product = get_object_or_404(product, id=request.data.get('id'))
        else:
            product = Product.objects.all()
            product = get_product_annotate(product)
            product = get_object_or_404(product, slug=request.data.get('slug'))

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def list(self, request):
        if request.data.get('ids'):
            # Array str to array
            ids = request.data.get('ids')
            if not isinstance(ids, list):
                ids = json.loads(request.data.get('ids'))
            products = Product.objects.filter(id__in=ids)
            products = get_product_annotate(products)
        else:
            products = Product.objects.filter(slug__in=request.data.get('slugs'))
            products = get_product_annotate(products)
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)

    def search_detail(self, request):

        if (request.GET.get('query')):
            query = request.GET.get('query')

            queryset = Product.objects.filter(name__icontains=query)
            queryset = get_product_annotate(queryset)

            page = self.paginate_queryset(queryset)
            serializer = ProductDetailSerializer(page, many=True)

            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=400)

    def search_list(self, request):

        if (request.data.get('query')):
            query = request.data.get('query')

            products = Product.objects.filter(name__icontains=query)
            products = products[:5]

            serializer = ProductSearchListSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response(status=400)

    @method_decorator(cache_page(60 * 60 * 2))
    def querysets(self, request):
        if (request.GET.get('type')):
            type = request.GET.get('type')

            count = 10
            if (request.GET.get('count')):
                count = int(request.GET.get('count'))

            if type == 'last':
                products = Product.objects.filter(~Q(status=0)).order_by('-id')[:count]
                products = get_product_annotate(products)
                serializer = smProductDetailSerializer(products, many=True)
                return Response(serializer.data)

            if type == 'popular':
                products = Product.objects.filter(~Q(status=0))
                products = get_product_annotate(products).order_by('rating_avg')[:count]
                serializer = smProductDetailSerializer(products, many=True)
                return Response(serializer.data)

            if type == 'popular_from_category':
                products = Product.objects.filter(~Q(status=0), category_id=request.GET.get('id'))
                products = get_product_annotate(products).order_by('rating_avg')[:count]
                serializer = smProductDetailSerializer(products, many=True)
                return Response(serializer.data)

            if type == 'popular_wish':
                favorite_wish = Wish.objects.all().values('product_id').annotate(total=Count('product_id')).order_by(
                    '-total').values_list('product_id', flat=True)
                products = Product.objects.filter(~Q(status=0), id__in=favorite_wish)
                products = get_product_annotate(products).order_by('rating_avg')[:count]
                serializer = smProductDetailSerializer(products, many=True)
                return Response(serializer.data)
