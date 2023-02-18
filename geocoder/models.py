from django.db import models
from geocoder.ya_utils import fetch_coordinates
from star_burger.settings import YANDEX_API_TOKEN
from django.utils import timezone


class AddressClient(models.Model):

    address = models.CharField(
        blank=False,
        max_length=256,
        verbose_name='Адрес'
    )
    latitude = models.DecimalField(
        null=False,
        default=0,
        max_digits=30,
        decimal_places=15,
        verbose_name='Широта'
    )
    longitude = models.DecimalField(
        null=False,
        default=0,
        max_digits=30,
        decimal_places=15,
        verbose_name='Долгота'
    )
    date_fill = models.DateTimeField(
        null=False,
        blank=False,
        default=timezone.now,
        db_index=True,
        verbose_name='Дата создания'
    )

    def set_coordinates(self):
        coordinates = fetch_coordinates(YANDEX_API_TOKEN, self.address)[::-1]
        self.latitude = coordinates[0]
        self.longitude = coordinates[1]

    class Meta:
        verbose_name = 'Адрес клиента'
        verbose_name_plural = 'Адреса клиентов'

    def __str__(self):
        return f'{self.address}'


class AddressRestaurant(models.Model):

    name = models.CharField(
        blank=False,
        max_length=256,
        verbose_name='Название'
    )

    address = models.CharField(
        blank=False,
        max_length=256,
        verbose_name='Адрес'
    )
    latitude = models.DecimalField(
        null=False,
        default=0,
        max_digits=30,
        decimal_places=15,
        verbose_name='Широта'
    )
    longitude = models.DecimalField(
        null=False,
        default=0,
        max_digits=30,
        decimal_places=15,
        verbose_name='Долгота'
    )
    date_fill = models.DateTimeField(
        null=False,
        blank=False,
        default=timezone.now,
        db_index=True,
        verbose_name='Дата создания'
    )

    def set_coordinates(self):
        coordinates = fetch_coordinates(YANDEX_API_TOKEN, self.address)[::-1]
        self.latitude = coordinates[0]
        self.longitude = coordinates[1]

    class Meta:
        verbose_name = 'Адрес ресторана'
        verbose_name_plural = 'Адреса ресторанов'

    def __str__(self):
        return f'{self.name}'
