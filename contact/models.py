# contact/models.py
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    
# contact/models.py
from django.db import models
from django.utils import timezone

class NavMenuItem(models.Model):
    """Navigation menu items for website"""
    
    MENU_TYPE_CHOICES = [
        ('main', 'Main Menu'),
        ('footer', 'Footer Links'),
        ('utility', 'Utility Links'),
    ]
    
    label = models.CharField(
        max_length=100,
        help_text="Display text for the menu item"
    )
    url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="URL or route name (e.g., /services/ or home)"
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="FontAwesome icon class (e.g., fas fa-home)"
    )
    menu_type = models.CharField(
        max_length=20,
        choices=MENU_TYPE_CHOICES,
        default='main'
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        help_text="Parent menu item for submenu"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (ascending)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show on website"
    )
    target = models.CharField(
        max_length=20,
        choices=[('_self', 'Same Window'), ('_blank', 'New Window')],
        default='_self'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['menu_type', 'order', 'label']
        verbose_name = "Navigation Menu Item"
        verbose_name_plural = "Navigation Menu Items"
    
    def __str__(self):
        return f"{self.label} ({self.get_menu_type_display()})"
    
    def get_menu_type_display(self):
        return dict(self.MENU_TYPE_CHOICES).get(self.menu_type, self.menu_type)
    
    def get_absolute_url(self):
        """Get the URL for this menu item"""
        if self.url.startswith('/') or self.url.startswith('http'):
            return self.url
        else:
            # Treat as Django URL name
            from django.urls import reverse
            try:
                return reverse(self.url)
            except:
                return '#'
    
    def has_children(self):
        """Check if menu item has submenus"""
        return self.children.filter(is_active=True).exists()
    
    def get_active_children(self):
        """Get active child items"""
        return self.children.filter(is_active=True).order_by('order')
    
    @classmethod
    def get_menu_by_type(cls, menu_type='main'):
        """Get all active items of specific type"""
        return cls.objects.filter(
            menu_type=menu_type,
            is_active=True,
            parent__isnull=True
        ).prefetch_related('children').order_by('order')
