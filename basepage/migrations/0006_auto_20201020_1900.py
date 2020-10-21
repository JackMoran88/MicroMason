# Generated by Django 3.1.2 on 2020-10-20 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0005_auto_20201020_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wish', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wish',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basepage.product'),
        ),
    ]
