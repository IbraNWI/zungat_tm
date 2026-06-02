from django.urls import path
from . import views

urlpatterns = [
    path('connect/', views.bitrix_connect, name='bitrix_connect'),
    path('callback/', views.bitrix_callback, name='bitrix_callback'),
    path('get_tm_driver_info')
]