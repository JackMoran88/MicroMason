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
    ADDRESS_TYPE = (
        ('address', 'Адресс'),
        ('novaposhta_warehouse', 'Отделение новой почты'),
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+380991234567'.")

    customer = ForeignKey(Customer, on_delete=CASCADE, null=True, blank=True, related_name='address')
    anonymous_customer = ForeignKey(AnonymousCustomer, on_delete=SET_NULL, null=True, blank=True)

    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    middle_name = CharField(max_length=50)

    email = EmailField()
    phone_number = CharField(validators=[phone_regex], max_length=17, blank=True)
    address = CharField(max_length=250)
    postal_code = CharField(max_length=20, null=True, blank=True)
    city = CharField(max_length=100)

    address_type = CharField('Тип адресса', null=True, blank=True, max_length=255, choices=ADDRESS_TYPE)

    priority = BooleanField(default=False)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.city}'

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Shipping(Model):
    name = CharField(max_length=225)
    description = CharField(max_length=5000)

    price = PositiveIntegerField()

    order_by = PositiveIntegerField(null=True, blank=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Метод доставки'
        verbose_name_plural = 'Методы доставки'

    def __str__(self):
        return f'{self.name}'


class Payment(Model):
    name = CharField(max_length=255)
    type = CharField(max_length=255, null=True, blank=True)

    description = TextField(blank=True, null=True)

    order_by = PositiveIntegerField(blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Метод оплаты'
        verbose_name_plural = 'Методы оплаты'

    def __str__(self):
        return f'{self.name}'


class OrderStatus(Model):
    name = CharField(max_length=255)
    order_by = PositiveIntegerField(blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'

    def __str__(self):
        return f'{self.name}'


class Order(Model):
    PAID_STAUTUSES = (
        ('0', 'Не оплачено'),
        ('1', 'Ожидается оплата'),
        ('2', 'Оплачено'),
    )
    customer = ForeignKey(Customer, on_delete=CASCADE, null=True, blank=True)
    anonymous_customer = ForeignKey(AnonymousCustomer, on_delete=SET_NULL, null=True, blank=True)

    shipping = ForeignKey(Shipping, on_delete=CASCADE, null=True, blank=True, verbose_name='Способ доставки')
    delivery_point = TextField(null=True, blank=True)
    address = ForeignKey(Address, on_delete=CASCADE, null=True, blank=True, verbose_name='Адресс доставки')

    payment_method = ForeignKey(Payment, on_delete=CASCADE, verbose_name='Способ оплаты')
    paid = CharField(max_length=255, choices=PAID_STAUTUSES, default=0, verbose_name='Статус оплаты')
    status = ForeignKey(OrderStatus, on_delete=CASCADE, verbose_name='Статус заказа',
                        null=True)

    note = TextField(blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    tracker = FieldTracker(
        fields=('status',), )

    def save(self, *args, **kwargs):
        if not self.status:
            self.status = OrderStatus.objects.get(order_by=1)

        ret = super().save(*args, **kwargs)
        has_changed = self.tracker.changed()
        if has_changed:
            from basepage.tasks import se_order

            se_order('update', self, [self.customer.email])
            return ret
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'#{self.id}'

    def get_amount(self):
        items = self.order_products.all()
        cart_amount = 0
        for item in items:
            item_amount = item.product.price * item.quantity
            cart_amount += item_amount

        if (self.shipping.price):
            cart_amount += self.shipping.price
        return cart_amount

    def get_description(self):
        items = self.order_products.all()
        description = ''
        for item in items:
            item_description = f'{item.product.name} x {item.quantity} \n'
            description += item_description
        return description


class OrderProduct(Model):
    order = ForeignKey(Order, on_delete=CASCADE, related_name='order_products')
    product = ForeignKey('product.Product', on_delete=CASCADE)
    quantity = PositiveIntegerField('Количество', default=1)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'

    def __str__(self):
        return f'x{self.quantity} {self.product.name}'
