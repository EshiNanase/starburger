from django.contrib import admin
from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ['filled_at']

    class Meta:
        model = Address

    def save_model(self, request, obj, form, change):
        obj.set_coordinates()
        obj.save()
        super(AddressAdmin, self).save_model(request, obj, form, change)

