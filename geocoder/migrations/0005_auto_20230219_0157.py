# Generated by Django 3.2.15 on 2023-02-18 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geocoder', '0004_auto_20230219_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressclient',
            name='latitude',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='addressclient',
            name='longitude',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30, verbose_name='Долгота'),
        ),
        migrations.AlterField(
            model_name='addressrestaurant',
            name='latitude',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='addressrestaurant',
            name='longitude',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30, verbose_name='Долгота'),
        ),
    ]
