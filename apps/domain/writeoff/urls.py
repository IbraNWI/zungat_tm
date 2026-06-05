from django.urls import path
from . import views

urlpatterns = [
    path('accept/', views.create_writeoff, name='create_writeoff'),
    ]