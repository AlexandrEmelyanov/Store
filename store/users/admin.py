from django.contrib import admin
from .models import User
from products.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email')
    inlines = (BasketAdmin,)  # для отображения списка товаров в корзине сразу в админке пользователя
