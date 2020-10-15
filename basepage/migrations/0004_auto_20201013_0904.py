# Generated by Django 3.1.2 on 2020-10-13 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0003_auto_20201013_0834'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=160, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
