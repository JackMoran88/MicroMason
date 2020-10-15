# Generated by Django 3.1.2 on 2020-10-13 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0010_auto_20201013_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(blank=True, to='basepage.ProductImage'),
        ),
    ]
