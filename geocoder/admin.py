from django.contrib import admin
from .models import Address
from geocoder.geocoder_utils import set_coordinates


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ['filled_at']

    class Meta:
        model = Address

    def save_model(self, request, obj, form, change):
        set_coordinates(obj.id)
        super(AddressAdmin, self).save_model(request, obj, form, change)

