from django.contrib import admin
from .models import *
from shop_settings.models import *
from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q
from django.contrib.admin import helpers
import copy

from mptt.admin import MPTTModelAdmin

# Register your models here.


admin.site.register(Cart)
admin.site.register(CartProduct)