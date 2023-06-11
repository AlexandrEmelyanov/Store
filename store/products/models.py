from django.db import models

from users.models import User

# Create your models here.

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


class BasketQuerySet(models.QuerySet):
    def total_sum(self):  # этот self - уже будет обращение ко всему классу (ко всем объектам класса)
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


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
