from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_writeoff, name='create_writeoff'),
    ]