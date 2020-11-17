from django.contrib import admin
from .models import *
from .forms import *

# Для отображения фото в товаре
fields = ['image_tag']
readonly_fields = ['image_tag']


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     form = MultipluProductImage
#     inlines = [ProductImages]
#
#
#     def save_related(self, request, form, formsets, change):
#         super().save_related(request, form, formsets, change)
#         form.save_photos(form.instance)


class ProductImagesInline(admin.TabularInline):
    model = ProductImage
    fieldsets = (
        ('Фото', {
            'classes': ('collapse',),
            'fields': ('image_tag',),
        }),
    )
    readonly_fields = readonly_fields
    extra = 0


class ProductOptionsInline(admin.TabularInline):
    model = OptionProduct
    # fields = ('parameter','name')
    extra = 0



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image_tag']
    list_display_links = ['name']
    search_fields = ['name']
    inlines = [ProductOptionsInline, ProductImagesInline, ]
    save_on_top = True

    # form = ProductAdminForm
    #
    # def save_related(self, request, form, formsets, change):
    #     super().save_related(request, form, formsets, change)
    #     form.save_photos(form.instance)


# Импорты
admin.site.register(Category)
admin.site.register(Option)
admin.site.register(OptionProduct)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(AnonymousCustomer)

admin.site.register(Wish)
