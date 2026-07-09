# from django.urls import path
# from app import dashboard_views

# urlpatterns = [
#     path('dashboard/', dashboard_views.dashboard, name='dashboard'),
# ]

from django.urls import path
from app import dashboard_views

urlpatterns = [
    path('dashboard/', dashboard_views.dashboard_views, name='dashboard'),
    path('notifications/', dashboard_views.notifications_views, name='notifications'),
    path('notifications/<int:pk>/read/', dashboard_views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', dashboard_views.mark_all_read, name='mark_all_read'),
    path('search/', dashboard_views.dashboard_search, name='dashboard_search'),
]