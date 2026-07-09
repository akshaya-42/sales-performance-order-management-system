from django.urls import path
from app import customer_views

urlpatterns = [
    path('', customer_views.customer_list, name='customer_list'),
    path('add/', customer_views.customer_create, name='customer_create'),
    path('<int:pk>/', customer_views.customer_detail, name='customer_detail'),
    path('<int:pk>/edit/', customer_views.customer_edit, name='customer_update'),
    path('<int:pk>/delete/', customer_views.customer_delete, name='customer_delete'),
]