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
from cart.models import *

from django_filters import rest_framework as filters
from product.filters import *

from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers as CoreSerializer

from model_search import model_search
from _novaposhta.models import Warehouse

from .tasks import send_email
from django.conf import settings
import requests
from django.conf import settings
from oauth2_provider.models import Application


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

            filters_of_category = Filter.objects.all().values().filter(category__slug=request.data.get('slug'), state=1)

            def rename_key(arr):
                for dict in arr:
                    if 'options__name' in dict:
                        dict['name'] = dict['options__name']
                        del dict['options__name']
                    if 'options__id' in dict:
                        dict['id'] = dict['options__id']
                        del dict['options__id']

            def get_prices():
                prices = products.values_list('price', flat=True)
                if prices:
                    min_max = [min(prices), max(prices)]
                else:
                    min_max = [0, 0]
                response['filters']['prices'] = min_max

            def remove_dublicates(arr):
                # `return [dict(t) for t in {tuple(d.items()) for d in arr}]`
                done = set()
                result = []
                for d in arr:
                    if d['name'] not in done:
                        done.add(d['name'])  # note it down for further iterations
                        result.append(d)
                return result

            for filter_of_category in filters_of_category:
                if filter_of_category['request_name'] == 'prices':
                    get_prices()

                if filter_of_category['model']:
                    filter = eval(filter_of_category['model']).objects.all()
                    if filter_of_category['model_parameter_id']:
                        filter = Option.objects.filter(id=filter_of_category['model_parameter_id'])
                    elif filter_of_category['filter']:
                        filter = filter.filter(**eval(filter_of_category['filter']))

                    if filter_of_category['output']:
                        filter = filter.values(f'{filter_of_category["output"]}')
                    else:
                        filter = filter.values()

                    filter = list(filter)

                    if filter_of_category['sub_model']:
                        choices = eval(filter_of_category['sub_model']).objects.all()
                        if filter_of_category['model_parameter_id']:
                            choices = choices.filter(options__parameter_id=filter_of_category['model_parameter_id'],
                                                     category_id=cur_category[0]['id'])
                        elif filter_of_category['sub_filter']:
                            choices = choices.filter(
                                **eval(filter_of_category['sub_filter']))
                        if filter_of_category['sub_output']:
                            choices = choices.values(eval(filter_of_category['sub_output']))
                        else:
                            try:
                                choices = list(choices.values('options__id', 'options__name'))
                            except:
                                choices = choices.values()
                        choices = list(choices)
                        rename_key(choices)
                        choices = remove_dublicates(choices)

                        for num, choice in enumerate(choices):
                            if choice['name'].strip() == "":
                                choices.pop(num)

                        filter.append({'choices': choices})

                    if filter:
                        response['filters'][filter_of_category['request_name']] = list(filter)

            if cur_category:
                response['category'] = list(cur_category)
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

            serializer = smProductDetailSerializer(page, many=True)

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
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            queryset = Product.objects.all().filter(product__customer=user)
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            queryset = Product.objects.all().filter(product__anonymous_customer=user)

        queryset = get_product_annotate(queryset)
        serializer = smProductDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            data = {
                'customer': get_object_or_404(Customer, id=user.id),
                'product': get_object_or_404(Product, id=request.data.get('product')),
            }
            data['defaults'] = {
                'product': data.get("product"),
                'customer': data.get('customer'),
            }
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            data = {
                'anonymous_customer': get_object_or_404(AnonymousCustomer, id=user.id),
                'product': get_object_or_404(Product, id=request.data.get('product')),
            }
            data['defaults'] = {
                'product': data.get("product"),
                'anonymous_customer': data.get('anonymous_customer'),
            }
        else:
            return Response(status=400)

        Wish.objects.update_or_create(**data)
        return Response(status=201)

    def delete(self, request):
        user = get_user(request)
        data = {
            'product': request.data.get('product'),
        }
        if 'customer' in user.keys():
            user = user['customer']
            data['customer'] = user
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            data['anonymous_customer'] = user
        else:
            return Response(status=400)
        Wish.objects.get(**data).delete()
        return Response(status=204)


