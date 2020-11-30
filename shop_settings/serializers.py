from rest_framework import serializers
from .models import *
from basepage.models import *


class FooterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer
        fields = ('name', 'description')


class SettingDetailSerializer(serializers.ModelSerializer):
    footer = FooterDetailSerializer(many=True)

    class Meta:
        model = Setting
        fields = ('__all__')


class ProductSortTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSortType
        fields = ('__all__')

class BreadCrumbCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class BreadCrumbProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')
