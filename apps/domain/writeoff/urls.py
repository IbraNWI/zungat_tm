from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.writeoff_func, name='create_writeoff'),
    ]