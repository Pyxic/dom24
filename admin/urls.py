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
    path('create_house', views.update_house, name='create_house'),
    path('update_house/<int:house_id>', views.update_house, name='update_house'),
    path('delete_house/<int:house_id>', views.delete_house, name='delete_house'),
    path('detail_house/<int:pk>/', views.HouseDetail.as_view(), name='detail_house'),
    path('flat_list', views.FlatList.as_view(), name='flat_list'),
    path('create_flat', views.update_flat, name='create_flat'),
    path('detail_flat/<int:pk>/', views.FlatDetail.as_view(), name='detail_flat'),
    path('delete_section/<int:pk>', views.delete_section, name='delete_section'),
    path('delete_level/<int:pk>', views.delete_level, name='delete_level'),
    path('delete_house_user/<int:pk>', views.delete_house_user, name='delete_house_user'),
    path('get_section_level', views.get_section_level, name='get_section_level'),
    path('update_flat/<int:flat_id>', views.update_flat, name='update_flat'),
    path('delete_flat/<int:pk>', views.delete_flat, name='delete_flat'),
    path('owner_list', views.OwnerList.as_view(), name='owner_list'),
    path('create_owner', views.update_owner, name='create_owner'),
    path('update_owner/<int:owner_id>', views.update_owner, name='update_owner'),
    path('detail_owner/<int:pk>', views.OwnerDetail.as_view(), name='detail_owner'),
    path('delete_owner/<int:user_id>', views.delete_owner, name='delete_owner'),
]
