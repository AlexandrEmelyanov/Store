from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import ProductCategory, Products


class IndexViewTestCase(TestCase):

    def test_view(self):  # обязательно начинать с test_...
        path = reverse('index')  # index - http://127/0.0.1:8000/
        response = self.client.get(path)  # self.client.get - позволяет создать get запрос

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json']  # при создании тестовой БД, она будет заполняться этими данными

    def setUp(self):
        self.products = Products.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )

    def _common_test(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
