from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/',include('app.urls')),
    path('', lambda request: redirect('dashboard') if request.user.is_authenticated else redirect('login'), name='home'),
    path('auth/', include('app.auth_urls')),
    path('dashboard/', include('app.dashboard_urls')),
    path('products/', include('app.product_urls')),
    path('customers/', include('app.customer_urls')),
    path('orders/', include('app.order_urls')),
    path('reports/', include('app.report_urls')),
    path('profile/', include('app.profile_urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.contrib import adminS
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.shortcuts import redirect

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', lambda request: redirect('dashboard') if request.user.is_authenticated else redirect('login'), name='home'),
#     path('auth/', include('app.urls')),
#     path('dashboard/', include('app.urls')),
#     path('products/', include('app.urls')),
#     path('customers/', include('app.urls')),
#     path('orders/', include('app.urls')),
#     path('reports/', include('app.urls')),
#     path('profile/', include('app.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.shortcuts import redirect

# urlpatterns = [
#     path('admin/', admin.site.urls),

#     path(
#         '',
#         lambda request: redirect('dashboard')
#         if request.user.is_authenticated
#         else redirect('login'),
#         name='home'
#     ),

#     path('auth/', include('app.urls')),
    
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)

# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.shortcuts import redirect

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', lambda request: redirect('dashboard') if request.user.is_authenticated else redirect('login'), name='home'),
#     path('auth/', include('app.urls.auth_urls')),
#     path('dashboard/', include('app.urls.dashboard_urls')),
#     path('products/', include('app.urls.product_urls')),
#     path('customers/', include('app.urls.customer_urls')),
#     path('orders/', include('app.urls.order_urls')),
#     path('reports/', include('app.urls.report_urls')),
#     path('profile/', include('app.urls.profile_urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)