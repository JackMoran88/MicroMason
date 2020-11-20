from django.db.models import Model, CASCADE
from django.db.models import CharField, FloatField, TextField, PositiveIntegerField, EmailField, DateTimeField
from django.db.models import DateField, BooleanField
from django.db.models import ManyToManyField, ForeignKey


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
    create_at = DateTimeField(auto_now_add=True)
    update_at = DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Настройка магазина'
        verbose_name_plural = 'Настройки магазина'

    def __str__(self):
        return f'{self.title}'