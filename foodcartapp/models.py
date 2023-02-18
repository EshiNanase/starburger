import requests
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator
from django.utils import timezone
from geopy import distance
from restaurateur.ya import fetch_coordinates

# FIXME
from star_burger.settings import YANDEX_API_TOKEN


STATUS_CHOICES = (
    ('Contacting client', 'Необработан'),
    ('Packing order', 'Собирается'),
    ('Delivering order', 'В процессе доставки'),
    ('Successfully delivered', 'Доставлен')
)

PAYMENT_CHOICES = (
    ('Cash', 'Наличность'),
    ('Card', 'Карта')
)


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):

    def count_cost(self):
        queryset = self.annotate(cost=models.Sum(models.F('items__cost')*models.F('items__quantity')))
        return queryset


class Order(models.Model):
    firstname = models.CharField(
        blank=False,
        max_length=256,
        verbose_name='Имя'
    )
    lastname = models.CharField(
        blank=False,
        max_length=256,
        verbose_name='Фамилия'
    )
    phonenumber = PhoneNumberField(
        null=False,
        max_length=256,
        verbose_name='Телефон'
    )
    address = models.CharField(
        blank=False,
        max_length=256,
        verbose_name='Адрес'
    )
    status = models.CharField(
        blank=False,
        choices=STATUS_CHOICES,
        default='Contacting client',
        max_length=256,
        verbose_name='Статус заказа',
        db_index=True
    )
    comment = models.CharField(
        blank=True,
        max_length=256,
        verbose_name='Комментарий'
    )
    register_time = models.DateTimeField(
        null=False,
        blank=False,
        db_index=True,
        default=timezone.now,
        verbose_name='Зарегистрирован в'
    )
    contact_time = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Согласован в'
    )
    delivery_time = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Доставлен в'
    )
    payment = models.CharField(
        blank=False,
        choices=PAYMENT_CHOICES,
        default='Card',
        max_length=256,
        verbose_name='Оплата',
        db_index=True
    )
    restaurant = models.ForeignKey(
        null=True,
        to=Restaurant,
        on_delete=models.SET_NULL,
        verbose_name='Ресторан'
    )

    objects = OrderQuerySet.as_manager()

    def find_restaurant(self):
        restaurants = Restaurant.objects.prefetch_related('menu_items__product')

        restaurant_products_available = {}
        for restaurant in restaurants:
            restaurant_products_available[restaurant] = []
            for item in restaurant.menu_items.all():
                if item.availability:
                    restaurant_products_available[restaurant].append(item.product.id)

        restaurants_availibility = {}
        for restaurant in restaurant_products_available:
            order_item_ids = [product.product.id for product in self.items.prefetch_related('product')]
            if all(item in restaurant_products_available[restaurant] for item in order_item_ids):

                try:
                    client_coordinates = fetch_coordinates(YANDEX_API_TOKEN, self.address)[::-1]
                except requests.RequestException:
                    return 'Invalid data'
                restaurant_coordinates = fetch_coordinates(YANDEX_API_TOKEN, restaurant.address)[::-1]
                distance_between_client_restaurant = distance.distance(restaurant_coordinates, client_coordinates).km

                restaurants_availibility[restaurant.name] = round(distance_between_client_restaurant, 2)
        return sorted(restaurants_availibility.items(), key=lambda x: x[1])

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname}: {self.address}'


class OrderItem(models.Model):
    product = models.ForeignKey(
        null=False,
        to=Product,
        verbose_name='Товар',
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        null=False,
        default=1,
        verbose_name='Количество',
    )
    order = models.ForeignKey(
        null=False,
        to=Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='items'
    )
    cost = models.DecimalField(
        null=False,
        default=0,
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Стоимость'
    )

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f'{self.product.name} - {self.order}'
