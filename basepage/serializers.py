from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q
from asgiref.sync import sync_to_async, async_to_sync


######################################################################

# class ModelNameFunctionSerializer

######################################################################

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewDetailFilterSerializer(serializers.ListSerializer):
    # Фильтрания отзывов, только те, у кого нет родителя(главные)
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


######################################################################


class CategoryListSerializer(serializers.ModelSerializer):

    children = RecursiveSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = ('__all__')

    def get_group_name(self):
        return 'Categories'


class OptionDetailSerializer(serializers.ModelSerializer):
    parameter = serializers.CharField(source='parameter.name')
    class Meta:
        model = OptionProduct
        fields = ('__all__')


class ProductImagesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('__all__')


class ReviewDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    star = serializers.IntegerField(source='star.value')
    children = RecursiveSerializer(many=True)
    customer = serializers.IntegerField(source='author_id')

    class Meta:
        list_serializer_class = ReviewDetailFilterSerializer
        model = Review
        fields = ('__all__')


class ProductDetailSerializer(serializers.ModelSerializer):

    category = serializers.CharField(source='category.name')
    images = ProductImagesDetailSerializer(many=True)
    count_reviews = serializers.IntegerField()
    rating_avg = serializers.FloatField(default=0)
    options = OptionDetailSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'code',
            'price', 'description', 'main_image',
            'slug', 'category', 'images',
            'count_reviews', 'options',
            'rating_avg'

        )

    def get_group_name(self):
        return 'Product'


class CategoryDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    images = ProductImagesDetailSerializer(many=True)
    rating_avg = serializers.FloatField(default=0)
    count_reviews = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'code',
                  'price', 'description', 'main_image',
                  'slug', 'category', 'images',
                  'count_reviews', 'options',
                  'rating_avg',
                  )


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('__all__')

    def create(self, validated_data):
        review, _ = Review.objects.update_or_create(
            author=validated_data.get('author'),
            product=validated_data.get('product'),
            parent=None,
            defaults={
                'star': validated_data.get("star"),
                'text': validated_data.get("text"),
                'advantages': validated_data.get("advantages"),
                'disadvantages': validated_data.get("disadvantages"),
            }
        )
        return Review


class ReviewAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('__all__')

    def create(self, validated_data):
        review = Review.objects.create(
            author=validated_data.get('author'),
            product=validated_data.get('product'),
            parent=validated_data.get('parent'),
            star=validated_data.get('star'),
            text=validated_data.get("text"),
        )
        return Review


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


class WishAddSerializer(serializers.ModelSerializer):
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


class CustomerDetailSerializer(serializers.ModelSerializer):
    wish = serializers.SlugRelatedField(slug_field='product_id', many=True, read_only=True, )

    class Meta:
        model = Customer
        fields = ('id', 'email', 'phone_number', 'birthday', 'first_name', 'last_name', 'wish')


class CustomerChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
