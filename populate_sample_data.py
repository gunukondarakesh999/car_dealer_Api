import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_dealer_Api.settings')
django.setup()

from users.models import CustomUser
from cars.models import Car
from bookings.models import Booking
from payments.models import Payment

# --- USERS ---
if not CustomUser.objects.filter(email='user1@example.com').exists():
    user1 = CustomUser.objects.create_user(username='user1', email='user1@example.com', password='test123')
else:
    user1 = CustomUser.objects.get(email='user1@example.com')

if not CustomUser.objects.filter(email='user2@example.com').exists():
    user2 = CustomUser.objects.create_user(username='user2', email='user2@example.com', password='test123')
else:
    user2 = CustomUser.objects.get(email='user2@example.com')

# --- CARS ---
car1, _ = Car.objects.get_or_create(name='Model S', brand='Tesla', price=79999.99)
car2, _ = Car.objects.get_or_create(name='Model 3', brand='Tesla', price=49999.99)
car3, _ = Car.objects.get_or_create(name='Model X', brand='Tesla', price=89999.99)

# --- BOOKINGS ---
booking1, _ = Booking.objects.get_or_create(user=user1, car=car1, status='confirmed')
booking2, _ = Booking.objects.get_or_create(user=user2, car=car2, status='pending')

# --- PAYMENTS ---
payment1, _ = Payment.objects.get_or_create(user=user1, booking=booking1, amount=79999.99, status='paid')
payment2, _ = Payment.objects.get_or_create(user=user2, booking=booking2, amount=49999.99, status='pending')

print("Sample data inserted successfully!")
