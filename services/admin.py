from django.contrib import admin
from .models import Service, ServiceApplication


# =========================
# SERVICE ADMIN
# =========================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'price',
        'is_active',
        'is_featured',
        'created_at'
    )

    list_filter = (
        'category',
        'is_active',
        'is_featured',
        'created_at'
    )

    search_fields = (
        'name',
        'slug',
        'description'
    )

    prepopulated_fields = {'slug': ('name',)}  # auto slug

    ordering = ('-created_at',)

    list_editable = ('is_active', 'is_featured', 'price')

    list_per_page = 20


# =========================
# SERVICE APPLICATION ADMIN
# =========================
@admin.register(ServiceApplication)
class ServiceApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'service',
        'status',
        'applied_at',
        'updated_at'
    )

    list_filter = (
        'status',
        'applied_at',
        'updated_at'
    )

    search_fields = (
        'user__username',
        'service__name',
        'notes'
    )

    ordering = ('-applied_at',)

    list_editable = ('status',)

    list_per_page = 20