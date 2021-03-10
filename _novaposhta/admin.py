from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *
from .services import *
from django.shortcuts import redirect
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib import messages


@admin.register(Cities)
class CitiesAdmin(TranslationAdmin):
    readonly_fields = ('ref', 'description', 'area', 'city_id', 'city_ref')
    list_display = ('description', 'area')


@admin.register(Warehouse)
class WarehouseAdmin(TranslationAdmin):
    readonly_fields = ('description', 'ref', 'number', 'type_warehouse', 'city_description', 'city_ref')
    list_display = ('description', 'city_description')


@admin.register(Invoice)
class InvoiceAdmin(TranslationAdmin):
    list_display = ('recipient_city_name', 'description', 'cost')

    change_form_template = "admin/_novaposhta_order__change_form.html"

    def response_change(self, request, obj):
        if "_make-shipping" in request.POST:
            properties = {
                "NewAddress": "1",
                # Кто оплачивает
                "PayerType": obj.payer_type,
                # Способ оплаты
                "PaymentMethod": obj.payment_method,
                # Вид груза
                "CargoType": obj.cargo_type,
                # Объем
                "VolumeGeneral": obj.volume_general,
                # Фактический вес
                "Weight": obj.weight,
                # Технология доставки (Отделение-Отделение\Двери-Двери)
                "ServiceType": obj.service_type,
                # Количество мест отправления
                "SeatsAmount": obj.seats_amount,
                # Описание
                "Description": obj.description,
                # Стоимость
                "Cost": obj.cost,
                # Индитификатор города отправителя
                "CitySender": obj.city_sender,
                # Идентификатор отправителя
                "Sender": obj.sender,
                # Идентификатор адреса отправителя
                "SenderAddress": obj.sender_address,
                # Идентификатор контактного лица отправителя
                "ContactSender": obj.contact_sender,
                # Телефон отправителя в формате: +380660000000, 380660000000, 0660000000
                "SendersPhone": obj.sender_phone,
                # Идентификатор города получателя (УКАЗЫВАЕТЬСЯ СТРОКОЙ)
                "RecipientCityName": obj.recipient_city_name,
                # Идентификатор области (УКАЗЫВАЕТЬСЯ СТРОКОЙ)
                "RecipientArea": obj.recipient_area,
                # Идентификатор района (УКАЗЫВАЕТЬСЯ СТРОКОЙ)
                "RecipientAreaRegions": obj.recipient_area_region,
                # Идентификатор номера отделения (УКАЗЫВАЕТЬСЯ СТРОКОЙ)
                "RecipientAddressName": obj.recipient_address_name,
                # Идентификатор номера улицы (УКАЗЫВАЕТЬСЯ СТРОКОЙ)
                "RecipientHouse": obj.recipient_house,
                # Идентификатор этажа (УКАЗЫВАЕТЬСЯ СТРОКОЙ)
                "RecipientFlat": obj.recipient_flat,
                # Идентификатор ФИО получателя (УКАЗЫВАЕТЬСЯ СТРОКОЙ)
                "RecipientName": obj.recipient_name,
                # Тип получателя
                "RecipientType": obj.recipient_type,
                # Телефон получателя
                "RecipientsPhone": obj.recipients_phone,
                # Дата отправки в формате дд.мм.гггг
                "DateTime": str(obj.date_time.strftime('%d.%m.%Y')),
                # "RecipientWarehouse": 'e68be3b9-ca66-11e9-b0c5-005056b24375'
            }

            req = saveDocument(properties).json()
            if (req['success']):
                data = {
                    'order': obj.order,
                    'ref': req['data'][0]['Ref'],
                    'cost_on_site': req['data'][0]['CostOnSite'],
                    'estimated_delivery_date': req['data'][0]['EstimatedDeliveryDate'],
                    'int_doc_number': req['data'][0]['IntDocNumber'],
                    'type_document': req['data'][0]['TypeDocument'],
                }
                instance = Delivery.objects.create(**data)
                messages.success(request, "Отправление успешно создано!")
                obj.delete()
                return redirect(instance.get_admin_url())
            messages.error(request, "Ошибка создания отправления!")
            messages.error(request, req['errors'])
        return super().response_change(request, obj)


@admin.register(Counterparty)
class CounterpartyAdmin(TranslationAdmin):
    change_form_template = "admin/_novaposhta_conterparty__change_form.html"

    def response_change(self, request, obj):
        if "_make-conterparty" in request.POST:
            properties = {
                "FirstName": obj.first_name,
                "MiddleName": obj.middle_name,
                "LastName": obj.last_name,
                "Phone": obj.phone,
                "Email": obj.email,
                "CounterpartyType": obj.counterparty_type,
                "CounterpartyProperty": obj.counterparty_property,
            }
            result = saveCounterparty(properties).json()
            if (result['success']):
                obj.ref = result['data'][0]['Ref']
                obj.save()
            return redirect(request.path)

        return super().response_change(request, obj)


@admin.register(Delivery)
class DeliveryAdmin(TranslationAdmin):
    list_display = ('int_doc_number', 'estimated_delivery_date')
    readonly_fields = ('ref', 'cost_on_site', 'estimated_delivery_date', 'int_doc_number', 'type_document', 'status', 'order')
    change_form_template = "admin/_novaposhta_delivery__change_form.html"

    def response_change(self, request, obj):
        if "_make-update" in request.POST:
            obj.update_status()
            return redirect(request.path)

        return super().response_change(request, obj)
