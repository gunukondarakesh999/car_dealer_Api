from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Car

class CarsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.car1 = Car.objects.create(name='Model S', brand='Tesla', price=79999.99)
        self.car2 = Car.objects.create(name='Model 3', brand='Tesla', price=49999.99)

    def test_get_all_cars(self):
        response = self.client.get('/api/cars/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Model S')


from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from .models import Car
from django.core.cache import cache

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class CarsAPITest(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.car1 = Car.objects.create(name='Model S', brand='Tesla', price=79999.99)

    def test_get_cars(self):
        response = self.client.get('/api/cars/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_car(self):
        data = {"name": "Model 3", "brand": "Tesla", "price": 49999.99, "available": True}
        response = self.client.post('/api/cars/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 2)

    def test_update_car(self):
        data = {"price": 75999.99}
        response = self.client.patch(f'/api/cars/{self.car1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car1.refresh_from_db()
        self.assertEqual(float(self.car1.price), 75999.99)

    def test_delete_car(self):
        response = self.client.delete(f'/api/cars/{self.car1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from .models import Car

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class CarsAPITest(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.car1 = Car.objects.create(name='Model S', brand='Tesla', price=79999.99)

    def test_get_cars(self):
        response = self.client.get('/api/cars/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_car(self):
        data = {"name": "Model 3", "brand": "Tesla", "price": 49999.99, "available": True}
        response = self.client.post('/api/cars/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 2)

    def test_update_car(self):
        data = {"price": 75999.99}
        response = self.client.patch(f'/api/cars/{self.car1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car1.refresh_from_db()
        self.assertEqual(float(self.car1.price), 75999.99)

    def test_delete_car(self):
        response = self.client.delete(f'/api/cars/{self.car1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Car.objects.count(), 0)
