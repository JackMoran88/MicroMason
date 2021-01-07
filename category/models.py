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


class Filter(Model):
    TYPES = (
        ('0', 'default'),
        ('1', 'Type 1'),
        ('2', 'Type 2'),
        ('3', 'Type 3'),
    )

    name = CharField(max_length=64)
    description = CharField(max_length=255, null=True, blank=True)


    type = CharField(max_length=32, null=True, blank=True, choices=TYPES)
    request_name = CharField(max_length=32, blank=True)
    model = CharField(max_length=32, blank=True)
    query = CharField(max_length=32, null=True, blank=True)
    parameter = CharField(max_length=128, null=True)


    category = ManyToManyField(basepage.models.Category)
    order_by = PositiveIntegerField(blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"

    def __str__(self):
        return f'{self.name}'