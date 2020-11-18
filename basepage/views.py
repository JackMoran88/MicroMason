from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, viewsets

from .serializers import *
from .models import *

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q

from channels.layers import get_channel_layer


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Category.objects.all().filter(parent__isnull=True)
        serializer = CategoryListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        products = Product.objects.filter(category__slug=slug).annotate(
            rating_avg=Avg("reviews__star", filter=Q(reviews__star__in=[1, 2, 3, 4, 5])),
            count_reviews=Count("reviews", output_field=IntegerField())
        )
        serializer = CategoryDetailSerializer(products, many=True)
        return Response(serializer.data)


class CartViewSet(viewsets.ViewSet):

    def list(self, request):
        if (request.headers.get('Authorization')):
            token = request.headers['Authorization'].replace('Token ', '')
            customer = Customer.objects.get(auth_token__key=token)
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
        products = Product.objects.all().filter(product__customer=customer).annotate(
            rating_avg=Avg("reviews__star", filter=Q(reviews__star__in=[1, 2, 3, 4, 5])),
            count_reviews=Count("reviews", output_field=IntegerField())
        )
        serializer = ProductDetailSerializer(products, many=True)
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


class ProductViewSet(viewsets.ViewSet):
    def retrieve(self, request):
        if request.data.get('id'):
            product = Product.objects.annotate(
                rating_avg=Avg("reviews__star", filter=Q(reviews__star__in=[1, 2, 3, 4, 5])),
                count_reviews=Count("reviews", output_field=IntegerField())
            ).get(id=request.data.get('id'))
        else:
            product = Product.objects.annotate(
                rating_avgrating_avg=Avg("reviews__star", filter=Q(reviews__star__in=[1, 2, 3, 4, 5])),
                count_reviews=Count("reviews", output_field=IntegerField())
            ).get(slug=request.data.get('slug'))

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def list(self, request):
        if request.data.get('ids'):
            ids = request.data.get('ids')
            products = Product.objects.filter(id__in=ids)
        else:
            products = Product.objects.annotate(
                rating_avg=Avg("reviews__star", filter=Q(reviews__star__in=[1, 2, 3, 4, 5])),
                count_reviews=Count("reviews", output_field=IntegerField())
            ).filter(slug__in=request.data.get('slugs'))

        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def check(self, request):
        return Response()

    def anonymousCreate(self, request):
        anonymous = AnonymousCustomerCreateSerializer(data=request.data)
        if anonymous.is_valid():
            anonymous.save()
            return Response(anonymous.data)
        else:
            return Response(status=400)

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

    def setFullName(self, request):
        token = request.headers['Authorization'].replace('Token ', '')
        customer = Customer.objects.get(auth_token__key=token)
        if (request.data.get('first_name') and request.data.get('last_name')):
            customer.first_name = request.data.get('first_name')
            customer.last_name = request.data.get('last_name')
            customer.save()
            return Response(status=200)
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
