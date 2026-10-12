
# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    # Customer
    path('dashboard/home/', views.customer_dashboard, name='customer_dashboard'),
    # Admin
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:pk>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin-panel/users/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin-panel/contacts/', views.admin_contacts, name='admin_contacts'),
    path('admin-panel/contacts/<int:pk>/delete/', views.admin_contact_delete, name='admin_contact_delete'),
    path('admin-panel/services/', views.admin_services, name='admin_services'),
    path('admin-panel/services/add/', views.admin_service_add, name='admin_service_add'),
    path('admin-panel/services/<int:pk>/edit/', views.admin_service_edit, name='admin_service_edit'),
    path('admin-panel/services/<int:pk>/delete/', views.admin_service_delete, name='admin_service_delete'),
    path('admin-panel/applications/', views.admin_applications, name='admin_applications'),
    path('admin-panel/applications/<int:pk>/status/', views.admin_app_status, name='admin_app_status'),
    
        # Navigation Menu Management
   # Admin Panel - Navigation Menu (ADD THESE LINES)
    path('admin-panel/nav-menu/', views.admin_nav_menu, name='admin_nav_menu'),
    path('admin-panel/nav-menu/add/', views.admin_nav_add, name='admin_nav_add'),
    path('admin-panel/nav-menu/<int:pk>/edit/', views.admin_nav_edit, name='admin_nav_edit'),
    path('admin-panel/nav-menu/<int:pk>/delete/', views.admin_nav_delete, name='admin_nav_delete'),
    path('admin-panel/nav-menu/reorder/', views.admin_nav_reorder, name='admin_nav_reorder'),
    path('admin-panel/nav-menu/<int:pk>/toggle/', views.admin_nav_toggle, name='admin_nav_toggle'),
    path('admin-panel/nav-menu/get-parents/', views.admin_nav_get_parents, name='admin_nav_get_parents'),
]