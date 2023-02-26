from django.contrib import admin
from django.shortcuts import reverse, redirect
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import iri_to_uri
from datetime import datetime

from .models import Product
from .models import ProductCategory
from .models import Restaurant
from .models import RestaurantMenuItem
from .models import Order
from .models import OrderItem
from geocoder.models import Address


class RestaurantMenuItemInline(admin.TabularInline):
    model = RestaurantMenuItem
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'address',
        'contact_phone',
    ]
    list_display = [
        'name',
        'address',
        'contact_phone',
    ]
    inlines = [
        RestaurantMenuItemInline
    ]

    def save_model(self, request, obj, form, change):
        updated_values = {'address': obj.address}
        address, created = Address.objects.update_or_create(
            name=obj.name,
            defaults=updated_values
        )
        address.set_coordinates()
        address.save()
        super(RestaurantAdmin, self).save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'get_image_list_preview',
        'name',
        'category',
        'price',
    ]
    list_display_links = [
        'name',
    ]
    list_filter = [
        'category',
    ]
    search_fields = [
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        'name',
        'category__name',
    ]

    inlines = [
        RestaurantMenuItemInline
    ]
    fieldsets = (
        ('Общее', {
            'fields': [
                'name',
                'category',
                'image',
                'get_image_preview',
                'price',
            ]
        }),
        ('Подробно', {
            'fields': [
                'special_status',
                'description',
            ],
            'classes': [
                'wide'
            ],
        }),
    )

    readonly_fields = [
        'get_image_preview',
    ]

    class Media:
        css = {
            "all": (
                static("admin/foodcartapp.css")
            )
        }

    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)
    get_image_preview.short_description = 'превью'

    def get_image_list_preview(self, obj):
        if not obj.image or not obj.id:
            return 'нет картинки'
        edit_url = reverse('admin:foodcartapp_product_change', args=(obj.id,))
        return format_html('<a href="{edit_url}"><img src="{src}" style="max-height: 50px;"/></a>', edit_url=edit_url, src=obj.image.url)
    get_image_list_preview.short_description = 'превью'


@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    pass


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemAdmin]
    list_display = ['__str__', 'phonenumber', 'status', 'get_cost']
    fieldsets = (
        (
            None, {'fields': (
                'firstname', 'lastname', 'phonenumber', 'address', 'bad_address', 'comment', 'status', 'payment', 'get_cost', 'cooking_restaurant', ('registered_at', 'delivered_at', 'contacted_at',)
            )
            }
        ),
    )
    readonly_fields = ['get_cost']

    def get_cost(self, obj):
        cost = 0
        for item in obj.items.all():
            cost += item.cost*item.quantity
        return cost

    get_cost.short_description = 'Итоговая сумма'

    def save_model(self, request, obj, form, change):
        if obj.cooking_restaurant and obj.status == 'Contacting client':
            obj.status = 'Packing order'
        if obj.status != 'Contacting client' and not obj.contacted_at:
            obj.contacted_at = datetime.now()
        address, created = Address.objects.get_or_create(
            address=obj.address
        )
        if created:
            address.set_coordinates()
            address.save()
        super(OrderAdmin, self).save_model(request, obj, form, change)

    def response_post_save_change(self, request, obj):
        res = super().response_post_save_change(request, obj)
        if "next" in request.GET and url_has_allowed_host_and_scheme(request.GET['next'], None):
            url = iri_to_uri(request.GET['next'])
            return redirect(url)
        else:
            return res

