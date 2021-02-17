import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicroMason.settings')
django.setup()


from product.models import Product

print(Product.objects.all())



# Python manage.py shell < db/filters.py