from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Car
from .serializers import CarSerializer
from django.core.cache import cache


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer

    def get_queryset(self):
        cars = cache.get('all_cars')
        if not cars:
            cars = Car.objects.all()
            cache.set('all_cars', cars, timeout=60*5)  # 5 min cache
        return cars

    def perform_create(self, serializer):
        serializer.save()
        cache.delete('all_cars')  # clear cache

    def perform_update(self, serializer):
        serializer.save()
        cache.delete('all_cars')

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete('all_cars')
