from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.core import serializers as CoreSerializer
from .models import *

from versatileimagefield.serializers import VersatileImageFieldSerializer

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q, Max, Min
from asgiref.sync import sync_to_async, async_to_sync

from order.serializers import *
import product.models


######################################################################

# class ModelNameFunctionSerializer

######################################################################


class ProductImagesDetailSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(sizes='product_img')

    class Meta:
        model = ProductImage
        fields = ('__all__')


class OptionDetailSerializer(serializers.ModelSerializer):
    parameter_name = serializers.CharField(source='parameter.name')
    parameter_id = serializers.IntegerField(source='parameter.id')
    class Meta:
        model = product.models.OptionProduct
        fields = ('__all__')


class ProductDetailSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='category.id')
    category = serializers.CharField(source='category.name')
    main_image = VersatileImageFieldSerializer(sizes='product_img')
    images = ProductImagesDetailSerializer(many=True)
    count_reviews = serializers.IntegerField()
    parent_category = serializers.CharField(required=False)
    category_slug = serializers.CharField(source='category.slug', required=False)
    rating_avg = serializers.FloatField(default=0)
    options = OptionDetailSerializer(many=True)

    class Meta:
        model = Product
        fields = ('__all__')

    def get_group_name(self):
        return 'Product'


class ProductSearchListSerializer(serializers.ModelSerializer):
    category_slug = serializers.CharField(source='category.slug')
    main_image = VersatileImageFieldSerializer(sizes='product_img')

    class Meta:
        model = Product
        fields = ('__all__')


class BrandDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    # price_min = serializers.IntegerField()
    # price_max = serializers.IntegerField()
    # test = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('__all__')

    # def get_test(self, context):
    #     return CoreSerializer.serialize('json', Brand.objects.all())
