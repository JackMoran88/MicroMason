from django.contrib import admin
from .models import *
from .forms import *
from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q
from django.contrib.admin import helpers
import copy


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    form = FooterAdminForm
    list_display = ['id', 'name']

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'phone', 'email']

@admin.register(ProductSortType)
class ProductSortTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'field', 'order']

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url']

@admin.register(Slider)
class SliderTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'place']


