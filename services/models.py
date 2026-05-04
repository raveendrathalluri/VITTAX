# services/models.py
from django.db import models
from accounts.models import CustomUser

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('tax', 'Tax Filing'),
        ('gst', 'GST Services'),
        ('accounting', 'Accounting'),
        ('investment', 'Investment'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    icon = models.CharField(max_length=100, default='fas fa-file-alt')  # FontAwesome icon
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ServiceApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    documents = models.FileField(upload_to='documents/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service.name} - {self.service.name}"