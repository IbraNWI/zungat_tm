from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.echo, name='create_writeoff'),
    ]