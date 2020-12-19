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

from .service import *


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


class CategoryViewSet(viewsets.GenericViewSet):
    pagination_class = PaginationProducts

    def list(self, request):
        queryset = cache_tree_children(Category.objects.all().order_by('id'))
        serializer = CategoriesListSerializer(queryset, many=True)
        return Response(serializer.data)

    def details(self, request):
        if (request.data.get('slug')):
            parent_category = get_object_or_404(Category, slug=request.data.get('slug'))
            category = parent_category.get_descendants(include_self=True)

            queryset = Product.objects.filter(category__in=category)
            queryset = queryset.annotate(parent_category=Value(parent_category, output_field=CharField()))
            queryset = get_product_annotate(queryset).order_by(sort_by_choice(request))

            page = self.paginate_queryset(queryset)

            serializer = ProductDetailSerializer(page, many=True)
            # return Response(serializer.data)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=400)

    def search_list(self, request):
        if (request.data.get('query')):
            query = request.data.get('query')

            queryset = Category.objects.filter(name__icontains=query)
            queryset = queryset[:5]

            serializer = CategorySearchListSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=400)


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


class WishViewSet(viewsets.ViewSet):

    def list(self, request):
        customer = Customer.objects.get(auth_token__key=request.data.get('token'))

        queryset = Product.objects.all().filter(product__customer=customer)
        queryset = get_product_annotate(queryset)

        serializer = ProductDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        wishProduct = WishAddSerializer(data=request.data)
        if wishProduct.is_valid():
            wishProduct.save()
            return Response(status=201)
        else:
            return Response(status=400)

    def delete(self, request):
        Wish.objects.get(
            customer=request.data.get('customer'),
            product=request.data.get('product'),
        ).delete()
        return Response(status=204)


class ReviewViewSet(viewsets.ViewSet):

    def create(self, request):
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
        review = ReviewCreateSerializer(data=data)
        if review.is_valid(raise_exception=True):
            review.save()
            return Response(status=201)

    def answer(self, request):
        author = Customer.objects.get(id=request.data.get('author'))
        parent = Review.objects.get(id=request.data.get('parent'))
        star = RatingStar.objects.get(value=0)
        data = {
            'product': request.data.get('product'),
            'author': author.id,
            'text': request.data.get('text'),
            'parent': parent.id,
            'star': star.id,
        }
        review = ReviewAnswerCreateSerializer(data=data)
        if review.is_valid(raise_exception=True):
            review.save()
            return Response(status=201)

    def delete(self, request):
        # Только авторизированный
        comment_id = request.data.get('comment')
        author_id = request.data.get('author')
        Review.objects.all().filter(id=comment_id, author_id=author_id).delete()
        return Response(status=200)

    def list(self, request):
        if (request.data.get('id')):
            reviews = Review.objects.all().filter(
                product=request.data.get('id')
            )
            serializer = ReviewDetailSerializer(reviews, many=True)
            return Response(serializer.data)
        return Response(status=400)


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


class CustomerViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def check(self, request):
        return Response()

    def retrieve(self, request):
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
            serializer = CustomerDetailSerializer(customer)
            return Response(serializer.data)
        else:
            return Response(status=400)

    def change(self, request):
        token = request.headers['Authorization'].replace('Token ', '')
        customer = Customer.objects.get(auth_token__key=token)
        if (customer):
            if (request.data.get('first_name')):
                customer.first_name = request.data.get('first_name')
            if (request.data.get('last_name')):
                customer.last_name = request.data.get('last_name')
            if (request.data.get('email')):
                customer.email = request.data.get('email')
            if (request.data.get('phone')):
                customer.phone_number = request.data.get('phone')
            customer.save()
            return Response(status=200)
        else:
            return Response(status=400)


class AnonymousViewSet(viewsets.ViewSet):
    def create(self, request):
        anonymous = AnonymousCustomerCreateSerializer(data=request.data)
        if anonymous.is_valid():
            anonymous.save()
            return Response(anonymous.data)
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

async def update_product(product):
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
    group_name = CategoriesListSerializer().get_group_name()
    channel_layer = get_channel_layer()

    content = {
        "type": "UPDATE_PRODUCT",
        "payload": category.id,
    }
    await channel_layer.group_send(group_name, {
        "type": "notify",
        "content": content,
    })
