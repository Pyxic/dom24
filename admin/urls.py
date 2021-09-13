from django.urls import path

from admin import views

urlpatterns = [
    path('', views.index, name='index'),
    path('singleton_page/<str:page_name>', views.singleton_page, name='main_page'),
    path('singleton_page/<str:page_name>', views.singleton_page, name='about_us_page'),
    path('singleton_page/<str:page_name>', views.singleton_page, name='service_page'),
    path('singleton_page/<str:page_name>', views.singleton_page, name='contact_page'),
    path('delete_image_gallery/<int:image_id>', views.delete_from_gallery, name='delete_image'),
    path('delete_document/<int:pk>', views.delete_document, name='delete_document'),
    path('edit_services', views.edit_services, name='edit_services'),
    path('delete_service', views.delete_service, name='delete_service'),
    path('delete_unit', views.delete_unit, name='delete_unit'),
    path('tariff_list', views.TariffList.as_view(), name='tariff_list'),
    path('create_tariff', views.update_tariff, name='create_tariff'),
    path('update_tariff/<int:tariff_id>', views.update_tariff, name='update_tariff'),
    path('delete_tariff/<int:tariff_id>', views.delete_tariff, name='delete_tariff'),
    path('get_unit_by_service', views.get_unit_by_service, name='get_unit_by_service'),
    path('roles/', views.settings_roles, name='roles'),
    path('user_list', views.UserList.as_view(), name='user_list'),
    path('update_user/<int:user_id>', views.update_user, name='update_user'),
    path('create_user', views.update_user, name='create_user'),
    path('user_delete/<int:user_id>', views.delete_user, name='delete_user'),
    path('requisites', views.settings_requisites, name='requisites'),
    path('payment_item', views.PaymentItemList.as_view(), name='payment_item_list'),
    path('create_payment_item', views.PaymentItemCreateView.as_view(), name='create_payment_item'),
    path('update_payment_item/<int:pk>', views.PaymentItemUpdateView.as_view(), name='update_payment_item'),
    path('delete_payment_item/<int:payment_item_id>', views.delete_payment_item, name='delete_payment_item'),
    path('house_list', views.HouseList.as_view(), name='house_list'),
]
