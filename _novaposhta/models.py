import os
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import RegexValidator

from django.db.models import Model, CASCADE
from django.db.models import CharField, FloatField, TextField, PositiveIntegerField, EmailField, DateTimeField
from django.db.models import DateField, BooleanField
from django.db.models import ManyToManyField, ForeignKey

from django.db.models import ImageField

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from autoslug import AutoSlugField

from django.db.models import SET_NULL, SmallIntegerField, Avg

from model_utils import FieldTracker
from asgiref.sync import async_to_sync, sync_to_async
from django.utils.html import mark_safe

import mptt
from mptt.models import MPTTModel, TreeForeignKey

from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.placeholder import OnStoragePlaceholderImage

from basepage.models import *
from order.models import *
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .services import *


class Cities(Model):
    description = CharField('Город', max_length=255)
    ref = CharField('Идентификатор города', max_length=255)
    area = CharField('Область', max_length=255)
    city_id = CharField('Код населенного пункта', max_length=255)
    city_ref = CharField('Идентификатор (REF) типа населенного пункта', max_length=255)

    class Meta:
        verbose_name = ('Город')
        verbose_name_plural = ('Города')


class Warehouse(Model):
    description = CharField('Отделение', max_length=255)
    ref = CharField('Идентификатор отделения', max_length=255)
    number = CharField('Номер', max_length=255)
    type_warehouse = CharField('Тип отделения', max_length=255)

    city_description = CharField('Название населенного пункта', max_length=255)
    city_ref = CharField('Идентификатор населенного пункта', max_length=255)

    class Meta:
        verbose_name = ('Отделение')
        verbose_name_plural = ('Отделения')


class Invoice(Model):
    PAYER_TYPES = (
        ('Recipient', 'Получатель'),
        ('Sender', 'Отправитель'),
        ('ThirdPerson', 'Третья особа'),
    )
    PAYMENT_TYPES = (
        ('Cash', 'Наличный расчет'),
        ('NonCash', 'Безналичный расчет'),
    )
    CARGO_TYPES = (
        ('Parcel', 'Посилка'),
        ('Cargo', 'Вантаж'),
        ('Documents', 'Документи'),
        ('TiresWheels', 'Шини-диски'),
        ('Pallet', 'Палети'),
    )
    SERVICE_TYPES = (
        ('WarehouseWarehouse', 'Склад-Склад'),
        ('DoorsDoors', 'Двері-Двері'),
        ('DoorsWarehouse', 'Двері-Склад'),
        ('WarehouseDoors', 'Склад-Двері'),
    )
    order = ForeignKey(Order, on_delete=CASCADE)
    payer_type = CharField('Плательщик', null=True, blank=True, max_length=255, choices=PAYER_TYPES)
    payment_method = CharField('Способ оплаты', null=True, blank=True, max_length=255, choices=PAYMENT_TYPES)
    cargo_type = CharField('Тип посылки', null=True, blank=True, max_length=255, choices=CARGO_TYPES)
    volume_general = CharField('Объем', null=True, blank=True, max_length=255)
    weight = CharField('Вес', null=True, blank=True, max_length=255)
    service_type = CharField('Вид доставки', null=True, blank=True, max_length=255, choices=SERVICE_TYPES)
    seats_amount = CharField('Количество мест', null=True, blank=True, max_length=255)
    description = TextField('Описание', null=True, blank=True, max_length=5000)
    cost = CharField('Цена', null=True, blank=True, max_length=5000)
    city_sender = CharField('Индитификатор города отправителя', null=True, blank=True, max_length=255)
    sender = CharField('Идентификатор отправителя', null=True, blank=True, max_length=255)
    sender_address = CharField('Идентификатор адреса отправителя', null=True, blank=True, max_length=255)
    contact_sender = CharField('Идентификатор контактного лица отправителя', null=True, blank=True, max_length=255)
    sender_phone = CharField('Телефон отправителя', null=True, blank=True, max_length=255)
    recipient_city_name = CharField('Идентификатор города получателя', null=True, blank=True, max_length=255)
    recipient_area = CharField('Идентификатор области', null=True, blank=True, max_length=255)
    recipient_area_region = CharField('Идентификатор района', null=True, blank=True, max_length=255)
    recipient_address_name = CharField('Идентификатор номера отделения', null=True, blank=True, max_length=255)
    recipient_house = CharField('Идентификатор номера улицы', null=True, blank=True, max_length=255)
    recipient_flat = CharField('Идентификатор этажа ', null=True, blank=True, max_length=255)
    recipient_name = CharField('ФИО получателя', null=True, blank=True, max_length=255)
    recipient_type = CharField('Тип получателя', null=True, blank=True, max_length=255)
    recipients_phone = CharField('Телефон получателя', null=True, blank=True, max_length=255)
    date_time = DateField('Дата отправки', null=True)

    class Meta:
        verbose_name = ('Накладная')
        verbose_name_plural = ('Накладные')

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))


class Counterparty(Model):
    COUNTERPARTY_TYPES = (
        ('Organization', 'Организация'),
        ('PrivatePerson', 'Частное лицо'),
    )

    first_name = CharField('Имя', max_length=255)
    middle_name = CharField('Отчество', max_length=255)
    last_name = CharField('Фамилия', max_length=255)

    sender_ref = CharField('Sender Ref', max_length=255)
    city = CharField('Город отправления', max_length=255)
    contact_ref = CharField('Contact Ref', max_length=255)
    status = BooleanField(default=False)

    phone = CharField('Телефон', max_length=255)

    email = EmailField('Email', max_length=255)
    counterparty_type = CharField('Плательщик', null=True, blank=True, max_length=255, choices=COUNTERPARTY_TYPES)
    counterparty_property = CharField(null=True, max_length=255, default='Recipient')

    ref = CharField('Идентификатор', max_length=255, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name}'

    class Meta:
        verbose_name = ('Контрагент')
        verbose_name_plural = ('Контрагент')


class Delivery(Model):
    order = ForeignKey(Order, on_delete=CASCADE, related_name='delivery')
    ref = CharField(max_length=255)
    cost_on_site = CharField(max_length=255)
    estimated_delivery_date = CharField(max_length=255)
    int_doc_number = CharField(max_length=255)
    type_document = CharField(max_length=255)
    status = CharField(max_length=255)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))

    def update_status(self):
        status = getStatusDocuments([{"DocumentNumber": self.int_doc_number}]).json()
        status = status['data'][0]['Status']
        self.status = status
        self.save()

    def delete(self, *args, **kwargs):
        deleteDocument(self.int_doc_number)
        super(Delivery, self).delete(*args, **kwargs)

    def __str__(self):
        return f'{self.int_doc_number}'

    class Meta:
        verbose_name = ('Отправление')
        verbose_name_plural = ('Отправления')
