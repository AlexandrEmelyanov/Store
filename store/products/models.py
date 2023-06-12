import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)  # CharField - для небольшого текста
    description = models.TextField(null=True, blank=True)  # TextField - для текста любого объема

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'  # Для отображение имени в django admin
        verbose_name_plural = 'Categories'


class Products(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')  # указывается куда сохраняются images
    # в on_delete PROTECT - категорию нельзя будут удалить пока не будут удалены все продукты данной
    # CASCADE - при удалении категории к которой привязаны продукты, будет запрашиваться подтверждение на удаление
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'

    class Meta:
        verbose_name = 'Product'  # Для отображение имени в django admin
        verbose_name_plural = 'Products'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Products, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),  # т.к. price хранящаяся DecimalField, должна быть округлена до копеек
            currency='rub'
        )
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):  # этот self - уже будет обращение ко всему классу (ко всем объектам класса)
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связываем столбец с id users
    product = models.ForeignKey(Products, on_delete=models.CASCADE)  # связываем столбец с id продукта
    quantity = models.PositiveIntegerField(default=0)

    created_timestamp = models.DateTimeField(auto_now_add=True)
    # DateTimeField - метод для отображения даты
    # auto_now_add - автоматически будет заполняться при создании нового объекта

    objects = BasketQuerySet.as_manager()  # говорим обращаться к созданному классу как к менеджеру

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item
