# Generated by Django 3.1.2 on 2021-01-07 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_auto_20210107_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filter',
            name='model',
        ),
        migrations.RemoveField(
            model_name='filter',
            name='output',
        ),
        migrations.RemoveField(
            model_name='filter',
            name='parameter',
        ),
    ]
