from django.core.management.base import BaseCommand
from _novaposhta.models import *

class Command(BaseCommand):
    help = 'Загрузить данный для Новой Почты'

    def handle(self, **options):
        warehouses = getWarehouses().json()
        warehouses = warehouses['data']
        Warehouse.objects.all().delete()
        for warehouse in warehouses:
            data = {
                'ref': warehouse['Ref'],

                'description': warehouse['DescriptionRu'],
                'description_ru': warehouse['DescriptionRu'],
                'description_uk': warehouse['Description'],

                'type_warehouse': warehouse['TypeOfWarehouse'],
                'number': warehouse['Number'],

                'city_description': warehouse['CityDescriptionRu'],
                'city_description_ru': warehouse['CityDescriptionRu'],
                'city_description_uk': warehouse['CityDescription'],
                'city_ref': warehouse['CityRef'],

            }
            Warehouse.objects.create(**data)

        cities = getCities().json()
        cities = cities['data']
        Cities.objects.all().delete()
        for city in cities:
            data = {
                'ref': city['Ref'],

                'description': city['DescriptionRu'],
                'description_ru': city['DescriptionRu'],
                'description_uk': city['Description'],

                'city_id': city['CityID'],
                'city_ref': city['Ref'],

                'area': city['Area'],
            }
            Cities.objects.create(**data)
