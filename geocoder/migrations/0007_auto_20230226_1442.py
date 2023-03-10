# Generated by Django 3.2.15 on 2023-02-26 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geocoder', '0006_auto_20230226_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.DecimalField(decimal_places=15, max_digits=30, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.DecimalField(decimal_places=15, max_digits=30, verbose_name='Долгота'),
        ),
    ]
