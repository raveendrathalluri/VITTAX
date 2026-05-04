# contact/forms.py
from django import forms
from .models import NavMenuItem

class NavMenuForm(forms.ModelForm):
    """Form for creating/editing navigation menu items"""
    
    class Meta:
        model = NavMenuItem
        fields = ['label', 'url', 'icon', 'menu_type', 'parent', 'order', 'target', 'is_active']
        widgets = {
            'label': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Home, Services, About',
                'required': True
            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. / or /services/',
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. fas fa-home (optional)',
            }),
            'menu_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_menu_type',
                'required': True
            }),
            'parent': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_parent',
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'target': forms.Select(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Start with empty parent choices
        self.fields['parent'].queryset = NavMenuItem.objects.none()
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = "-- None (Top Level) --"
        
        # If editing existing item, show valid parents
        if self.instance.pk and self.instance.menu_type:
            self.fields['parent'].queryset = NavMenuItem.objects.filter(
                menu_type=self.instance.menu_type,
                parent__isnull=True
            ).exclude(pk=self.instance.pk)
        
        # If form is bound (POST request), filter by selected menu_type
        elif 'menu_type' in self.data:
            try:
                menu_type = self.data.get('menu_type')
                if menu_type:
                    self.fields['parent'].queryset = NavMenuItem.objects.filter(
                        menu_type=menu_type,
                        parent__isnull=True,
                        is_active=True
                    )
            except (ValueError, TypeError):
                pass
    
    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        menu_type = cleaned_data.get('menu_type')
        
        # Prevent selecting parent of different menu type
        if parent and parent.menu_type != menu_type:
            raise forms.ValidationError(
                "Parent menu item must be of the same menu type."
            )
        
        return cleaned_data