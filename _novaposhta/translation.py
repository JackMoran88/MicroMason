from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Cities)
class CitiesTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(Warehouse)
class WarehouseTranslationOptions(TranslationOptions):
    fields = ('description', 'city_description')

@register(Invoice)
class InvoiceTranslationOptions(TranslationOptions):
    fields = ()

@register(Counterparty)
class CounterpartyTranslationOptions(TranslationOptions):
    fields = ()

@register(Delivery)
class DeliveryTranslationOptions(TranslationOptions):
    fields = ()

