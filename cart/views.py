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

from product.models import *
from product.serializers import *


class CartViewSet(viewsets.ViewSet):
    def list(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            products = Product.objects.all().filter(cartproduct__cart__customer_id=user.id)
            products = get_cart_annotate(products)
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            products = Product.objects.all().filter(cartproduct__cart__anonymous_customer=user.id)
            products = get_cart_annotate(products)
        else:
            return Response(status=400)

        serializer = CartDetailSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            if not (Cart.objects.filter(customer=user.id)):
                Cart.objects.create(customer=user)
            cart = Cart.objects.get(customer=user.id)
            data = {
                'cart': cart.id,
                'product': request.data.get('product'),
                'quantity': request.data.get('quantity'),
            }
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            if not (Cart.objects.filter(anonymous_customer=user.id)):
                Cart.objects.create(anonymous_customer=user)
            cart = Cart.objects.get(anonymous_customer=user.id)
            data = {
                'cart': cart.id,
                'product': request.data.get('product'),
                'quantity': request.data.get('quantity'),
            }
        else:
            return Response(status=400)

        item = CartAddSerializer(data=data)
        if item.is_valid(raise_exception=True):
            item.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        user = get_user(request)
        data = {
            'product_id': request.data.get('product')
        }
        if 'customer' in user.keys():
            user = user['customer']
            data['cart__customer_id'] = user.id
            if not (Cart.objects.filter(customer=user.id)):
                Cart.objects.create(customer=user)
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            data['cart__anonymous_customer_id'] = user.id
            if not (Cart.objects.filter(anonymous_customer=user.id)):
                Cart.objects.create(anonymous_customer=user)
        else:
            return Response(status=400)

        get_object_or_404(CartProduct, **data).delete()
        return Response(status=200)
