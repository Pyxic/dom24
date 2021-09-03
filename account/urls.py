from django.contrib.auth import logout
from django.urls import path

from account import views
from account.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    ]