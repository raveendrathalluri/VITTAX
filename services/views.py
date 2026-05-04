
# ════════════════════════════════════════════════════
# FILE 2:  services/views.py
# ════════════════════════════════════════════════════
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, ServiceApplication


def _nav():
    """Return active main-menu items (safe helper)."""
    try:
        from contact.models import NavMenuItem
        return NavMenuItem.objects.filter(
            menu_type='main', is_active=True, parent=None
        )
    except Exception:
        return []


# ── Public: list all services ─────────────────────────────
def services_view(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'services.html', {
        'services':  services,
        'nav_items': _nav(),
    })


# ── Public: single service detail ─────────────────────────
def service_detail(request, slug):
    service  = get_object_or_404(Service, slug=slug, is_active=True)
    related  = Service.objects.filter(
        is_active=True, category=service.category
    ).exclude(pk=service.pk)[:3]
    return render(request, 'service_detail.html', {
        'service':   service,
        'related':   related,
        'nav_items': _nav(),
    })


# ── Protected: apply for a service ────────────────────────
@login_required
def apply_service(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)

    # Check if already applied (pending / in progress)
    already = ServiceApplication.objects.filter(
        user=request.user,
        service=service,
        status__in=['pending', 'in_progress']
    ).exists()

    if already:
        messages.warning(
            request,
            f'You already have an active application for "{service.name}".'
        )
        return redirect('customer_dashboard')

    if request.method == 'POST':
        notes     = request.POST.get('notes', '').strip()
        documents = request.FILES.get('documents')

        app = ServiceApplication.objects.create(
            user      = request.user,
            service   = service,
            notes     = notes,
            documents = documents,
        )

        # Notify admin
        try:
            send_mail(
                f'[VITTAX] New Application — {service.name}',
                f'User     : {request.user.username}\n'
                f'Email    : {request.user.email}\n'
                f'Service  : {service.name}\n'
                f'Price    : ₹{service.price}\n'
                f'Notes    : {notes or "None"}\n',
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        # Confirm to customer
        try:
            send_mail(
                f'Application Received — {service.name} | VITTAX',
                f'Dear {request.user.first_name or request.user.username},\n\n'
                f'We have received your application for "{service.name}".\n'
                f'Our team will contact you within 24 hours.\n\n'
                f'Best Regards,\nVITTAX Team',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(
            request,
            f'✅ Applied for "{service.name}" successfully! '
            f'Our expert will contact you within 24 hours.'
        )
        return redirect('customer_dashboard')

    return render(request, 'apply_service.html', {
        'service':   service,
        'nav_items': _nav(),
    })