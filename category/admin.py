from django.contrib import admin
from .models import *
# Register your models here.
from django.db import models
from django.forms import CheckboxSelectMultiple, TextInput

@admin.register(Filter)
class Filter(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_editable = ('state',)
    search_fields = ['name']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
        models.CharField: {'widget': TextInput(attrs={'size': '150'})},
    }


