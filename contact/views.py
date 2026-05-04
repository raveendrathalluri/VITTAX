# contact/views.py
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import ContactMessage, NavMenuItem

def contact_view(request):
    nav_items = NavMenuItem.objects.filter(menu_type='main', is_active=True, parent=None)
    if request.method == 'POST':
        name = request.POST.get('name','').strip()
        email = request.POST.get('email','').strip()
        phone = request.POST.get('phone','').strip()
        subject = request.POST.get('subject','').strip()
        message = request.POST.get('message','').strip()
        if name and email and subject and message:
            # Save to DB
            contact = ContactMessage.objects.create(name=name, email=email, phone=phone, subject=subject, message=message)
            # Email to Admin
            try:
                send_mail(
                    f'[VITTAX Contact] {subject}',
                    f'Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}',
                    settings.EMAIL_HOST_USER,
                    [settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except: pass
            # Email to Customer
            try:
                send_mail(
                    'Thank you for contacting VITTAX!',
                    f'Dear {name},\n\nThank you for reaching out to us. We have received your message and our team will get back to you within 24 hours.\n\nYour Query: {subject}\n\nBest Regards,\nVITTAX Team\n📞 +91-XXXXXXXXXX\n🌐 vittax.com',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=True,
                )
            except: pass
            messages.success(request, 'Your message has been sent successfully! We\'ll contact you within 24 hours.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill all required fields.')
    return render(request, 'contact.html', {'nav_items': nav_items})

