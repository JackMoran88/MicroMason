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
    author = serializers.StringRelatedField()


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
    rating_avg = serializers.FloatField(default=0)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'code',
            'price', 'description', 'main_image',
            'slug', 'category', 'images',
            'reviews', 'options',
            'rating_avg',

        )


class CategoryDetailSerializer(serializers.ModelSerializer):
    # Просмотр определенной категории
    category = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True,
    )
    rating_avg = serializers.FloatField(default=0)

    class Meta:
        model = Product
        fields = ('id', 'name', 'code',
                  'price', 'description', 'main_image',
                  'slug', 'category', 'images',
                  'reviews', 'options',
                  'rating_avg',
                  )
        # fields = ('id','name')


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


class CartAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ('__all__')

    def create(self, validated_data):
        cart_product, _ = CartProduct.objects.update_or_create(
            cart=validated_data.get('cart'),
            product=validated_data.get('product'),
            defaults={'quantity': validated_data.get("quantity")}
        )
        return cart_product


class AnonymousCustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousCustomer
        fields = ('__all__')

    def create(self, validated_data):
        anonymous = AnonymousCustomer.objects.create()
        anonymous.save()
        return anonymous


class CartDetailSerializer(serializers.ModelSerializer):
    #
    totals = serializers.FloatField(default=0)

    class Meta:
        model = CartProduct
        # fields = ('id', 'quantity', 'totals')
        exclude = ('id',)


class AddWishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = ('__all__')

    def create(self, validated_data):
        product = Wish.objects.update_or_create(
            customer=validated_data.get('customer'),
            product=validated_data.get('product'),
            defaults={'product': validated_data.get("product"), 'customer': validated_data.get('customer')}
        )
        return product


class DetailCustomerSerializer(serializers.ModelSerializer):
    wish = serializers.SlugRelatedField(slug_field='product_id', many=True, read_only=True, )

    # wish = DetailWishSerializer(many=True, read_only=True)
    # wish = serializers.ManyRelatedField(child_relation='product')

    class Meta:
        model = Customer
        fields = ('id', 'email', 'phone_number', 'birthday', 'first_name', 'last_name', 'cart', 'wish')
