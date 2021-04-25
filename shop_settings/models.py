from django.db.models import Model, CASCADE
from django.db.models import CharField, FloatField, TextField, PositiveIntegerField, EmailField, DateTimeField
from django.db.models import DateField, BooleanField
from django.db.models import ManyToManyField, ForeignKey
from django.db.models import ImageField
from versatileimagefield.fields import VersatileImageField, PPOIField


class Footer(Model):
    name = CharField(max_length=255)
    description = CharField(max_length=20000, null=True, blank=True)

    class Meta:
        verbose_name = 'Пункт футера'
        verbose_name_plural = 'Пункты футера'

    def __str__(self):
        return f'{self.name}'


class Setting(Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    title = CharField(max_length=150)
    description = CharField(max_length=150, null=True, blank=True)
    phone = CharField(max_length=15)
    email = CharField(max_length=50, null=True, blank=True)

    footer = ManyToManyField(Footer)

    instagram = CharField(max_length=100, null=True, blank=True)
    telegram = CharField(max_length=100, null=True, blank=True)
    youtube = CharField(max_length=100, null=True, blank=True)
    status = CharField(max_length=10, choices=STATUS)

    meta_description = CharField(max_length=5000, null=True, blank=True)
    meta_keywords = CharField(max_length=5000, null=True, blank=True)

    create_at = DateTimeField(auto_now_add=True)
    update_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Настройка магазина'
        verbose_name_plural = 'Настройки магазина'

    def __str__(self):
        return f'{self.title}'


class ProductSortType(Model):
    name = CharField(max_length=50)
    field = CharField(max_length=50)
    order = PositiveIntegerField(null=True, blank=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Сортировка товаров'
        verbose_name_plural = 'Сортировки товаров'

    def __str__(self):
        return f'{self.name}'


class Slide(Model):
    title = CharField(max_length=255, null=True, blank=True)
    image = VersatileImageField("Слайд", upload_to="Slides/", blank=True, ppoi_field='slide_ppoi')
    slide_ppoi = PPOIField()

    url = CharField(max_length=1000, blank=True, null=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    def __str__(self):
        return f'{self.title}'

class Slider(Model):
    name = CharField(max_length=255)
    slides = ManyToManyField(Slide)
    place = CharField(max_length=255)
    width = PositiveIntegerField()
    height = PositiveIntegerField()

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдеры'

    def __str__(self):
        return f'{self.name} -  {self.place}'
