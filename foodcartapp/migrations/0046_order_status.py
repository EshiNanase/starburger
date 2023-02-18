# Generated by Django 3.2.15 on 2023-02-18 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0045_alter_orderitem_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Contacting client', 'Необработан'), ('Packing order', 'Собирается'), ('Delivering order', 'В процессе доставки'), ('Successfully delivered', 'Доставлен')], default='Contacting client', max_length=256, verbose_name='Статус заказа'),
        ),
    ]
