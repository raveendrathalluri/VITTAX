#dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from accounts.models import CustomUser
from services.models import Service, ServiceApplication
from contact.models import ContactMessage, NavMenuItem
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import json

from django.views.decorators.http import require_http_methods
from django.db.models import Q
from contact.models import NavMenuItem
from contact.form import NavMenuForm

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin_user():
            messages.error(request, 'Access denied. Admin only.')
            return redirect('customer_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def dashboard_redirect(request):
    if request.user.is_admin_user():
        return redirect('admin_dashboard')
    return redirect('customer_dashboard')

# ── CUSTOMER DASHBOARD ──
@login_required
def customer_dashboard(request):
    apps = ServiceApplication.objects.filter(user=request.user).order_by('-applied_at')
    services = Service.objects.filter(is_active=True)[:6]
    return render(request, 'customer_dashboard/index.html', {
        'applications': apps,
        'services': services,
        'total_apps': apps.count(),
        'pending': apps.filter(status='pending').count(),
        'completed': apps.filter(status='completed').count(),
    })

# ── ADMIN DASHBOARD ──
@admin_required
def admin_dashboard(request):
    users = CustomUser.objects.filter(role='customer').count()
    contacts = ContactMessage.objects.filter(is_read=False).count()
    services = Service.objects.count()
    applications = ServiceApplication.objects.count()
    recent_contacts = ContactMessage.objects.order_by('-created_at')[:5]
    recent_users = CustomUser.objects.filter(role='customer').order_by('-date_joined')[:5]
    recent_apps = ServiceApplication.objects.order_by('-applied_at')[:5]
    return render(request, 'admin_dashboard/index.html', {
        'total_users': users,
        'unread_contacts': contacts,
        'total_services': services,
        'total_applications': applications,
        'recent_contacts': recent_contacts,
        'recent_users': recent_users,
        'recent_apps': recent_apps,
    })

@admin_required
def admin_users(request):
    users = CustomUser.objects.filter(role='customer').order_by('-date_joined')
    return render(request, 'admin_dashboard/users.html', {'users': users})

@admin_required
def admin_user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.city = request.POST.get('city', user.city)
        user.pan_number = request.POST.get('pan_number', user.pan_number)
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
        messages.success(request, f'User {user.username} updated successfully!')
        return redirect('admin_users')
    return render(request, 'admin_dashboard/user_edit.html', {'edit_user': user})

@admin_required
def admin_user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully.')
        return redirect('admin_users')
    return render(request, 'admin_dashboard/confirm_delete.html', {'obj': user, 'type': 'User'})

@admin_required
def admin_contacts(request):
    contacts = ContactMessage.objects.order_by('-created_at')
    ContactMessage.objects.filter(is_read=False).update(is_read=True)
    return render(request, 'admin_dashboard/contacts.html', {'contacts': contacts})

@admin_required
def admin_contact_delete(request, pk):
    contact = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact message deleted.')
        return redirect('admin_contacts')
    return render(request, 'admin_dashboard/confirm_delete.html', {'obj': contact, 'type': 'Contact'})

@admin_required
def admin_services(request):
    services = Service.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard/services.html', {'services': services})

@admin_required
def admin_service_add(request):
    from django.utils.text import slugify
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = slugify(name)
        # ensure unique slug
        base, counter = slug, 1
        while Service.objects.filter(slug=slug).exists():
            slug = f"{base}-{counter}"; counter += 1
        Service.objects.create(
            name=name, slug=slug,
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            short_description=request.POST.get('short_description'),
            price=request.POST.get('price', 0),
            icon=request.POST.get('icon', 'fas fa-file-alt'),
            is_featured=request.POST.get('is_featured') == 'on',
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, f'Service "{name}" added successfully!')
        return redirect('admin_services')
    return render(request, 'admin_dashboard/service_form.html', {'action': 'Add'})

@admin_required
def admin_service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.name = request.POST.get('name', service.name)
        service.category = request.POST.get('category', service.category)
        service.description = request.POST.get('description', service.description)
        service.short_description = request.POST.get('short_description', service.short_description)
        service.price = request.POST.get('price', service.price)
        service.icon = request.POST.get('icon', service.icon)
        service.is_featured = request.POST.get('is_featured') == 'on'
        service.is_active = request.POST.get('is_active') == 'on'
        service.save()
        messages.success(request, f'Service "{service.name}" updated!')
        return redirect('admin_services')
    return render(request, 'admin_dashboard/service_form.html', {'action': 'Edit', 'service': service})

@admin_required
def admin_service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted.')
        return redirect('admin_services')
    return render(request, 'admin_dashboard/confirm_delete.html', {'obj': service, 'type': 'Service'})

@admin_required
def admin_applications(request):
    apps = ServiceApplication.objects.all().order_by('-applied_at')
    return render(request, 'admin_dashboard/applications.html', {'applications': apps})

@admin_required
def admin_app_status(request, pk):
    app = get_object_or_404(ServiceApplication, pk=pk)
    if request.method == 'POST':
        app.status = request.POST.get('status', app.status)
        app.save()
        messages.success(request, 'Application status updated.')
        return redirect('admin_applications')
    return render(request, 'admin_dashboard/app_status.html', {'application': app})





# ────── Helper Functions ──────────────────────────────────
def is_admin(user):
    """Check if user is admin"""
    return user.is_staff or user.role == 'admin'


# ────── Navigation Menu Views ──────────────────────────────

@login_required
@user_passes_test(is_admin)
def admin_nav_menu(request):
    """List all navigation menu items"""
    menu_type = request.GET.get('type', 'main')
    
    menu_items = NavMenuItem.objects.filter(menu_type=menu_type).order_by('order')
    
    context = {
        'menu_items': menu_items,
        'menu_type': menu_type,
        'is_main': menu_type == 'main',
        'is_footer': menu_type == 'footer',
        'is_utility': menu_type == 'utility',
    }
    
    return render(request, 'admin_dashboard/nav_menu.html', context)


@login_required
@user_passes_test(is_admin)
def admin_nav_add(request):
    """Add new navigation menu item"""
    if request.method == 'POST':
        form = NavMenuForm(request.POST)
        if form.is_valid():
            nav_item = form.save()
            messages.success(
                request,
                f'Menu item "{nav_item.label}" added successfully!'
            )
            return redirect('admin_nav_menu')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = NavMenuForm()
    
    context = {
        'form': form,
        'action': 'Add',
        'is_add': True,
        'is_edit': False,
    }
    
    return render(request, 'admin_dashboard/nav_menu_form.html', context)


@login_required
@user_passes_test(is_admin)
def admin_nav_edit(request, pk):
    """Edit navigation menu item"""
    nav_item = get_object_or_404(NavMenuItem, pk=pk)
    
    if request.method == 'POST':
        form = NavMenuForm(request.POST, instance=nav_item)
        if form.is_valid():
            nav_item = form.save()
            messages.success(
                request,
                f'Menu item "{nav_item.label}" updated successfully!'
            )
            return redirect('admin_nav_menu')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = NavMenuForm(instance=nav_item)
    
    context = {
        'form': form,
        'action': 'Edit',
        'is_add': False,
        'is_edit': True,
        'nav_item': nav_item,
    }
    
    return render(request, 'admin_dashboard/nav_menu_form.html', context)


@login_required
@user_passes_test(is_admin)
def admin_nav_delete(request, pk):
    """Delete navigation menu item"""
    nav_item = get_object_or_404(NavMenuItem, pk=pk)
    
    if request.method == 'POST':
        label = nav_item.label
        nav_item.delete()
        messages.success(request, f'Menu item "{label}" deleted successfully!')
        return redirect('admin_nav_menu')
    
    context = {
        'obj': nav_item,
        'type': 'Menu Item',
    }
    
    return render(request, 'admin_dashboard/confirm_delete.html', context)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def admin_nav_reorder(request):
    """AJAX endpoint to reorder menu items"""
    try:
        items = request.POST.getlist('item_ids[]')
        
        for index, item_id in enumerate(items):
            try:
                nav_item = NavMenuItem.objects.get(pk=int(item_id))
                nav_item.order = index
                nav_item.save()
            except (ValueError, NavMenuItem.DoesNotExist):
                continue
        
        return JsonResponse({'success': True, 'message': 'Items reordered successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def admin_nav_toggle(request, pk):
    """AJAX endpoint to toggle menu item active status"""
    try:
        nav_item = get_object_or_404(NavMenuItem, pk=pk)
        nav_item.is_active = not nav_item.is_active
        nav_item.save()
        
        return JsonResponse({
            'success': True,
            'is_active': nav_item.is_active,
            'message': 'Status updated successfully'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@user_passes_test(is_admin)
@require_http_methods(["GET"])
def admin_nav_get_parents(request):
    """AJAX endpoint to get parent menu items for selected menu type"""
    try:
        menu_type = request.GET.get('type', '')
        
        if not menu_type:
            return JsonResponse({'parents': []})
        
        parents = NavMenuItem.objects.filter(
            menu_type=menu_type,
            parent__isnull=True
        ).values('id', 'label').order_by('order')
        
        return JsonResponse({'parents': list(parents)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)