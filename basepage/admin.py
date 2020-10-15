from django.contrib import admin

from .models import *

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Option)
admin.site.register(OptionParameter)
admin.site.register(OptionProduct)
admin.site.register(Customer)
admin.site.register(Review)
