from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions

from .serializers import *
from .models import *

from django.db.models import Sum, F, FloatField, Avg

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def index(request):
    return render(request, 'basepage/index.html', {})


def room(request, room_name):
    print(room_name)
    return render(request, 'basepage/test.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


class AuthCheck(APIView):
    # Проверка токена
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response()


class DetailCustomerView(APIView):
    def post(self, request):
        if (request.data.get('token')):
            customer = Customer.objects.get(auth_token__key=request.data.get('token'))
            serializer = DetailCustomerSerializer(customer)
            return Response(serializer.data)
        else:
            return Response(status=400)


class CategoriesListView(APIView):
    # permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated
    # Все категории
    def post(self, request):
        categories = Category.objects.all().filter(parent__isnull=True)
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailView(APIView):
    # Просмотр определенной категории
    def post(self, request, slug):
        category = Product.objects.filter(category__slug=slug).annotate(
            rating_avg=Avg("ratings__star"),
        )
        serializer = CategoryDetailSerializer(category, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    # Просмотр товара
    def post(self, request):
        if request.data.get('id'):
            product = Product.objects.annotate(
                rating_avg=Avg("ratings__star")
            ).get(id=request.data.get('id'))
        else:
            product = Product.objects.annotate(
                rating_avg=Avg("ratings__star")
            ).get(slug=request.data.get('slug'))

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    # Создание отзыва
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
            return Response(status=201)
        else:
            return Response(status=400)


class AddRatingView(APIView):
    # Добавление рейтинга фильму

    def post(self, request):
        rating = RatingCreateSerializer(data=request.data)
        if rating.is_valid():
            rating.save()
            return Response(status=201)
        else:
            return Response(status=400)


class AddCartView(APIView):
    # Добавление товара в корзину
    def post(self, request):
        print(request.data)
        product = CartAddSerializer(data=request.data)
        if product.is_valid():
            product.save()
            return Response(status=201)
        else:
            return Response(status=400)


class AnonymousCustomerCreateView(APIView):

    def post(self, request):
        anonymous = AnonymousCustomerCreateSerializer(data=request.data)
        if anonymous.is_valid():
            anonymous.save()
            return Response(anonymous.data)
        else:
            return Response(status=400)


class CartDetailView(APIView):

    def post(self, request):
        products = CartProduct.objects.all().filter(cart=request.data.get('id')).annotate(
            totals=Sum(F('product__price') * F('quantity'), output_field=FloatField()))

        serializer = CartDetailSerializer(products, many=True)
        return Response(serializer.data)


class AddWishView(APIView):

    def post(self, request):
        wishProduct = AddWishSerializer(data=request.data)
        if wishProduct.is_valid():
            wishProduct.save()
            return Response(status=201)
        else:
            return Response(status=400)


class DeleteWishView(APIView):

    def post(self, request):
        Wish.objects.get(
            customer=request.data.get('customer'),
            product=request.data.get('product'),
        ).delete()
        return Response(status=204)


class DetailWishView(APIView):
    def post(self, request):
        customer = Customer.objects.get(auth_token__key=request.data.get('token'))
        products = Product.objects.all().filter(product__customer=customer).annotate(
            rating_avg=Avg("ratings__star"),
        )
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)


class SetCustomerFullName(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        token = request.headers['Authorization'].replace('Token ', '')
        customer = Customer.objects.get(auth_token__key=token)
        if(request.data.get('first_name') and request.data.get('last_name')):
            customer.first_name = request.data.get('first_name')
            customer.last_name = request.data.get('last_name')
            customer.save()
            return Response(status=200)
        return Response(status=400)









from channels.layers import get_channel_layer


async def update_product(product):
    print('\t update_product update_product update_product update_product update_product ')
    group_name = ProductDetailSerializer(product).get_group_name()
    channel_layer = get_channel_layer()

    content = {
        "type": "UPDATE_PRODUCT",
        "payload": product.id,
    }
    await channel_layer.group_send(group_name, {
        "type": "notify",
        "content": content,
    })


async def update_categories(category):
    print('\t update_categories update_categories update_categories update_categories ')
    group_name = CategoryListSerializer().get_group_name()
    channel_layer = get_channel_layer()

    content = {
        "type": "UPDATE_PRODUCT",
        "payload": category.id,
    }
    await channel_layer.group_send(group_name, {
        "type": "notify",
        "content": content,
    })
