from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):

    def test_view(self):  # обязательно начинать с test_...
        path = reverse('index')  # index - http://127/0.0.1:8000/
        response = self.client.get(path)  # self.client.get - позволяет создать get запрос

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


