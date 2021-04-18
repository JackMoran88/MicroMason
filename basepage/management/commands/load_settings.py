from django.core.management.base import BaseCommand
from django.core.files import File
from product.models import Product, Brand, ProductImage, Option, OptionProduct
from basepage.models import Category, RatingStar, Customer
from category.models import Filter
from order.models import Shipping, Payment, OrderStatus
from _novaposhta.models import Counterparty
from shop_settings.models import ProductSortType, Setting, Footer
from oauth2_provider.models import Application

import copy
# from django.core.management.base import BaseCommand

# from product.models import Product, Option, OptionProduct
# from basepage.models import Category
# import copy
import os
import logging
import csv
import requests
import urllib.request
import slugify
import ast

from django.db import models
from django.core.files import File
from urllib.request import urlopen, Request
from tempfile import NamedTemporaryFile

PATH = {
    'type': 'csv',
    'dir': 'data/start',
    'files': {
        'RatingStar': 'RatingStar',
        'Shipping': 'Shipping',
        'Payment': 'Payment',
        'OrderStatus': 'OrderStatus',
        'ProductSortType': 'ProductSortType',
        'Setting': 'Setting',
        'Footer': 'Footer',
        'Application': 'Application',
        'NP_Counterparty': 'NP_Counterparty',
        'Managers': 'Managers',
    }
}


def load_path():
    PATH.get('dir')
    for file in PATH['files']:
        PATH['files'][file] = os.path.join(PATH['dir'], f'{PATH["files"][file]}.{PATH["type"]}')


def get_row(num):
    if len(ROWS) >= num:
        return ROWS[num - 1]
    else:
        num = num - len(ROWS)
        return get_row(num)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')

SETTINGS = {
    'RatingStar': {
        'load': 1,
    },
    'Shipping': {
        'load': 1,
    },
    'Payment': {
        'load': 1,
    },
    'OrderStatus': {
        'load': 1,
    },
    'ProductSortType': {
        'load': 1,
    },
    'Setting': {
        'load': 1,
    },
    'Footer': {
        'load': 1,
    },
    'Application': {
        'load': 1,
    },
    'NP_Counterparty': {
        'load': 1,
    },
    'Managers': {
        'load': 1,
    },
}


class Command(BaseCommand):
    help = 'Загрузка начальных настроек'

    def handle(self, **options):
        load_path()

        if SETTINGS['Managers']['load']:
            with open(PATH['files']['Managers'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                Counterparty.objects.all().delete()
                for string in csv_dict_reader:
                    Customer.objects.create_superuser(**string)

        if SETTINGS['RatingStar']['load']:
            with open(PATH['files']['RatingStar'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                RatingStar.objects.all().delete()
                for string in csv_dict_reader:
                    RatingStar.objects.create(**string)

        if SETTINGS['Shipping']['load']:
            with open(PATH['files']['Shipping'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                Shipping.objects.all().delete()
                for string in csv_dict_reader:
                    Shipping.objects.create(**string)

        if SETTINGS['Payment']['load']:
            with open(PATH['files']['Payment'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                Payment.objects.all().delete()
                for string in csv_dict_reader:
                    Payment.objects.create(**string)

        if SETTINGS['OrderStatus']['load']:
            with open(PATH['files']['OrderStatus'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                OrderStatus.objects.all().delete()
                for string in csv_dict_reader:
                    OrderStatus.objects.create(**string)

        if SETTINGS['ProductSortType']['load']:
            with open(PATH['files']['ProductSortType'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                ProductSortType.objects.all().delete()
                for string in csv_dict_reader:
                    ProductSortType.objects.create(**string)

        if SETTINGS['Setting']['load']:
            with open(PATH['files']['Setting'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                Setting.objects.all().delete()
                for string in csv_dict_reader:
                    Setting.objects.create(**string)

        if SETTINGS['Footer']['load']:
            with open(PATH['files']['Footer'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                Footer.objects.all().delete()
                for string in csv_dict_reader:
                    Footer.objects.create(**string)

        if SETTINGS['Application']['load']:
            with open(PATH['files']['Application'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                Application.objects.all().delete()
                for string in csv_dict_reader:
                    Application.objects.create(**string)

        if SETTINGS['NP_Counterparty']['load']:
            with open(PATH['files']['NP_Counterparty'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                Counterparty.objects.all().delete()
                for string in csv_dict_reader:
                    Counterparty.objects.create(**string)
