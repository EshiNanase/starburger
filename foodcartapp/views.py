from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import phonenumbers

from .models import Product, Order, OrderItem


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


@api_view(['POST'])
def register_order(request):
    data = request.data

    if data.get('products') is None:
        return Response({'error': 'products key not presented or null'}, status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(data['products'], list):
        return Response({'error': 'products key is not list'}, status=status.HTTP_400_BAD_REQUEST)

    if not data['products']:
        return Response({'error': 'products key cant be empty'}, status=status.HTTP_400_BAD_REQUEST)

    if None in data.values():
        return Response(
            {'error': f'{", ".join([key for key in data.keys() if data[key] is None])} cant be empty'},
            status=status.HTTP_400_BAD_REQUEST)

    if len(data) != 5 or "" in data.values():
        return Response(
            {'error': 'five keys need to be presented and they cant be empty: products, firstname, lastname, address, phonenumber'},
            status=status.HTTP_400_BAD_REQUEST)

    phone_number = phonenumbers.parse(data['phonenumber'])
    if not phonenumbers.is_valid_number(phone_number):
        return Response({'error': 'phonenumber key not valid'}, status=status.HTTP_400_BAD_REQUEST)

    str_check = [key for key in data if key != 'products' and isinstance(data[key], str)]
    if str_check:
        return Response(
            {'error': f'{", ".join(str_check)} need to be str'},
            status=status.HTTP_400_BAD_REQUEST)

    products = Product.objects.all()
    for product in data['products']:
        if not products.filter(id=product['product']):
            return Response({'error': 'product key not possible'}, status=status.HTTP_400_BAD_REQUEST)

    order = Order.objects.create(
        first_name=data['firstname'],
        last_name=data['lastname'],
        phone_number=data['phonenumber'],
        address=data['address'],
    )

    for product in data['products']:
        OrderItem.objects.create(
            product=Product.objects.get(id=product['product']),
            quantity=product['quantity'],
            order=order
        )
    return Response(status.HTTP_200_OK)
