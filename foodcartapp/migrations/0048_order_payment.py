# Generated by Django 3.2.15 on 2023-02-18 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_auto_20230218_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('Contacting client', 'Необработан'), ('Packing order', 'Собирается'), ('Delivering order', 'В процессе доставки'), ('Successfully delivered', 'Доставлен')], db_index=True, default='Card', max_length=256, verbose_name='Оплата'),
        ),
    ]