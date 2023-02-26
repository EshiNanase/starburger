from django.templatetags.static import static
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer
from django.conf import settings

from .models import Product, Order, OrderItem
from geocoder.models import Address
from geocoder.ya_utils import fetch_coordinates


@api_view(['GET'])
def banners_list_api(request):
    # FIXME move data to db?
    return Response([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ]
    )


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return Response(dumped_products)


@transaction.atomic
@api_view(['POST'])
def register_order(request):

    data = request.data

    serializer = OrderSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    order = Order.objects.create(
        firstname=data['firstname'],
        lastname=data['lastname'],
        phonenumber=data['phonenumber'],
        address=data['address'],
    )

    try:
        coordinates = fetch_coordinates(settings.YANDEX_API_TOKEN, order.address)[::-1]
    except TypeError:
        coordinates = (None, None)
    if False in coordinates:
        order.bad_address = True
        order.save()

        latitude = 0
        longitude = 0
    else:
        latitude, longitude = coordinates
    address, created = Address.objects.get_or_create(
        address=data['address'],
        latitude=latitude,
        longitude=longitude
    )
    address.save()

    for item in data['products']:
        product = Product.objects.get(id=item['product'])
        quantity = item['quantity']
        cost = product.price
        OrderItem.objects.create(
            product=product,
            quantity=quantity,
            order=order,
            cost=cost
        )

    serializer_data = serializer.data
    serializer_data['id'] = order.id

    return Response(serializer_data)
