from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import permissions

from .serializers import *
from .models import *




class AuthCheck(APIView):
    # Проверка токена
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        return Response()



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
        category = Category.objects.get(slug=slug)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)


class ProductDetailView(APIView):
    # Просмотр товара
    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
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

