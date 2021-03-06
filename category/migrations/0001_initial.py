# Generated by Django 3.1.2 on 2021-04-25 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basepage', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(blank=True, choices=[('0', 'default'), ('1', 'Type 1'), ('2', 'Type 2'), ('3', 'Type 3')], max_length=32, null=True)),
                ('request_name', models.CharField(blank=True, max_length=255)),
                ('model', models.CharField(blank=True, max_length=255, null=True)),
                ('filter', models.CharField(blank=True, max_length=255, null=True)),
                ('output', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_model', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_filter', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_output', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.BooleanField(default=False, verbose_name='Состояние')),
                ('order_by', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ManyToManyField(to='basepage.Category')),
                ('model_parameter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.option')),
            ],
            options={
                'verbose_name': 'Фильтр',
                'verbose_name_plural': 'Фильтры',
            },
        ),
    ]
