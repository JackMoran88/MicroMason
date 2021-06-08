from django.contrib import admin
from .models import *
from shop_settings.models import *
from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q
from django.contrib.admin import helpers
import copy

from django.db import models
from django.forms import CheckboxSelectMultiple

from mptt.admin import MPTTModelAdmin

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    search_fields = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'phone_number']
    list_display = ['id', 'get_full_name', 'phone_number', ]


@admin.register(AnonymousCustomer)
class AnonymousCustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'token', 'last_update', ]


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'star', 'text']

@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'anonymous_customer', 'product']

@admin.register(Compare)
class CompareAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'anonymous_customer', 'product', 'category']



