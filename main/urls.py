from django.urls import path

from main import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('about_us', views.about_us, name='about_us_page'),
    path('services', views.services, name='service_page'),
    path('contacts', views.contacts, name='contact_page')
]
