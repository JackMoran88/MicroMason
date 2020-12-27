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
        if (request.headers.get('Authorization')):
            token = request.headers['Authorization'].replace('Token ', '')
            customer = Customer.objects.get(auth_token__key=token)

            products = Product.objects.all().filter(cartproduct__cart__customer_id=customer.id)
            products = get_cart_annotate(products)

            serializer = CartDetailSerializer(products, many=True)
            return Response(serializer.data)
        elif (request.data.get('anonymous')):
            # Если пользователь - Аноним
            anonymous = AnonymousCustomer.objects.get(id=request.data.get('anonymous'))

            products = Product.objects.all().filter(cartproduct__cart__anonymous_customer=anonymous.id)
            products = get_cart_annotate(products)

            serializer = CartDetailSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response(status=400)

    def create(self, request):
        if (request.headers.get('Authorization')):
            # Если пользователь авторизирован
            token = request.headers['Authorization'].replace('Token ', '')
            customer = Customer.objects.get(auth_token__key=token)
            if not (Cart.objects.filter(customer=customer.id)):
                Cart.objects.create(customer=customer)
            cart = Cart.objects.get(customer=customer.id)
            data = {
                'cart': cart.id,
                'product': request.data.get('product'),
                'quantity': request.data.get('quantity'),
            }
            product = CartAddSerializer(data=data)
            if product.is_valid(raise_exception=True):
                product.save()
                return Response(status=201)
            else:
                return Response(status=400)
        elif (request.data.get('anonymous')):
            # Если пользователь - Аноним
            anonymous = AnonymousCustomer.objects.get(id=request.data.get('anonymous'))
            if not (Cart.objects.filter(anonymous_customer=anonymous.id)):
                Cart.objects.create(anonymous_customer=anonymous)
            cart = Cart.objects.get(anonymous_customer=anonymous.id)
            data = {
                'cart': cart.id,
                'product': request.data.get('product'),
                'quantity': request.data.get('quantity'),
            }
            product = CartAddSerializer(data=data)
            if product.is_valid(raise_exception=True):
                product.save()
                return Response(status=201)
            else:
                return Response(status=400)
        else:
            return Response(status=400)

    def delete(self, request):
        if (request.headers.get('Authorization')):
            # Если пользователь авторизирован
            token = request.headers['Authorization'].replace('Token ', '')
            customer = Customer.objects.get(auth_token__key=token)
            if not (Cart.objects.filter(customer=customer.id)):
                Cart.objects.create(customer=customer)
            CartProduct.objects.get(
                cart__customer_id=customer.id,
                product_id=request.data.get('product')
            ).delete()
            return Response(status=200)
        elif (request.data.get('anonymous')):
            # Если пользователь - Аноним
            anonymous = AnonymousCustomer.objects.get(id=request.data.get('anonymous'))
            if not (Cart.objects.filter(anonymous_customer=anonymous.id)):
                Cart.objects.create(anonymous_customer=anonymous)
            CartProduct.objects.get(
                cart__anonymous_customer_id=anonymous,
                product_id=request.data.get('product')
            ).delete()
            return Response(status=200)
        else:
            return Response(status=400)