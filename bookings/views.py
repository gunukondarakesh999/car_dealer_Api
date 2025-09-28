from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer

from django.core.cache import cache

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get_queryset(self):
        bookings = cache.get('all_bookings')
        if not bookings:
            bookings = Booking.objects.all()
            cache.set('all_bookings', bookings, timeout=60*5)
        return bookings
