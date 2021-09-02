from django.urls import path

from admin import views

urlpatterns = [
    path('', views.index, name='index'),
    path('singleton_page/<str:page_name>', views.singleton_page, name='main_page'),
    path('singleton_page/<str:page_name>', views.singleton_page, name='about_us_page'),
    path('singleton_page/<str:page_name>', views.singleton_page, name='service_page'),
    path('singleton_page/<str:page_name>', views.singleton_page, name='contact_page'),
]