from rest_framework import serializers
from .models import *
from basepage.models import *
from versatileimagefield.serializers import VersatileImageFieldSerializer
import product.models

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
        model = product.models.Product
        fields = ('id', 'name')


class SlideDetailSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(sizes='slider_img')

    class Meta:
        model = Slide
        fields = ('__all__')


class SliderDetailSerializer(serializers.ModelSerializer):
    slides = SlideDetailSerializer(many=True)

    class Meta:
        model = Slider
        fields = ('__all__')
