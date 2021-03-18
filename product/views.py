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


class ProductPaginationGeneric(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductDetailSerializer
    pagination_class = PaginationProducts

    def get_queryset(self):
        if (self.request.data.get('slug')):
            parent_category = Category.objects.get(slug=self.request.data.get('slug'))
            category = parent_category.get_descendants(include_self=True)

            queryset = Product.objects.filter(category__in=category)
            queryset = queryset.annotate(parent_category=Value(parent_category, output_field=CharField()))
            queryset = get_product_annotate(queryset)
            return queryset


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
            ids = json.loads(request.data.get('ids'))
            products = Product.objects.filter(id__in=ids)
            products = get_product_annotate(products)
        else:
            products = Product.objects.filter(slug__in=request.data.get('slugs'))
            products = get_product_annotate(products)
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)

    def search_detail(self, request):

        if (request.data.get('query')):
            query = request.data.get('query')

            queryset = Product.objects.filter(name__icontains=query)
            queryset = get_product_annotate(queryset)

            page = self.paginate_queryset(queryset)
            serializer = ProductDetailSerializer(page, many=True)

            return self.get_paginated_response(serializer.data)
            # returnв Response(serializer.data)
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

    def last_added(self, request):
        count = 10
        if(request.GET.get('count')):
            count = int(request.GET.get('count'))
        products = Product.objects.all().filter(~Q(status=0)).order_by('-id')[:count]
        products = get_product_annotate(products)
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)
