from django.core.management.base import BaseCommand

from product.models import Product
from basepage.models import Category
from category.models import Filter
import copy



class Command(BaseCommand):
    help = 'Спарсить фильтры'

    def handle(self, **options):

        parent = Category.objects.get(name='Ноутбуки и компьютеры')
        data = {
            'name': 'Удалить',
            'parent_id': parent.id,
        }
        Category.objects.create(**data)