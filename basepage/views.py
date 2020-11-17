from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions

from .serializers import *
from .models import *

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


class AuthCheck(APIView):
    # Проверка токена
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response()


class DetailCustomerView(APIView):
    def post(self, request):
        if (request.headers.get('Authorization')):
            token = request.headers['Authorization'].replace('Token ', '')
            customer = Customer.objects.get(auth_token__key=token)
            if (request.data.get('anonymous')):
                anonymous_token = request.data.get('anonymous')
                try:
                    cart = Cart.objects.get(anonymous_customer=anonymous_token)
                    if not (Cart.objects.filter(customer=customer.id)):
                        cart.customer = customer
                        cart.anonymous_customer = None
                        cart.save()
                        customer.save()  # ДА ДА ДА. ОТета ебота.
                    else:
                        cart.delete()
                    AnonymousCustomer.objects.filter(id=anonymous_token).delete()
                except:
                    pass
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


class ProductsDetailView(APIView):
    # Просмотр товаров
    def post(self, request):
        if request.data.get('ids'):
            ids = request.data.get('ids')
            products = Product.objects.filter(id__in=ids)
        else:
            products = Product.objects.annotate(
                rating_avg=Avg("ratings__star")
            ).filter(slug__in=request.data.get('slugs'))

        serializer = ProductDetailSerializer(products, many=True)
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

    def post(self, request):
        author = Customer.objects.get(id=request.data.get('author'))
        star = RatingStar.objects.get(value=request.data.get('star'))
        data = {
            'star': star.id,
            'product': request.data.get('product'),
            'author': author.id,
            'text': request.data.get('text'),
            'advantages': request.data.get('advantages'),
            'disadvantages': request.data.get('disadvantages'),
        }
        rating = RatingCreateSerializer(data=data)
        if rating.is_valid(raise_exception=True):
            rating.save()
            return Response(status=201)


class DeleteRatingView(APIView):
    def post(self, request):
        # Только авторизированный
        comment_id = request.data.get('comment')
        author_id = request.data.get('author')
        Rating.objects.all().filter(id=comment_id, author_id=author_id).delete()
        return Response(status=200)


class DetailProductReviews(APIView):

    def post(self, request):
        if (request.data.get('id')):
            reviews = Rating.objects.all().filter(
                product=request.data.get('id')
            ).annotate(customer=Sum(F("author_id"), output_field=IntegerField()))
            serializer = RatingDetailSerializer(reviews, many=True)
            return Response(serializer.data)
        return Response(status=400)


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
        if (request.data.get('first_name') and request.data.get('last_name')):
            customer.first_name = request.data.get('first_name')
            customer.last_name = request.data.get('last_name')
            customer.save()
            return Response(status=200)
        return Response(status=400)


class AnonymousCustomerCreateView(APIView):

    def post(self, request):
        anonymous = AnonymousCustomerCreateSerializer(data=request.data)
        if anonymous.is_valid():
            anonymous.save()
            return Response(anonymous.data)
        else:
            return Response(status=400)


class AddCartView(APIView):
    # Добавление товара в корзину
    def post(self, request):
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


class DeleteCartView(APIView):
    # Добавление товара в корзину
    def post(self, request):
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


class CartProductsDetailView(APIView):
    def post(self, request):
        if (request.headers.get('Authorization')):
            token = request.headers['Authorization'].replace('Token ', '')
            customer = Customer.objects.get(auth_token__key=token)
            # products = CartProduct.objects.all().filter(cart__customer_id=customer.id).annotate(
            #     totals=Sum(F('product__price') * F('quantity'), output_field=FloatField()))
            products = Product.objects.all().filter(cartproduct__cart__customer_id=customer.id).annotate(
                totals=Sum(F('price') * F('cartproduct__quantity'), output_field=FloatField()),
                qty=Sum(F('cartproduct__quantity')))
            print(products)
            serializer = CartDetailSerializer(products, many=True)
            return Response(serializer.data)
        elif (request.data.get('anonymous')):
            # Если пользователь - Аноним
            print('anonymous anonymous anonymous anonymous ')
            anonymous = AnonymousCustomer.objects.get(id=request.data.get('anonymous'))
            products = Product.objects.all().filter(cartproduct__cart__anonymous_customer=anonymous.id).annotate(
                totals=Sum(F('price') * F('cartproduct__quantity'), output_field=FloatField()),
                qty=Sum(F('cartproduct__quantity')))
            print(products)
            serializer = CartDetailSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response(status=400)


#
#
#
#
#
#
#
#
#
#
#

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
