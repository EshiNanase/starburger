from django.db import models
from django.utils import timezone


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

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.address
