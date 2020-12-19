from django.contrib import admin
from .models import *
from django import forms

admin.site.register(OrderProduct)
admin.site.register(Address)
admin.site.register(Shipping)


class OrderAdminForm(admin.TabularInline):
    model = OrderProduct
    extra = 1
    classes = ['collapse']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderAdminForm, ]
