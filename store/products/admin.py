from django.contrib import admin

from products.models import Basket, ProductCategory, Products

admin.site.register(ProductCategory)


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'category']
    fields = ('name', ('price', 'quantity'), 'category', 'image', 'stripe_product_price_id', 'description')
    search_fields = ('name',)
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0
