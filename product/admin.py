from django.contrib import admin
from .models import *
from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q
from .forms import *
from django.forms import CheckboxSelectMultiple


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'request_name', 'order']
    search_fields = ['name', 'request_name']

@admin.register(OptionProduct)
class OptionProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'product', 'parameter']
    search_fields = ['name', 'product__name', 'parameter__name']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']



# Для отображения фото в товаре
fields = ['image_tag']
readonly_fields = ['image_tag']

class ProductImagesInline(admin.TabularInline):
    model = ProductImage
    fieldsets = (
        ('Photos', {
            'fields': ('image_tag',),
        }),
    )
    readonly_fields = readonly_fields
    extra = 0
    classes = ['collapse']

class ProductOptionsInline(admin.TabularInline):
    model = OptionProduct
    # raw_id_fields = ("parameter",)
    extra = 0
    classes = ['collapse']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "consoparameter":
            product_id = request.resolver_match.kwargs['object_id']
            category = Product.objects.get(id=product_id).category
            kwargs["queryset"] = Option.objects.filter(Q(category=category) | Q(category=None))
            print(kwargs["queryset"])
        return super(ProductOptionsInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image_tag']
    list_display_links = ['name']
    search_fields = ['name']
    inlines = [ProductOptionsInline, ProductImagesInline, ]
    save_on_top = True

    form = ProductAdminForm

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)

class OptiontAdmin(admin.ModelAdmin):
    """Отображение id в опциях и чекбоксы"""
    readonly_fields = ('id',)
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id']


