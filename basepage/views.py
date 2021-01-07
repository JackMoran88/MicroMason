from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, viewsets, mixins

from .serializers import *
from .models import *
from shop_settings.models import *

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q, Case, CharField, Subquery, \
    OuterRef, JSONField, QuerySet, FilteredRelation

from django.shortcuts import get_object_or_404
from channels.layers import get_channel_layer
from mptt.templatetags.mptt_tags import cache_tree_children

from .service import *

from product.models import *
from product.serializers import *

from category.models import *

from django_filters import rest_framework as filters
from product.filters import *

from django.http import JsonResponse
from django.core import serializers as CoreSerializer

from django.db.models import Q


class CategoryViewSet(viewsets.GenericViewSet):
    pagination_class = PaginationProducts
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def list(self, request):
        queryset = cache_tree_children(Category.objects.all().order_by('id'))
        serializer = CategoriesListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request):
        response = {
            'filters': {}
        }

        if (request.data.get('slug')):
            categories = Category.objects.all().filter(slug=request.data.get('slug')).get_descendants(
                include_self=True).values_list('slug', flat=True)

            products = Product.objects.filter(category__slug__in=categories)
            cur_category = Category.objects.all().filter(slug=request.data.get('slug')).values()

            prices = products.values_list('price', flat=True)
            # brands = Brand.objects.filter(product__in=products).values()

            f = Filter.objects.all().values().filter(category__slug=request.data.get('slug'))


            for item in f:
                filter = eval(item['model']).objects.filter(
                    Q(**{item['query']: eval(item['parameter'])})).values()

                if filter:
                    response['filters'][item['request_name']] = list(filter)



            if cur_category:
                response['category'] = list(cur_category)
            if prices:
                response['filters']['prices'] = list((min(prices), max(prices)))
            # if brands:
            #     response['filters']['brands'] = list(brands)

            return JsonResponse(response)

    def detail_products(self, request):
        if (request.data.get('slug')):
            parent_category = get_object_or_404(Category, slug=request.data.get('slug'))
            category = parent_category.get_descendants(include_self=True)

            queryset = Product.objects.filter(category__in=category)
            queryset = queryset.annotate(parent_category=Value(parent_category, output_field=CharField()))
            queryset = get_product_annotate(queryset).order_by(sort_by_choice(request))

            queryset = self.filter_queryset(queryset)
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
        Review.objects.filter(id=comment_id, author_id=author_id).delete()
        return Response(status=200)

    def list(self, request):
        if (request.data.get('id')):
            reviews = Review.objects.all().filter(
                product=request.data.get('id')
            )
            serializer = ReviewDetailSerializer(reviews, many=True)
            return Response(serializer.data)
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
                    cart = basepage.models.Cart.objects.get(anonymous_customer=anonymous_token)
                    if not (basepage.models.Cart.objects.filter(customer=customer.id)):
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
