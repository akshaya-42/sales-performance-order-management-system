from django.urls import path
from app import order_views

urlpatterns = [
    path('', order_views.order_list, name='order_list'),
    path('add/', order_views.order_create, name='order_create'),
    path('<int:pk>/', order_views.order_detail, name='order_detail'),
    path('<int:pk>/edit/', order_views.order_edit, name='order_edit'),
    path('<int:pk>/delete/', order_views.order_delete, name='order_delete'),
    path('<int:pk>/status/', order_views.update_order_status, name='update_order_status'),
]