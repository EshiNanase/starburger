from django.db import models
from geocoder.ya_utils import fetch_coordinates
from django.utils import timezone
from django.conf import settings


class Address(models.Model):

    address = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Адрес'
    )
    latitude = models.DecimalField(
        blank=True,
        null=True,
        max_digits=30,
        decimal_places=15,
        verbose_name='Широта'
    )
    longitude = models.DecimalField(
        blank=True,
        null=True,
        max_digits=30,
        decimal_places=15,
        verbose_name='Долгота'
    )
    filled_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        verbose_name='Дата создания'
    )

    def set_coordinates(self):
        coordinates = fetch_coordinates(settings.YANDEX_API_TOKEN, self.address)[::-1]
        self.latitude, self.longitude = coordinates
        self.save()

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.address
