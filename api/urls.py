from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRouter),
    path('transfer/', views.transfer),
]
