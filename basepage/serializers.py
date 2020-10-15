from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class RecursiveSerializer(serializers.Serializer):
    # Рекурсивные детки
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterReviewDetailSerializer(serializers.ListSerializer):
    # Фильтрания отзывов, только те, у кого нет родителя(главные)
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CategoryListSerializer(serializers.ModelSerializer):
    # Список категорий
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Category
        fields = ('__all__')


class ReviewCreateSerializer(serializers.ModelSerializer):
    # Создание отзыва
    class Meta:
        model = Review
        fields = "__all__"


class ReviewDetailSerializer(serializers.ModelSerializer):
    # Отобразить отзывы
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewDetailSerializer
        model = Review
        fields = ('id', 'author', 'text', 'product', 'children')


class ProductImagesSerializer(serializers.ModelSerializer):
    # Фото товара
    class Meta:
        model = ProductImage
        fields = ('__all__')


class ProductDetailSerializer(serializers.ModelSerializer):
    # Просмотр товара
    category = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True,
    )
    images = ProductImagesSerializer(many=True)
    reviews = ReviewDetailSerializer(many=True)
    rating_avg = serializers.FloatField()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'code',
            'price', 'description', 'main_image',
            'slug', 'category', 'images',
            'reviews', 'options', 'rating_avg',

        )


class CategoryDetailSerializer(serializers.ModelSerializer):
    # Просмотр определенной категории
    category = ProductDetailSerializer(many=True)

    class Meta:
        model = Category
        # fields = ('__all__')
        fields = ('id', 'category')


class RatingCreateSerializer(serializers.ModelSerializer):
    # Добавление рейтинга пользователем
    class Meta:
        model = Rating
        fields = ('__all__')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            author=validated_data.get('author'),
            product=validated_data.get('product'),
            defaults={'star': validated_data.get("star")}
        )
        return rating
