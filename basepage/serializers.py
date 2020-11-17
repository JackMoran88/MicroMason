from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

from asgiref.sync import sync_to_async, async_to_sync


class RecursiveSerializer(serializers.Serializer):
    # Рекурсивные детки
    def to_representation(self, value):
        print(f'\t  to_representation')
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterReviewDetailSerializer(serializers.ListSerializer):
    # Фильтрания отзывов, только те, у кого нет родителя(главные)
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CategoryListSerializer(serializers.ModelSerializer):
    # Список категорий

    children = RecursiveSerializer(many=True, required=False)
    print('\t AFTER CHILDREN')

    # children = sync_to_async(RecursiveSerializer)(many=True)

    class Meta:
        model = Category
        fields = ('__all__')

    def get_group_name(self):
        return 'Categories'

    # def test(self):
    #     print(f'\t children {self.children}')


class ReviewCreateSerializer(serializers.ModelSerializer):
    # Создание отзыва
    class Meta:
        model = Review
        fields = "__all__"


class ReviewDetailSerializer(serializers.ModelSerializer):
    # Отобразить отзывы
    children = RecursiveSerializer(many=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        list_serializer_class = FilterReviewDetailSerializer
        model = Review
        fields = ('id', 'author', 'text', 'product', 'children')


class OptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('__all__')


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
    options = OptionDetailSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'code',
            'price', 'description', 'main_image',
            'slug', 'category', 'images',
            'reviews', 'options',
            'rating_avg'

        )

    def get_group_name(self):
        return 'Product'


class CategoryDetailSerializer(serializers.ModelSerializer):
    # Просмотр определенной категории
    category = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True,
    )
    images = ProductImagesSerializer(many=True)
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
            defaults={
                'star': validated_data.get("star"),
                'text': validated_data.get("text"),
                'advantages': validated_data.get("advantages"),
                'disadvantages': validated_data.get("disadvantages"),
            }
        )
        return rating


class RatingDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    customer = serializers.IntegerField()
    star = serializers.IntegerField(source='star.value')


    class Meta:
        model = Rating
        fields = ('__all__')


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
        # fields = ('__all__')
        exclude = ['last_update', ]

    def create(self, validated_data):
        anonymous = AnonymousCustomer.objects.create()
        anonymous.save()
        return anonymous


class CartDetailSerializer(serializers.ModelSerializer):
    totals = serializers.FloatField(default=0)
    qty = serializers.IntegerField(default=0)

    class Meta:
        model = Product
        fields = ('__all__')
        # exclude = ('id',)


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
        fields = ('id', 'email', 'phone_number', 'birthday', 'first_name', 'last_name', 'wish')


class CustomerChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
