from django.urls import path
from .views import UserListView

urlpatterns = [
    path('all/', UserListView.as_view(), name='user-list'),
]
