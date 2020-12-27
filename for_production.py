


# Сортировка app в админке.
# Данный код в settings.py
# set my ordering list
ADMIN_ORDERING = [
    ('basepage', [
       'Category',
       'Customer',
       'RatingStar',
       'Rating',
       'Review',
       'AnonymousCustomer',
       'Wish',
    ]),
    ('product', [
       'Product',
       'ProductImage',
       'Brand',
       'OptionProduct',
       'Option',
    ]),
    ('cart', [
       'Cart',
       'CartProduct',
    ]),
    ('order', [
       'Order',
       'OrderProduct',
       'Address',
       'Shipping',
       'Payment',
    ]),
    ('shop_settings', [
       'Setting',
       'Footer',
       'ProductSortType',
       'Slider',
       'Slide',
    ]),
]
# Creating a sort function
def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    for app_name, object_list in ADMIN_ORDERING:
        app = app_dict[app_name]
        app['models'].sort(key=lambda x: object_list.index(x['object_name']))
        yield app


# Covering django.contrib.admin.AdminSite.get_app_list
from django.contrib import admin

admin.AdminSite.get_app_list = get_app_list

# !Сортировка app в админке.!