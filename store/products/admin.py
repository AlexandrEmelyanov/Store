from django.contrib import admin

from products.models import Basket, ProductCategory, Products

# Register your models here.

admin.site.register(ProductCategory)


@admin.register(Products)  # перед началом указываем с какой моделью будет работать этот класс
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'category']  # отображение в таблице столбцов
    fields = ('name', ('price', 'quantity'), 'category', 'image', 'description')  # поля которые можно редактировать
    # использование вложенного кортежа позволяет в редактировании, чтобы отображались на одной строке
    # также можно менять порядок - в каком порядке передадим в таком будут отображаться при редактировании (создании)
    # readonly_fields = ('description',)  # доступ к переменной только для чтения (нельзя редактировать)
    search_fields = ('name', )  # поисковая строка (в которой указывается по каким полям будет идти поиск)
    ordering = ('name', )  # сортировка отображения (отображение в алфавитном порядке по имени например


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0  # дополнительные пустые поля отображения товаров в корзине
