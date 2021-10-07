from django.contrib.auth import logout
from django.urls import path

from cabinet import views


urlpatterns = [
    path('index', views.index, name='index'),
    path('summary/<int:flat_id>', views.summary, name='summary'),
    path('receipt_list', views.ReceiptList.as_view(), name='receipt_list'),
    path('detail_receipt/<str:pk>', views.ReceiptDetail.as_view(), name='detail_receipt'),
    path('detail_flatservice/<int:pk>', views.FlatServiceDetail.as_view(), name='detail_flatservice'),
    path('message_list/', views.MessageList.as_view(), name='message_list'),
    path('detail_message/<int:pk>', views.MessageDetail.as_view(), name='detail_message'),
    path('master_request_list', views.MasterRequestList.as_view(), name='master_request_list'),
    path('create_master_request', views.MasterRequestCreate.as_view(), name='create_master_request'),
    path('delete_master_request/<int:pk>', views.delete_master_request, name='delete_master_request'),
    path('owner_profile', views.OwnerProfile.as_view(), name='owner_profile'),
    path('receipt_pdf/<str:receipt_id>', views.render_pdf_view, name='receipt_pdf'),
    ]
