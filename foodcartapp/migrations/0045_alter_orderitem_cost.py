# Generated by Django 3.2.15 on 2023-02-18 15:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_auto_20230218_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Стоимость'),
        ),
    ]
