# Generated by Django 3.1.2 on 2020-11-19 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0025_auto_20201119_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionproduct',
            name='parameter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parameter', to='basepage.option'),
        ),
    ]
