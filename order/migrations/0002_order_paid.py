# Generated by Django 3.1.2 on 2020-12-13 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.CharField(choices=[('0', 'Не оплачено'), ('1', 'Ожидается оплата'), ('2', 'Оплачено')], default=1, max_length=255),
            preserve_default=False,
        ),
    ]
