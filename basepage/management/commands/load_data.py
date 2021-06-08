from django.core.management.base import BaseCommand
from django.core.files import File
from product.models import Product, Brand, ProductImage, Option, OptionProduct
from basepage.models import Category
from category.models import Filter
import copy
# from django.core.management.base import BaseCommand

# from product.models import Product, Option, OptionProduct
# from basepage.models import Category
# import copy
import os
import logging
import csv
import urllib.request
import slugify
import ast

from django.db import models
from django.core.files import File
from urllib.request import urlopen, Request
from tempfile import NamedTemporaryFile

PATH = {
    'type': 'csv',
    'dir': 'data',
    'files': {
        'category': 'category',
        'product': 'product',
        'option': 'option',
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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wb')

SETTINGS = {
    'product': {
        'clear': 0,
        'product': 1,
        'image': 1,
        'images': 1,
    },
    'category': {
        'clear': 0,
        'category': 0,
        'image': 0,
    },
    'option': {
        'clear': 0,
    },
}

ROWS = [1, 2, 3]

opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'whatever')


class Command(BaseCommand):
    help = 'Спарсить фильтры'

    def handle(self, **options):
        load_path()

        if SETTINGS['category']['category']:
            with open(PATH['files']['category'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)

                if SETTINGS['category']['clear']:
                    Category.objects.all().delete()

                for string in csv_dict_reader:

                    if not (Category.objects.filter(name=string['name'])):
                        if string['parent']:
                            parent = Category.objects.filter(name=string['parent']).first()
                            row = None
                            if parent.parent is None:
                                children = Category.objects.filter(parent=parent)
                                row = get_row(len(children))

                        else:
                            parent = None
                            row = None
                        logger.debug(f'PARENT: {parent}')

                        data = {
                            'parent': parent,
                            'name': string['name'],
                            'description': string['description'],
                            'row': row,
                        }

                        category = Category.objects.create(**data)

                        if string['img'] and SETTINGS['category']['image']:
                            img = NamedTemporaryFile(delete=True)
                            r = Request(string['img'], headers={'User-Agent': 'Mozilla/5.0'})
                            img.write(urlopen(r).read())
                            img.flush()
                            category.main_image.save(f"image_{category.id}", File(img))

                        logger.info(f'{data["name"]} сохранен')
        if SETTINGS['product']['product']:
            with open(PATH['files']['product'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)

                if SETTINGS['product']['clear']:
                    Product.objects.all().delete()

                if SETTINGS['option']['clear']:
                    Option.objects.all().delete()

                for string in csv_dict_reader:

                    category = Category.objects.filter(name=string['category']).first()

                    if not category:
                        logger.info(f"Не найдена категория для {string['name']}")
                        continue

                    brand = Brand.objects.filter(name=string['brand']).first()
                    if brand is None:
                        brand = Brand.objects.create(name=string['brand'])

                    if not (Product.objects.filter(name=string['name'])):
                        data = {
                            'name': string['name'],
                            'brand': brand,
                            'code': string['code'],
                            'quantity': string['quantity'],
                            'price': int(float(string['price'])),
                            'description': string['description'],
                            'category': category,
                            'status': string['status'],
                        }

                        try:
                            product = Product.objects.create(**data)
                        except:
                            continue

                        if string['main_img'] and SETTINGS['product']['image']:
                            img = NamedTemporaryFile(delete=True)
                            r = Request(string['main_img'], headers={'User-Agent': 'Mozilla/5.0'})
                            img.write(urlopen(r).read())
                            img.flush()
                            product.main_image.save(f"image_{product.id}.jpg", File(img))

                        if string['images'] and SETTINGS['product']['images']:
                            imgs = ast.literal_eval(string['images'])
                            for item in imgs:
                                img = NamedTemporaryFile(delete=True)
                                r = Request(item, headers={'User-Agent': 'Mozilla/5.0'})
                                img.write(urlopen(r).read())
                                img.flush()
                                ProductImage.objects.create(product_id=product).image.save(f"image_{product.id}.jpg",
                                                                                           File(img))

                        if string['options']:
                            options = ast.literal_eval(string['options'])
                            for option in options:

                                cur_option = Option.objects.filter(name=option['name']).first()
                                if cur_option is None:
                                    cur_option = Option.objects.create(name=option['name'],
                                                                       request_name=slugify.slugify(option['name']))
                                cur_option.category.add(category)

                                OptionProduct.objects.create(name=option['parameter'], parameter=cur_option,
                                                             product=product)
                        logger.info(f'{data["name"]} сохранен')
