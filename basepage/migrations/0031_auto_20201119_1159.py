# Generated by Django 3.1.2 on 2020-11-19 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0030_footer_settings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settings',
            name='footer',
        ),
        migrations.DeleteModel(
            name='Footer',
        ),
        migrations.DeleteModel(
            name='Settings',
        ),
    ]
