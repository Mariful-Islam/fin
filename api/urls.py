from django.urls import path
from . import views
from .views import MyTokenObtainPairView, RegisterApi

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRouter),
    path('register/', RegisterApi.as_view()),
    path('login/', views.log_in),
    path('transfer/', views.transfer),
    path('transactions/<str:username>/', views.transactions),
    path('ledger/', views.ledger),
    path('balance/<str:username>/', views.balance),

    path('friends/', views.friends),
    path('bank_account/', views.create_bank_account),
    path('bank_account/<str:username>/', views.get_bank_account),
    path('create-profile/', views.create_profile),
    path('profile/<str:username>/', views.get_profile),


    path('token/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),

    path('revenue/', views.revenue),
]
