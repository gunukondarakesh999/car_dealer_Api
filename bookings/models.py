from django.db import models

# Create your models here.
from django.db import models
from users.models import CustomUser
from cars.models import Car

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Booking {self.id}: {self.user.email} -> {self.car.name}"
