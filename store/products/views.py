from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Products, ProductCategory, Basket
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    context = {
        'title': 'Store',
    }
    return render(request, 'products/index.html', context=context)


def products(request, category_id=None, page_number=1):
    products = Products.objects.filter(category_id=category_id) if category_id else Products.objects.all()

    paginator = Paginator(object_list=products, per_page=3)
    products_paginator = paginator.page(page_number)

    context = {
        'title': 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
    }
    return render(request, 'products/products.html', context=context)


@login_required
def basket_add(request, product_id):
    product = Products.objects.get(id=product_id)
    # с помощью get отображаем что это за товар с переданным нам id

    baskets = Basket.objects.filter(user=request.user, product=product)
    # если у пользователя этот товар добавлен в корзину мы увеличим кол-во на 1, если нет, то добавим

    if not baskets.exists():  # exists() проверяет если ли какие-то переменные. Смотрим если корзина пустая то:
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:  # если корзина не пустая:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
