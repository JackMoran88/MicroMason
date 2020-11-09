# Generated by Django 3.1.2 on 2020-11-06 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0004_auto_20201106_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basepage.customergender'),
        ),
        migrations.AlterField(
            model_name='customergender',
            name='gender',
            field=models.CharField(default=1, max_length=20, verbose_name='Пол'),
            preserve_default=False,
        ),
    ]
