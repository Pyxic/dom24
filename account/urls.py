from django.contrib.auth import logout
from django.urls import path

from account import views
from account.views import LoginView, LoginOwnerView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login_owner/', LoginOwnerView.as_view(), name='login_owner'),
    path('get_user_role', views.get_user_role, name='get_user_role'),
    path('logout/', views.logout_user, name='logout')
    ]
