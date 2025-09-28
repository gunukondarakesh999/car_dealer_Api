from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser
from bookings.models import Booking
from cars.models import Car
from .models import Payment

class PaymentsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user2', email='user2@example.com', password='test123')
        self.car = Car.objects.create(name='Model X', brand='Tesla', price=89999.99)
        self.booking = Booking.objects.create(user=self.user, car=self.car, status='confirmed')
        self.payment = Payment.objects.create(user=self.user, booking=self.booking, amount=89999.99, status='paid')

    def test_get_all_payments(self):
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]['amount']), 89999.99)

from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from users.models import CustomUser
from cars.models import Car
from bookings.models import Booking
from .models import Payment

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class PaymentsAPITest(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='user2', email='user2@example.com', password='test123')
        self.car = Car.objects.create(name='Model X', brand='Tesla', price=89999.99)
        self.booking = Booking.objects.create(user=self.user, car=self.car, status='confirmed')
        self.payment = Payment.objects.create(user=self.user, booking=self.booking, amount=89999.99, status='paid')

    def test_get_payments(self):
        response = self.client.get('/api/payments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_payment(self):
        data = {"user": self.user.id, "booking": self.booking.id, "amount": 89999.99, "status": "pending"}
        response = self.client.post('/api/payments/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payment.objects.count(), 2)

    def test_update_payment(self):
        data = {"status": "refunded"}
        response = self.client.patch(f'/api/payments/{self.payment.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'refunded')

    def test_delete_payment(self):
        response = self.client.delete(f'/api/payments/{self.payment.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Payment.objects.count(), 0)
