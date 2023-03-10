# Generated by Django 3.2.15 on 2023-02-26 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geocoder', '0010_remove_address_bad_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=30, null=True, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=15, max_digits=30, null=True, verbose_name='Долгота'),
        ),
    ]
