from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

from versatileimagefield.serializers import VersatileImageFieldSerializer

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q
from asgiref.sync import sync_to_async, async_to_sync

import product.models

######################################################################

# class ModelNameFunctionSerializer

######################################################################



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


class CartDetailSerializer(serializers.ModelSerializer):
    category_slug = serializers.CharField(source='category.slug')
    totals = serializers.FloatField(default=0)
    qty = serializers.IntegerField(default=0)
    main_image = VersatileImageFieldSerializer(sizes='product_img')
    class Meta:
        model = product.models.Product
        fields = ('__all__')