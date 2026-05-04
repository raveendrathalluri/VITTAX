# # vittax/urls.py
# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),

#     path('', include('accounts.urls')),
#     path('', include('services.urls')),
#     path('', include('contact.urls')),
#     path('', include('admindashboard.urls')),
# ]

# # ✅ Serve MEDIA files
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # ✅ Serve STATIC files
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# # ✅ Error handlers
# handler404 = 'django.views.defaults.page_not_found'
# handler500 = 'django.views.defaults.server_error'


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main homepage
    path('', include('accounts.urls')),

    # Other apps
    path('services/', include('services.urls')),
    path('contact/', include('contact.urls')),
    path('dashboard/', include('admindashboard.urls')),
]