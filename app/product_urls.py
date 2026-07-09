# from django.urls import path
# from app import product_views

# urlpatterns = [
#     path('', product_views.product_list, name='product_list'),
#     path('add/', product_views.product_create, name='product_create'),
#     path('<int:pk>/edit/', product_views.product_edit, name='product_edit'),
#     path('<int:pk>/delete/', product_views.product_delete, name='product_delete'),
#     path('categories/create/',product_views.category_create,name='category_create'),

#     path('categories/', product_views.category_list, name='category_list'),
#     path('categories/create/', product_views.category_create, name='category_create'),
#     path('categories/<int:pk>/edit/', product_views.category_edit, name='category_edit'),
#     path('categories/<int:pk>/delete/', product_views.category_delete, name='category_delete'),

# ]

from django.urls import path
from app import product_views

urlpatterns = [
    path('', product_views.product_list, name='product_list'),
    path('add/', product_views.product_create, name='product_create'),
    path('<int:pk>/', product_views.product_detail, name='product_detail'),
    path('<int:pk>/edit/', product_views.product_edit, name='product_edit'),
    path('<int:pk>/delete/', product_views.product_delete, name='product_delete'),
    path('categories/create/',product_views.category_create,name='category_create'),

    path('categories/', product_views.category_list, name='category_list'),
    path('categories/create/', product_views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', product_views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', product_views.category_delete, name='category_delete'),

]