class CompareViewSet(viewsets.ViewSet):

    def list(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            queryset = Compare.objects.all().filter(customer=user)
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            queryset = Compare.objects.all().filter(anonymous_customer=user)

        serializer = CompareDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            data = {
                'customer': get_object_or_404(Customer, id=user.id),
                'product': get_object_or_404(Product, id=request.data.get('product')),
                'category': get_object_or_404(Product, id=request.data.get('product')).category,
            }
            data['defaults'] = {
                'product': data.get("product"),
                'customer': data.get('customer'),
                'category': data.get('category'),
            }
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            data = {
                'anonymous_customer': get_object_or_404(AnonymousCustomer, id=user.id),
                'product': get_object_or_404(Product, id=request.data.get('product')),
                'category': get_object_or_404(Product, id=request.data.get('product')).category,
            }
            data['defaults'] = {
                'product': data.get("product"),
                'anonymous_customer': data.get('anonymous_customer'),
                'category': data.get('category'),
            }
        else:
            return Response(status=400)

        Compare.objects.update_or_create(**data)
        return Response(status=201)

    def delete(self, request):
        user = get_user(request)
        data = {
            'product': request.data.get('product'),
        }
        if 'customer' in user.keys():
            user = user['customer']
            data['customer'] = user
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            data['anonymous_customer'] = user
        else:
            return Response(status=400)
        Compare.objects.get(**data).delete()
        return Response(status=204)


class ReviewViewSet(viewsets.ViewSet):
    def create(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            star = RatingStar.objects.get(value=request.data.get('star'))
            data = {
                'star': star.id,
                'product': request.data.get('product'),
                'author': user.id,
                'text': request.data.get('text'),
                'advantages': request.data.get('advantages'),
                'disadvantages': request.data.get('disadvantages'),
            }
            review = ReviewCreateSerializer(data=data)
            if review.is_valid(raise_exception=True):
                review.save()
                return Response(status=201)
        else:
            return Response(status=400)

    def answer(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            parent = Review.objects.get(id=request.data.get('parent'))
            star = RatingStar.objects.get(value=0)
            data = {
                'product': request.data.get('product'),
                'author': user.id,
                'text': request.data.get('text'),
                'parent': parent.id,
                'star': star.id,
            }
            review = ReviewAnswerCreateSerializer(data=data)
            if review.is_valid(raise_exception=True):
                review.save()
                return Response(status=201)

    def delete(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            data = {
                'id': request.data.get('comment'),
                'author_id': user.id
            }
            Review.objects.filter(**data).delete()
            return Response(status=200)

    def list(self, request):
        if (request.data.get('id')):
            reviews = Review.objects.all().filter(
                product=request.data.get('id')
            )
            serializer = ReviewDetailSerializer(reviews, many=True)
            return Response(serializer.data)
        return Response(status=400)

    def user_list(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']
            reviews = Review.objects.all().filter(author=user)
            serializer = ReviewDetailSerializer(reviews, many=True)
            return Response(serializer.data)
        elif 'anonymous' in user.keys():
            user = user['anonymous']
            return Response(status=204)
        return Response(status=400)


class CustomerViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def check(self, request):
        return Response()

    def retrieve(self, request):
        if (request.headers.get('Authorization')):
            token = clear_token(request)
            customer = Customer.objects.filter(auth_token__key=token).first()
            if not (customer):
                customer = Customer.objects.filter(oauth2_provider_accesstoken__token=token).first()

            if (request.data.get('anonymous')):
                anonymous_token = request.data.get('anonymous')
                cart = Cart.objects.filter(anonymous_customer=anonymous_token)
                compare = Compare.objects.filter(anonymous_customer=anonymous_token)
                # wish = Wish.objects.filter(anonymous_customer=anonymous_token)
                if not (Cart.objects.filter(customer=customer.id)):
                    cart.update(customer=customer)
                    cart.update(anonymous_customer=None)
                else:
                    cart.delete()

                if not (Compare.objects.filter(customer=customer.id)):
                    compare.update(customer=customer)
                    compare.update(anonymous_customer=None)
                else:
                    compare.delete()

                # if not (Wish.objects.filter(customer=customer.id)):
                #     wish.update(customer=customer)
                #     wish.update(anonymous_customer=None)
                # else:
                #     wish.delete()

                AnonymousCustomer.objects.filter(id=anonymous_token).delete()
            serializer = CustomerDetailSerializer(customer)
            return Response(serializer.data)
        else:
            return Response(status=400)

    def change(self, request):
        user = get_user(request)
        if 'customer' in user.keys():
            user = user['customer']

            if not (request.data.get('password')):
                return Response({'password': 'This field is required'}, status=400)

            password = request.data.get('password')
            if not (user.check_password(password)):
                return Response({'password': 'Неверный пароль'}, status=400)

            headers = {
                'Authorization': request.headers.get('Authorization')
            }
            data = {
                'current_password': password,
            }

            if (request.data.get('first_name')):
                user.first_name = request.data.get('first_name')
            if (request.data.get('last_name')):
                user.last_name = request.data.get('last_name')
            if (request.data.get('phone')):
                user.phone_number = request.data.get('phone')

            if (request.data.get('email') and user.email != request.data.get('email')):
                    data['new_email'] = request.data.get('email')
                    r = requests.post(f'{settings.BACK_END_HOST}/api/v2/auth/users/set_email/', data=data, headers=headers)
                    try:
                        response = r.json()
                    except:
                        response = r
                    return Response(response, status=r.status_code)
            if (request.data.get('new_password')):
                data['new_password'] = request.data.get('new_password')
                r = requests.post(f'{settings.BACK_END_HOST}/api/v2/auth/users/set_password/', data=data,
                                  headers=headers)
                try:
                    response = r.json()
                except:
                    response = r
                return Response(response, status=r.status_code)

            user.save()
            return Response(status=200)
        else:
            return Response(status=400)


class CustomerSocial(viewsets.ViewSet):

    def social(self, request):
        url = 'https://oauth2.googleapis.com/token'
        provider_data = {
            'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'redirect_uri': settings.FRONT_END_HOST,
            'provider': 'google',
        }
        data = {
            'grant_type': 'authorization_code',
        }
        data = dict(list(data.items()) + list(request.data.items()) + list(provider_data.items()))
        res = requests.post(url, json=data)
        print('ОТВЕТ GOOGLE')
        print(res)
        print(res.json())
        if res.status_code == 200:
            local_prodvider_data = {
                'provider': {
                    'provider': 'google',
                    'client_id': Application.objects.get(name='Google Auth').client_id,
                    'client_secret': Application.objects.get(name='Google Auth').client_secret,
                    'redirect_uri': settings.FRONT_END_HOST,
                }
            }
            result = dict(list(res.json().items()) + list(local_prodvider_data.items()))
            return JsonResponse(result)
        return Response(status=400)


class AnonymousViewSet(viewsets.ViewSet):
    def create(self, request):
        anonymous = AnonymousCustomerCreateSerializer(data=request.data)
        if anonymous.is_valid():
            anonymous.save()
            return Response(anonymous.data)
        else:
            return Response(status=400)


class RedirectToFront(viewsets.ViewSet):

    def pass_reset_confirm(self, request, uid, token):
        return HttpResponseRedirect(f'{settings.FRONT_END_HOST}/user/password/reset/confirm/{uid}/{token}')


class NovaPoshtaViewSet(viewsets.ViewSet):
    def search(self, request):
        print(request.data.get('query'))
        if not (request.data.get('query')):
            return Response(status=204)
        query = request.data.get('query')
        queryset = Warehouse.objects.all().filter(
            Q(city_description_ru__istartswith=str(query)) | Q(city_description_uk__istartswith=str(query))).values(
            'description').distinct()
        serializer = NovaPoshtaCitySerializer(queryset, many=True)
        return Response(serializer.data, status=200)
