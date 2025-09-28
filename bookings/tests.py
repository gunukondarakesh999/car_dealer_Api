from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
from cars.models import Car
from .models import Booking

class BookingsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user1', email='user1@example.com', password='test123')
        self.car = Car.objects.create(name='Model S', brand='Tesla', price=79999.99)
        self.booking = Booking.objects.create(user=self.user, car=self.car, status='confirmed')

    def test_get_all_bookings(self):
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'confirmed')

from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from users.models import CustomUser
from cars.models import Car
from .models import Booking
from django.core.cache import cache

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class BookingAPITest(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user1', email='user1@example.com', password='test123')
        self.car = Car.objects.create(name='Model S', brand='Tesla', price=79999.99)
        self.booking = Booking.objects.create(user=self.user, car=self.car, status='confirmed')

    def test_create_booking(self):
        data = {"user": self.user.id, "car": self.car.id, "status": "pending"}
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 2)

    def test_update_booking(self):
        data = {"status": "cancelled"}
        response = self.client.patch(f'/api/bookings/{self.booking.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')

    def test_delete_booking(self):
        response = self.client.delete(f'/api/bookings/{self.booking.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Booking.objects.count(), 0)

from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from users.models import CustomUser
from cars.models import Car
from .models import Booking

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class BookingsAPITest(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user1', email='user1@example.com', password='test123')
        self.car = Car.objects.create(name='Model S', brand='Tesla', price=79999.99)
        self.booking = Booking.objects.create(user=self.user, car=self.car, status='confirmed')

    def test_get_bookings(self):
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking(self):
        data = {"user": self.user.id, "car": self.car.id, "status": "pending"}
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 2)

    def test_update_booking(self):
        data = {"status": "cancelled"}
        response = self.client.patch(f'/api/bookings/{self.booking.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')

    def test_delete_booking(self):
        response = self.client.delete(f'/api/bookings/{self.booking.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Booking.objects.count(), 0)
