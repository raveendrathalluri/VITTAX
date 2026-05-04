from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = (
        'username',
        'email',
        'role',
        'phone',
        'is_staff',
        'is_active',
        'created_at'
    )

    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'role',
                'phone',
                'city',
                'pan_number',
                'gst_number',
                'profile_pic'
            )
        }),
    )
