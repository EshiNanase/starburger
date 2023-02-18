from django.contrib import admin
from .models import AddressClient, AddressRestaurant


@admin.register(AddressClient)
class AddressClientAdmin(admin.ModelAdmin):
    readonly_fields = ['date_fill']

    class Meta:
        model = AddressClient


@admin.register(AddressRestaurant)
class AddressShopClient(admin.ModelAdmin):
    readonly_fields = ['date_fill']

    class Meta:
        model = AddressRestaurant
