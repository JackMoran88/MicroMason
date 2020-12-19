from django.contrib import admin
from .models import *
from .forms import *
from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q
from django.contrib.admin import helpers
import copy


admin.site.register(Setting)
admin.site.register(ProductSortType)
admin.site.register(Slide)
admin.site.register(Slider)


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    form = FooterAdminForm