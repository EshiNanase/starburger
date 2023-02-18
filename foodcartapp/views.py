from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer

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

    serializer = OrderSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    order = Order.objects.create(
        firstname=data['firstname'],
        lastname=data['lastname'],
        phonenumber=data['phonenumber'],
        address=data['address'],
        cost=0
    )

    for product in data['products']:
        order_item = OrderItem.objects.create(
            product=Product.objects.get(id=product['product']),
            quantity=product['quantity'],
            order=order,
            cost=0
        )
        order_item.cost = order_item.set_cost()
        order_item.save()

    order.cost = order.get_cost()
    order.save()

    serializer_data = serializer.data
    serializer_data['id'] = order.id

    return Response(serializer_data)
