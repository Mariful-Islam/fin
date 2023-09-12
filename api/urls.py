from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRouter, name='get_router'),
    path('transfer/', views.transfer),
]
