from django.urls import path
from .auth_views import login_views, logout_views, register_views, change_password_views
from .import product_views
from .import dashboard_views

app_name = 'app'

urlpatterns = [

    path('login/',login_views, name='login'),
    path('logout/', logout_views, name='logout'),
    path('register/', register_views, name='register'),
    path('categories/',product_views.category_list,name='category_list'),
    path('dashboard/',dashboard_views.dashboard_views,name='dashboard'),
    path('change_password/', change_password_views, name='change_password'),
    path('categories/', product_views.category_list,name='category_list'),
    path('products/',product_views.product_list,name='product_list'),
    


]