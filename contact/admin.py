# contact/admin.py
from django.contrib import admin
from .models import ContactMessage, NavMenuItem


# ════════ Navigation Menu Admin ════════

class NavMenuChildInline(admin.TabularInline):
    """Inline editing for child menu items"""
    model = NavMenuItem
    extra = 0
    fields = ('label', 'url', 'icon', 'order', 'is_active')
    fk_name = 'parent'


@admin.register(NavMenuItem)
class NavMenuItemAdmin(admin.ModelAdmin):
    """Navigation Menu Item Admin"""
    list_display = ('label', 'menu_type', 'parent', 'order', 'is_active')
    list_filter = ('menu_type', 'is_active', 'created_at')
    search_fields = ('label', 'url')
    ordering = ('menu_type', 'order')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('label', 'menu_type', 'url', 'icon')
        }),
        ('Display', {
            'fields': ('order', 'parent', 'target', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    inlines = [NavMenuChildInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('parent')


# ════════ Contact Message Admin ════════

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Contact Message Admin"""
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'phone', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent adding messages from admin - only from contact form"""
        return False