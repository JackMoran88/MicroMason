import os
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import RegexValidator

from django.db.models import Model, CASCADE
from django.db.models import CharField, FloatField, TextField, PositiveIntegerField, EmailField, DateTimeField
from django.db.models import DateField, BooleanField
from django.db.models import ManyToManyField, ForeignKey

from django.db.models import ImageField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from autoslug import AutoSlugField

from django.db.models import SET_NULL, SmallIntegerField, Avg

from model_utils import FieldTracker
from asgiref.sync import async_to_sync, sync_to_async
from django.utils.html import mark_safe

import mptt
from mptt.models import MPTTModel, TreeForeignKey

from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.placeholder import OnStoragePlaceholderImage

from basepage.models import *


class Address(Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+380991234567'.")

    customer = ForeignKey(Customer, on_delete=CASCADE, null=True, blank=True, related_name='address')
    anonymous_customer = ForeignKey(AnonymousCustomer, on_delete=SET_NULL, null=True, blank=True)

    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email = EmailField()
    phone_number = CharField(validators=[phone_regex], max_length=17, blank=True)
    address = CharField(max_length=250)
    postal_code = CharField(max_length=20)
    city = CharField(max_length=100)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.city}'

class Shipping(Model):
    name = CharField(max_length=225)
    description = CharField(max_length=5000)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Метод доставки'
        verbose_name_plural = 'Методы доставки'



class Payment(Model):
    pass


class Order(Model):
    PAYMENT_METHODS = (
        ('0', 'Наложеный платеж'),
        ('1', 'Оплата картой'),
    )
    PAID_STAUTUSES = (
        ('0', 'Не оплачено'),
        ('1', 'Ожидается оплата'),
        ('2', 'Оплачено'),
    )
    customer = ForeignKey(Customer, on_delete=CASCADE, null=True, blank=True)
    anonymous_customer = ForeignKey(AnonymousCustomer, on_delete=SET_NULL, null=True, blank=True)


    shipping = ForeignKey(Shipping, on_delete=CASCADE, null=True, blank=True)
    address = ForeignKey(Address, on_delete=CASCADE, null=True, blank=True)

    payment_method = CharField(max_length=255, choices=PAYMENT_METHODS, default=0)
    paid = CharField(max_length=255, choices=PAID_STAUTUSES, default=0)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'#{self.id} - {self.get_payment_method_display()}'



class OrderProduct(Model):
    order = ForeignKey(Order, on_delete=CASCADE, related_name='order_products')
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = PositiveIntegerField('Количество', default=1)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'

    def __str__(self):
        return f'x{self.quantity} {self.product.name}'

