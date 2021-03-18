from django.contrib import admin
from .models import *
from django import forms
from django.shortcuts import redirect

from django.conf.urls import url
from django.utils.html import format_html
from django.urls import reverse
from _novaposhta import models
from django.db.models import Q
from django.contrib import messages


class OrderAdminForm(admin.TabularInline):
    model = OrderProduct
    extra = 1
    classes = ['collapse']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderAdminForm, ]
    exclude = ('ready',)

    change_form_template = "admin/order_order__change_form.html"

    def response_change(self, request, obj):
        if "_make-shipping" in request.POST:
            if (int(obj.paid) != 2):
                messages.error(request, "Покупитель не произвел оплату")
                return redirect(request.path)
            counterparty = models.Counterparty.objects.filter(status=True).first()
            if not (counterparty):
                messages.error(request, 'Нужно ключить контрагента')
                return redirect(request.path)
            city_sender = models.Cities.objects.filter(
                Q(description_ru=counterparty.city) | Q(description_uk=counterparty.city)).first().city_ref
            data = {
                'order': obj,
                'payer_type': 'Recipient',
                'service_type': '',
                'cost': obj.get_amount(),
                'sender': counterparty.sender_ref,
                'city_sender': city_sender,
                'sender_address': '',
                'contact_sender': counterparty.contact_ref,
                'sender_phone': settings.NOVA_POSHTA_PHONE_NUMBER,
            }
            # Способ оплаты
            if (obj.payment_method.type == 'liqpay'):
                data['payment_method'] = 'NonCash'
            else:
                data['payment_method'] = 'Cash'

            if (obj.address):
                data['recipients_phone'] = obj.address.phone_number
                data['recipient_city_name'] = obj.address.city
                data['recipient_name'] = obj.address.get_full_name()

                if (obj.address.address_type == 'novaposhta_warehouse'):
                    data['recipient_address_name'] = models.Warehouse.objects.filter(
                        Q(description_ru=obj.address.address) | Q(description_uk=obj.address.address)).first().number
                    data['recipient_area'] = ''
                    data['recipient_area_region'] = ''
                    data['recipient_house'] = ''
                    data['recipient_flat'] = ''

                data['recipient_type'] = 'PrivatePerson'
            instance = models.Invoice.objects.create(**data)
            messages.success(request, "Накладная успешно создана")
            return redirect(instance.get_admin_url())
        return super().response_change(request, obj)


admin.site.register(OrderProduct)
admin.site.register(Address)
admin.site.register(Shipping)
admin.site.register(Payment)
admin.site.register(OrderStatus)
