# Generated by Django 3.1.2 on 2020-11-17 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0014_auto_20201117_1127'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rating',
            new_name='Review',
        ),
    ]
