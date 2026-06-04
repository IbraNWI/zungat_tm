from django.urls import path
from . import views

urlpatterns = [
    path('cencel/', views.cencel_payment, name='cencel_payment'),
    ]