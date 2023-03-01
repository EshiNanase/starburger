import requests
from django.conf import settings
from geocoder.models import Address


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def set_coordinates(address_id):
    address = Address.objects.get(id=address_id)
    try:
        coordinates = fetch_coordinates(settings.YANDEX_API_TOKEN, address.address)[::-1]
    except TypeError:
        coordinates = (None, None)
    address.latitude, address.longitude = coordinates
    address.save()
