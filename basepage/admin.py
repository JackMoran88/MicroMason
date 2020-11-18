from django.contrib import admin
from .models import *
from .forms import *
from django.db.models import Sum, F, FloatField, Avg, IntegerField, Value, Count, Q
from django.contrib.admin import helpers

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
    extra = 1
    classes = ['collapse']



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image_tag']
    list_display_links = ['name']
    search_fields = ['name']
    inlines = [ProductOptionsInline, ProductImagesInline, ]
    save_on_top = True

    def get_inline_formsets(self, request, formsets, inline_instances, obj=None):
        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            prepopulated = dict(inline.get_prepopulated_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(
                inline, formset, fieldsets, prepopulated, readonly,
                model_admin=self,
            )
            if isinstance(inline, ProductOptionsInline):
                pass
                current_item_id = request.resolver_match.kwargs.get('object_id', None)
                if(current_item_id != None):
                    current_product = Product.objects.get(id=current_item_id)
                    current_category = current_product.category
                    q = Option.objects.all().filter(Q(category=current_category) | Q(category=None))
                    self.inlines[0].extra = len(q)
                    print(f'Текущий размер будет: {len(q)}')
                    # print(len(inline_admin_formset.forms))
                    self.inlines[0].max_num = len(q)
                    # for i in range(len(inline_admin_formset.forms), len(q)):
                    #     inline_admin_formset.forms.append(inline_admin_formset.forms[i - 1])
                    for form in inline_admin_formset.forms:
                        form.fields['parameter'].queryset = q


            inline_admin_formsets.append(inline_admin_formset)
        return inline_admin_formsets

    # list_filter = ('category',)

    form = ProductAdminForm

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.save_photos(form.instance)


# Импорты
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Option)
admin.site.register(OptionProduct)
admin.site.register(Customer)
admin.site.register(RatingStar)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(AnonymousCustomer)

admin.site.register(Wish)
