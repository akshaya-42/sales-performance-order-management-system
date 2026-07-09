from django.urls import path
from app import auth_views

urlpatterns = [
    path('login/', auth_views.login_views, name='login'),
    path('register/', auth_views.register_views, name='register'),
    path('logout/', auth_views.logout_views, name='logout'),
]