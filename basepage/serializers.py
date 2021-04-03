from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

from versatileimagefield.serializers import VersatileImageFieldSerializer

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q
from asgiref.sync import sync_to_async, async_to_sync

from .service import *

from order.serializers import *
from product.serializers import *
from _novaposhta.models import Warehouse


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


class ReviewDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_full_name')
    star = serializers.IntegerField(source='star.value')
    children = RecursiveSerializer(many=True)
    customer = serializers.IntegerField(source='author_id')

    class Meta:
        list_serializer_class = ReviewDetailFilterSerializer
        model = Review
        fields = ('__all__')


class CategorySearchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


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


class AnonymousCustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousCustomer
        exclude = ['id', 'last_update']


class CustomerDetailSerializer(serializers.ModelSerializer):
    address = AddressDetailSerializer(many=True)
    wish = serializers.SlugRelatedField(slug_field='product_id', many=True, read_only=True, )

    class Meta:
        model = Customer
        fields = ('id', 'email', 'phone_number', 'birthday', 'first_name', 'last_name', 'wish', 'address')


class CustomerChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class RecursiveField(serializers.Serializer):
    def to_native(self, value):
        return CategoriesListSerializer(value, context={"parent": self.parent.object, "parent_serializer": self.parent})


class CategoriesListSerializer(serializers.ModelSerializer):
    main_image = VersatileImageFieldSerializer(sizes='category_img')

    class Meta:
        model = Category
        fields = '__all__'

    def get_group_name(self):
        return 'Categories'

CategoriesListSerializer._declared_fields['children'] = CategoriesListSerializer(
    many=True,
    source='get_children',
)


class CompareProductDetailSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id')
    category = serializers.CharField(source='category.name')
    main_image = VersatileImageFieldSerializer(sizes='product_img')
    parent_category = serializers.CharField(required=False)
    category_slug = serializers.CharField(source='category.slug', required=False)
    rating_avg = serializers.FloatField(default=0)
    options = OptionDetailSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('description',)


class CompareDetailSerializer(serializers.ModelSerializer):
    product = CompareProductDetailSerializer()
    category_name = serializers.CharField(source='product.category.name')

    class Meta:
        model = Compare
        fields = ('__all__')


class NovaPoshtaCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ('description',)
