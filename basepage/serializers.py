from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategoryListSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Category
        fields = ('__all__')




class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('__all__')

class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True,
    )
    images = ProductImagesSerializer(many=True)
    class Meta:
        model = Product
        fields = ('__all__')




class CategoryDetailSerializer(serializers.ModelSerializer):
    category = ProductDetailSerializer(many=True)

    class Meta:
        model = Category
        # fields = ('__all__')
        fields = ('id', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"