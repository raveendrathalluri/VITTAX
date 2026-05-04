
from contact.models import NavMenuItem

def navigation_menu(request):
    """Make navigation available in all templates"""
    try:
        nav_main = NavMenuItem.objects.filter(
            menu_type='main',
            is_active=True,
            parent__isnull=True
        ).prefetch_related('children').order_by('order')
        
        nav_footer = NavMenuItem.objects.filter(
            menu_type='footer',
            is_active=True,
            parent__isnull=True
        ).prefetch_related('children').order_by('order')
        
        nav_utility = NavMenuItem.objects.filter(
            menu_type='utility',
            is_active=True,
            parent__isnull=True
        ).order_by('order')
    except Exception:
        nav_main = nav_footer = nav_utility = []
    
    return {
        'nav_main': nav_main,
        'nav_footer': nav_footer,
        'nav_utility': nav_utility,
    }