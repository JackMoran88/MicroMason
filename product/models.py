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

import basepage.models

class Option(Model):
    name = CharField(max_length=225)
    request_name = CharField(max_length=225, null=True, blank=True)
    category = ManyToManyField(basepage.models.Category)
    order = PositiveIntegerField(blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'

    def __str__(self):
        return f"{self.id} - {self.name}"


class OptionProduct(Model):
    name = CharField(max_length=225, blank=True)
    product = ForeignKey('Product',
                         on_delete=CASCADE,
                         null=True,
                         blank=True, related_name='options')
    parameter = ForeignKey(Option, on_delete=CASCADE, null=True, blank=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Опции товара'
        verbose_name_plural = 'Опции товаров'

    def __str__(self):
        return f" {self.id}: {self.parameter} - {self.name}"


class Brand(Model):
    name = CharField(max_length=40)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return f"{self.name}"


class Product(Model):
    STATUSES = (
        ('0', 'Нет в наличии'),
        ('1', 'В наличии'),
        ('2', 'Ожидается'),
        ('3', 'Предзаказ'),
    )

    name = CharField(max_length=120, null=False)
    brand = ForeignKey(Brand, on_delete=CASCADE, null=True, blank=True)
    code = PositiveIntegerField(null=False)
    quantity = PositiveIntegerField(editable=True, default=0)
    price = FloatField(null=False)
    description = TextField(blank=True, null=True)
    main_image = VersatileImageField(
        "Изображение",
        upload_to="Products/",
        blank=True,
        ppoi_field='main_image_ppoi',
        placeholder_image=OnStoragePlaceholderImage(
            path='images/default/product/404.png'
        )
    )
    main_image_ppoi = PPOIField()

    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)

    category = TreeForeignKey(basepage.models.Category, on_delete=CASCADE, related_name='category')

    status = CharField(max_length=255, choices=STATUSES)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    tracker = FieldTracker(
        fields=('name', 'brand', 'code', 'quantity', 'price', 'description', 'main_image', 'status',), )

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        has_changed = self.tracker.changed()
        if has_changed:
            from basepage.ws_service import update_product
            async_to_sync(update_product)(self)
            return ret

    def image_tag(self):
        return mark_safe(
            '<img src="/media/%s" width="75" height="75" />' % (self.main_image)
        )

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.id}: {self.name}"


class ProductImage(Model):
    product_id = ForeignKey('Product', on_delete=CASCADE, related_name='images')
    image = VersatileImageField(upload_to='ProductImages/', unique=True, ppoi_field='image_ppoi', )
    image_ppoi = PPOIField()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Фото товаров'
        verbose_name = 'Фото товара'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.image))

    image_tag.short_description = 'Image'