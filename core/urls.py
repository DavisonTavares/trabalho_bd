from django.contrib import admin
from django.urls import path
from .views import home, add_client


urlpatterns = [
    path('', home),
    path('add_client', add_client, name='add_client'),
]

