# Generated by Django 3.1.2 on 2021-02-15 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20201225_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
