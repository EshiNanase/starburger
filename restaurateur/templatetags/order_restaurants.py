from django import template
from geocoder.models import Address
from foodcartapp.models import Restaurant
from geopy import distance
register = template.Library()


@register.simple_tag
def find_restaurant(order):
    restaurants = Restaurant.objects.prefetch_related('menu_items__product')

    restaurant_products_available = {}
    for restaurant in restaurants:
        restaurant_products_available[restaurant] = []
        for item in restaurant.menu_items.all():
            if item.availability:
                restaurant_products_available[restaurant].append(item.product.id)

    restaurants_availibility = {}
    for restaurant in restaurant_products_available:
        order_item_ids = [product.product.id for product in order.items.prefetch_related('product')]
        if all(item in restaurant_products_available[restaurant] for item in order_item_ids):

            client_address = Address.objects.get(address=order.address)
            client_coordinates = (client_address.latitude, client_address.longitude)
            if None in client_coordinates:
                return None

            restaurant_address = Address.objects.get(address=restaurant.address)
            restaurant_coordinates = (restaurant_address.latitude, restaurant_address.longitude)
            distance_between_client_restaurant = distance.distance(restaurant_coordinates, client_coordinates).km

            restaurants_availibility[restaurant.name] = round(distance_between_client_restaurant, 2)

    return sorted(restaurants_availibility.items(), key=lambda x: x[1])
