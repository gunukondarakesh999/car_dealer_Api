from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser

class UsersAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create sample users
        self.user1 = CustomUser.objects.create_user(username='user1', email='user1@example.com', password='test123')
        self.user2 = CustomUser.objects.create_user(username='user2', email='user2@example.com', password='test123')

    def test_get_all_users(self):
        response = self.client.get('/api/users/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['email'], 'user1@example.com')
