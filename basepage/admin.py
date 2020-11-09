from django.contrib import admin
from .models import *
from .forms import *





# Для отображения фото в товаре
fields = ['image_tag']
readonly_fields = ['image_tag']


class ProductImages(admin.TabularInline):
    model = ProductImage
    # fields = ['image_tag']
    readonly_fields = ['image_tag']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = MultipluProductImage
    inlines = [ProductImages]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)


@admin.register(ProductImage)
class ProductAdmin(admin.ModelAdmin):
    fields = ['image_tag']
    readonly_fields = ['image_tag']





# Импорты
admin.site.register(Category)
admin.site.register(Option)
admin.site.register(OptionParameter)
admin.site.register(OptionProduct)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(AnonymousCustomer)

admin.site.register(Wish)
