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



class Cart(Model):
    customer = ForeignKey('basepage.Customer', on_delete=CASCADE, null=True, blank=True)
    anonymous_customer = ForeignKey('basepage.AnonymousCustomer', on_delete=SET_NULL, null=True, blank=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f'Корзина #{self.id}'


class CartProduct(Model):
    cart = ForeignKey(Cart, on_delete=CASCADE)
    product = ForeignKey('product.Product', on_delete=CASCADE)
    quantity = PositiveIntegerField('Количество', default=1)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар корзины"
        verbose_name_plural = "Товары корзины"

    def __str__(self):
        return f"Корзина #{self.cart.id} - {self.product}"
