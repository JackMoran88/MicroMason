from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

from versatileimagefield.serializers import VersatileImageFieldSerializer

from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q
from asgiref.sync import sync_to_async, async_to_sync

from basepage.service import *
from basepage.serializers import *

import product.models

######################################################################

# class ModelNameFunctionSerializer

######################################################################
class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class ShippingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ('__all__')


class AddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('__all__')


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('__all__')


class OrderProductDetailHelper(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    main_image = VersatileImageFieldSerializer(sizes='product_img')
    parent_category = serializers.CharField(required=False)
    category_slug = serializers.CharField(source='category.slug', required=False)
    rating_avg = serializers.FloatField(default=0)

    class Meta:
        model = product.models.Product
        # fields = ('__all__')
        exclude = ['description', ]


class OrderProductDetailSerializer(serializers.ModelSerializer):
    product = OrderProductDetailHelper()
    total = serializers.SerializerMethodField()

    def get_total(self, data):
        return data.product.price * data.quantity

    class Meta:
        model = OrderProduct
        fields = ('id', 'product', 'quantity', 'total')

class OrderStatusDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    order_products = OrderProductDetailSerializer(many=True, required=True)
    paid = ChoiceField(choices=Order.PAID_STAUTUSES)
    # payment_method = ChoiceField(choices=Order.PAYMENT_METHODS)
    payment_method = PaymentDetailSerializer()
    total = serializers.FloatField(default=0)
    qty = serializers.IntegerField(default=0)
    status = OrderStatusDetailSerializer()
    shipping = ShippingDetailSerializer()
    address = AddressDetailSerializer()

    class Meta:
        model = Order
        fields = ('__all__')


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('__all__')

    def create(self, validated_data):
        order = Order.objects.create(
            customer=validated_data.get('customer'),
            anonymous_customer=validated_data.get('anonymous_customer'),
            payment_method=validated_data.get('payment_method'),
        )
        return order

