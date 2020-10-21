from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions

from .serializers import *
from .models import *

from django.db.models import Sum, F, FloatField, Avg


class AuthCheck(APIView):
    # Проверка токена
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response()


class DetailCustomerView(APIView):
    def post(self, request):
        customer = Customer.objects.get(auth_token__key=request.data.get('token'))
        serializer = DetailCustomerSerializer(customer)
        return Response(serializer.data)


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
    def post(self, request, slug):
        product = Product.objects.annotate(
            rating_avg=Avg("ratings__star")
        ).get(slug=slug)
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

# class DetailWishView(APIView):
#     def post(self, request):
#         products = Product.objects.all().filter(product__customer=request.data.get('customer')).annotate(
#             rating_avg=Avg("ratings__star"),
#         )
#         serializer = DetailWishSerializer(products, many=True)
#         return Response(serializer.data)


# class DetailCurrentProductsView(APIView):
#     def post(self, request):
#         products = Product.objects.all().filter(id__in=[1])
#         serializer = ProductDetailSerializer(products, many=True)
#         return Response(serializer.data)
