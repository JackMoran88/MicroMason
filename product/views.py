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




class ProductPaginationGeneric(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductDetailSerializer
    pagination_class = PaginationProducts

    def get_queryset(self):
        if (self.request.data.get('slug')):
            parent_category = Category.objects.get(slug=self.request.data.get('slug'))
            category = parent_category.get_descendants(include_self=True)

            queryset = Product.objects.filter(category__in=category)
            queryset = queryset.annotate(parent_category=Value(parent_category, output_field=CharField()))
            queryset = get_product_annotate(queryset).order_by(sort_by_choice(self.request))
            return queryset



class ProductViewSet(viewsets.GenericViewSet):
    pagination_class = PaginationProducts

    def retrieve(self, request):
        if request.data.get('id'):
            product = Product.objects.all()
            product = get_product_annotate(product)
            # product = product.get(id=request.data.get('id'))
            product = get_object_or_404(product, id=request.data.get('id'))
        else:
            product = Product.objects.all()
            product = get_product_annotate(product)
            # product = product.get(slug=request.data.get('slug'))
            product = get_object_or_404(product, slug=request.data.get('slug'))

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def list(self, request):
        if request.data.get('ids'):
            ids = request.data.get('ids')
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
            queryset = queryset.order_by(sort_by_choice(request))

            page = self.paginate_queryset(queryset)
            serializer = ProductDetailSerializer(page, many=True)

            return self.get_paginated_response(serializer.data)
            # return Response(serializer.data)
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


