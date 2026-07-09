# from django.urls import path
# from app import profile_views

# urlpatterns = [
#     path('', profile_views.profile, name='profile'),
#     path('edit/', profile_views.profile_edit, name='profile_edit'),
#     path('change-password/', profile_views.change_password, name='change_password'),
# ]

from django.urls import path
from app import profile_views

urlpatterns = [
    path('', profile_views.profile_views, name='profile'),
    path('edit/', profile_views.profile_edit, name='profile_edit'),
    path('users/', profile_views.user_list, name='user_list'),
    path('users/<int:pk>/role/', profile_views.change_user_role, name='change_user_role'),
    
]