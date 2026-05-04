
# ════════════════════════════════════════════════════
# FILE 1:  services/urls.py
# ════════════════════════════════════════════════════
from django.urls import path
from . import views

urlpatterns = [
    path('services/',                     views.services_view,  name='services'),
    path('services/<slug:slug>/',         views.service_detail, name='service_detail'),
    path('services/<slug:slug>/apply/',   views.apply_service,  name='apply_service'),
]

