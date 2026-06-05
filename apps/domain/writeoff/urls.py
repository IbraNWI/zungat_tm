from django.urls import path
from . import views

urlpatterns = [
    path('accept/', views.accept_writeoff, name='create_writeoff'),
    ]