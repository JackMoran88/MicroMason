# Generated by Django 3.1.2 on 2021-03-10 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('_novaposhta', '0002_auto_20210310_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery', to='order.order'),
        ),
    ]
