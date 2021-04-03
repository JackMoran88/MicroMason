from django.core.management.base import BaseCommand
import os
import json
import logging
from glob import glob
from django.core.files import File


from shop_settings.models import Slider, Slide

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('wb')

# PATH = os.path.abspath(os.getcwd())
PATH = os.path.join('data', 'sliders')
print(PATH)

class Command(BaseCommand):
    help = 'Загрузка слайдеров'

    def handle(self, **options):

        slider_paths = glob(f'{PATH}/*/')

        Slider.objects.all().delete()
        Slide.objects.all().delete()

        for slider_path in slider_paths:
            settings_path = f'{slider_path}settings.json'
            if not os.path.exists(settings_path): continue
            with open(settings_path, encoding='UTF-8') as json_file:
                settings = json.load(json_file)

                slider_data = {
                    'name': settings['name'],
                    'place': settings['place'],
                    'width': settings['width'],
                    'height': settings['height'],
                }
                slider = Slider.objects.create(**slider_data)

                for num, slide_json in enumerate(settings['slides']):
                    if not glob(f'{slider_path}{slide_json["img"]}.*')[0]: continue
                    slide_json['img'] = glob(f'{slider_path}{slide_json["img"]}.*')[0]
                    slide_json['img'] = os.path.abspath(slide_json['img'])
                    slide_data = {
                        'title': slide_json['title'],
                        'image': slide_json['img'],
                        'url': slide_json['url'],
                    }
                    slide = Slide.objects.create(**slide_data)
                    slide.image.save(f'Slider#{slider.id}', File(open(slide_json['img'], 'rb')))
                    slider.slides.add(slide)

                logger.info(f'{slider_path} loaded')

