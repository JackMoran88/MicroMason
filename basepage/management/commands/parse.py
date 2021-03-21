# from django.core.management.base import BaseCommand

# from product.models import Product, Option, OptionProduct
# from basepage.models import Category
# import copy
import os
import logging
import requests
import collections
import bs4
import csv
import lxml

SETTINGS = {
    'parse': {
        'category': 0,
        'product': 1,
    }
}

PATH = {
    'type': 'csv',
    'dir': 'D:\OpenServer\OSPanel\domains\MicroMason\data',
    'files': {
        'category': 'category',
        'product': 'product',
        'option': 'option',
    }
}

SKIP_CATEGORY = ['Товары для детей', 'Детская одежда', 'Рыбалка', 'Туризм и кемпинг', 'Печать, расходные']


def load_path():
    PATH.get('dir')
    for file in PATH['files']:
        PATH['files'][file] = os.path.join(PATH['dir'], f'{PATH["files"][file]}.{PATH["type"]}')


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')


def dict_by_value(arr, v):
    for num, item in enumerate(arr):
        for key, value in item.items():
            if value == v:
                return arr[num]


# class Command(BaseCommand):
#     help = 'Спарсить фильтры'
#
#     def handle(self, **options):
class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'Accept-Language': 'ru',
        }

        self.headers = [
            'Категория'
        ]

        self.result = {
            'category': [
                # {
                # 'name': '',
                # 'img': '',
                # 'parent': '',
                # 'children': '',
                # 'url': '',
                # }
            ],
            'product': [
                # {
                # 'name': '',
                # 'brand': '',
                # 'code': '',
                # 'quantity': '',
                # 'main_img': '',
                # 'images': '',
                # 'description': '',
                # 'category': '',
                # 'status': '',
                # 'url': '',
                # }
            ],
        }

    def load_page(self, url):
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        body = soup.select('body')[0]
        return body

    def save_result(self, file):
        path = PATH['files'][file]
        logger.info('Сохранение...')
        logger.debug(f'Путь сохраниния: {path}')

        # for result_key in self.result:
        for row in self.result[file]:
            keys = row.keys()
            with open(path, 'w', newline='', encoding="utf-8") as f:
                dict_writer = csv.DictWriter(f, keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.result[file])

        logger.info('Сохранение завершено.')

    def parse_categories(self, block):
        container = block.select('.case.container > .portal-class')

        for item in container:
            category_lvl_1 = item.findAll('a', {'class': 'portal-link'})[0]
            category_lvl_1__name = category_lvl_1.find('h2', {'class': 'heading-thick'}).text
            category_lvl_1__url = category_lvl_1['href']

            if category_lvl_1__name in SKIP_CATEGORY:
                logger.info(f'{category_lvl_1__name} - skipped')
                break

            self.result['category'].append({
                'name': category_lvl_1.find('h2', {'class': 'heading-thick'}).text,
                'description': '',
                'img': '',
                'url': category_lvl_1__url,
                'children': [],
                'parent': '',
            })

            category_lvl_2 = item.findAll('div', {'class': 'verbose-item'})

            for item2 in category_lvl_2:
                category_lvl_2__name = item2.find('a', {'class': 'drops-caption'}).text
                category_lvl_2__img = item.find('a', {'class': 'portal-img'}).find('img')['data-observe-src']
                category_lvl_2__url = item2.find('a', {'class': 'drops-caption'})['href']
                self.result['category'].append({
                    'name': category_lvl_2__name,
                    'parent': category_lvl_1__name,
                    'description': '',
                    'img': category_lvl_2__img,
                    'children': [],
                    'url': category_lvl_2__url,
                })

                category_lvl_3 = item2.find('ul', {'class': 'list-smaller'}).findAll('li')

                for item3 in category_lvl_3:
                    category_lvl_3__name = item3.find('a').text
                    category_lvl_3__url = item3.find('a')['href']
                    self.result['category'].append({
                        'name': category_lvl_3__name,
                        'parent': category_lvl_2__name,
                        'description': '',
                        'img': '',
                        'children': [],
                        'url': category_lvl_3__url,
                    })

        self.save_result('category')

    def parse_products(self, path, page=1, max_page=1):
        if page >= 2:
            text = self.load_page(f'{path}page={page}/')
        else:
            text = self.load_page(path)

        logger.info(f'PAGE: {page}')

        body = self.parse_page(text=text)
        stuffs = body.select('.catalog__content .stuff')

        if stuffs and page <= max_page:
            product_urls = []
            for stuff in stuffs:
                stuff_block = stuff.find('a', {'class': 'to_product'})
                if stuff_block:
                    product_urls.append(stuff_block['href'])

            for url in product_urls:
                logger.debug(url)

                url = f'https://www.itbox.ua{url}'
                text = self.load_page(url)
                body = self.parse_page(text=text)

                product = body.select('section.product')[0]

                status = product.find('strong', {'class': 'stuff-price__digits no_product'})

                # IMG
                image_blocks = product.findAll('a', {'class': ['stuff-img', 'slick-slide']})
                images = []
                for image in image_blocks:
                    if image.has_attr('data-img-big'):
                        images.append(image['data-img-big'])
                images = list(set(images))
                # !IMG!

                # OPTION
                option_block = product.find('div', {'class': 'characteristics'})

                try:
                    option_lines = option_block.findAll('tr')
                except:
                    option_lines = None

                options = []
                options.append({
                    'name': 'Производитель',
                    'parameter': product['data-vendor'],
                })

                if option_lines:
                    for option in option_lines:
                        options.append({
                            'name': option.findAll('td')[0].text,
                            'parameter': option.findAll('td')[1].text,
                        })

                self.result['product'].append(
                    {
                        'name': product['data-name'],
                        'brand': product['data-vendor'],
                        'code': product['data-product-code'],
                        'price': product['data-price'],
                        'quantity': 10,
                        'main_img': images[0],
                        'images': images,
                        'description': product.find('div', {'class': 'product-desc'}).decode_contents(),
                        'category': product['data-category-name'],
                        'status': 0 if status else 1,
                        'url': url,

                        'options': options,
                    }
                )
            self.save_result('product')

            self.parse_products(path=path, page=page + 1)
        else:
            logger.info(f'Парсинг закончен на странице {page - 1}')
            return

    def parse_block(self, block):
        if SETTINGS['parse']['category']:
            logger.info('Запуск парсинга категорий')
            self.parse_categories(block)
            logger.info('Конец парсинга категорий')
        if SETTINGS['parse']['product']:
            logger.info('Запуск парсинга продуктов')
            with open(PATH['files']['category'], 'r', encoding='utf-8') as read_obj:
                csv_dict_reader = csv.DictReader(read_obj)
                for row in csv_dict_reader:
                    self.parse_products(path=f'https://www.itbox.ua/{row["url"]}')
            logger.info('Конец парсинга продуктов')

    def run(self):
        load_path()
        text = self.load_page('https://www.itbox.ua/ru/catalog/')
        self.parse_block(block=self.parse_page(text=text))


if __name__ == '__main__':
    parser = Parser()
    parser.run()
