# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm, ProfileUpdateForm
from contact.models import NavMenuItem


# ── helper ─────────────────────────────────────────────────
def _nav():
    try:
        from contact.models import NavMenuItem
        return NavMenuItem.objects.filter(
            menu_type='main', is_active=True, parent=None
        )
    except Exception:
        return []


# ── Public pages ───────────────────────────────────────────
def home(request):
    """Home page with navigation"""
    try:
        from services.models import Service
        services = Service.objects.filter(is_active=True, is_featured=True)[:6]
    except Exception:
        services = []
    
    return render(request, 'home.html', {
        'services': services,
        'nav_main': _get_nav_menu('main'),
        'nav_footer': _get_nav_menu('footer'),
    })
    

def _get_nav_menu(menu_type='main'):
    """Helper function to get navigation menu"""
    try:
        return NavMenuItem.objects.filter(
            menu_type=menu_type,
            is_active=True,
            parent__isnull=True  # Only top-level items
        ).prefetch_related('children').order_by('order')
    except Exception:
        return []


def about_view(request):
    """About page"""
    return render(request, 'about.html', {
        'nav_main': _get_nav_menu('main'),
        'nav_footer': _get_nav_menu('footer'),
    })


def pricing_view(request):
    """Pricing page"""
    try:
        from services.models import Service
        services = Service.objects.filter(is_active=True)
    except Exception:
        services = []
    
    return render(request, 'pricing.html', {
        'services': services,
        'nav_main': _get_nav_menu('main'),
        'nav_footer': _get_nav_menu('footer'),
    })


# ── Auth ───────────────────────────────────────────────────
def register_view(request):
    """Register page"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                send_mail(
                    'Welcome to VITTAX!',
                    f'Dear {user.first_name or user.username},\n\nWelcome to VITTAX!\n\nYour account has been created successfully.\n\nBest Regards,\nVITTAX Team',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            login(request, user)
            messages.success(request, f'Welcome {user.first_name or user.username}! Account created successfully.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form,
        'nav_main': _get_nav_menu('main'),
        'nav_footer': _get_nav_menu('footer'),
    })

def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {
        'nav_main': _get_nav_menu('main'),
        'nav_footer': _get_nav_menu('footer'),
    })


@login_required
def logout_view(request):
    """Logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile_view(request):
    """User profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'customer_dashboard/profile.html', {
        'form': form,
        'nav_main': _get_nav_menu('main'),
        'nav_footer': _get_nav_menu('footer'),
    })



# HEAD 1
def proprietorship(request): return render(request,'start_business/proprietorship.html')
def partnership_firm(request): return render(request,'start_business/partnership_firm.html')
def llp(request): return render(request,'start_business/llp.html')
def opc(request): return render(request,'start_business/opc.html')
def private_limited_company(request): return render(request,'start_business/private_limited_company.html')
def section8_company(request): return render(request,'start_business/section8_company.html')
def producer_company(request): return render(request,'start_business/producer_company.html')
def nidhi_company(request): return render(request,'start_business/nidhi_company.html')
def trust_registration(request): return render(request,'start_business/trust_registration.html')

# HEAD 2
# accounts/views.py
from django.shortcuts import render

# HEAD 2 : Registrations & Licences
def gst_registration(request): return render(request, 'registrations/gst_registration.html')
def msme_registration(request): return render(request, 'registrations/msme_registration.html')
def shop_establishment(request): return render(request, 'registrations/shop_establishment.html')
def trade_license(request): return render(request, 'registrations/trade_license.html')
def local_labour_licences(request): return render(request, 'registrations/local_labour_licences.html')
def professional_tax(request): return render(request, 'registrations/professional_tax.html')
def pf_registration(request): return render(request, 'registrations/pf_registration.html')
def esi_registration(request): return render(request, 'registrations/esi_registration.html')
def fssai(request): return render(request, 'registrations/fssai.html')
def import_export_code(request): return render(request, 'registrations/import_export_code.html')
def bis_registration(request): return render(request, 'registrations/bis_registration.html')
def barcode_registration(request): return render(request, 'registrations/barcode_registration.html')
def drug_license(request): return render(request, 'registrations/drug_license.html')
def startup_registration(request): return render(request, 'registrations/startup_registration.html')
def dpiit_recognition(request): return render(request, 'registrations/dpiit_recognition.html')
def darpan_registration(request): return render(request, 'registrations/darpan_registration.html')
def a12_registration(request): return render(request, 'registrations/12a_registration.html')
def g80_registration(request): return render(request, 'registrations/80g_registration.html')
def dsc(request): return render(request, 'registrations/dsc.html')
def iso_advisory(request): return render(request, 'registrations/iso_advisory.html')

# ===== HEAD 3 =====
def gst_service_1(request): return render(request,'gst/gst_registration.html')
def gst_service_2(request): return render(request,'gst/gst_returns.html')
def gst_service_3(request): return render(request,'gst/gst_returns_correction.html')
def gst_service_4(request): return render(request,'gst/gst_invoicing_setup.html')
def gst_service_5(request): return render(request,'gst/e_way_bill.html')
def gst_service_6(request): return render(request,'gst/itc_advisory.html')
def gst_service_7(request): return render(request,'gst/gstr9_audit.html')
def gst_service_8(request): return render(request,'gst/gst_refund.html')
def gst_service_9(request): return render(request,'gst/gst_notices.html')
def gst_service_10(request): return render(request,'gst/gst_health_check.html')
def gst_service_11(request): return render(request,'gst/export_sez.html')
def gst_service_12(request): return render(request,'gst/ecommerce_gst.html')
def gst_service_13(request): return render(request,'gst/gst_training.html')

# ===== HEAD 4 =====
def income_tax_1(request): return render(request,'income_tax/itr_filing.html')
def income_tax_2(request): return render(request,'income_tax/tax_planning.html')
def income_tax_3(request): return render(request,'income_tax/tds_tcs.html')
def income_tax_4(request): return render(request,'income_tax/capital_gains.html')
def income_tax_5(request): return render(request,'income_tax/advance_tax.html')
def income_tax_6(request): return render(request,'income_tax/tax_notices.html')
def income_tax_7(request): return render(request,'income_tax/appeals.html')
def income_tax_8(request): return render(request,'income_tax/form15ca_15cb.html')
def income_tax_9(request): return render(request,'income_tax/pan_tan.html')

# ===== HEAD 5 =====
def mca_1(request): return render(request,'mca/company_annual_filings.html')
def mca_2(request): return render(request,'mca/llp_annual_filings.html')
def mca_3(request): return render(request,'mca/director_kyc.html')
def mca_4(request): return render(request,'mca/auditor_appointment.html')
def mca_5(request): return render(request,'mca/company_amendments.html')
def mca_6(request): return render(request,'mca/llp_amendments.html')
def mca_7(request): return render(request,'mca/share_transfer.html')
def mca_8(request): return render(request,'mca/registers_minutes.html')
def mca_9(request): return render(request,'mca/xbrl.html')
def mca_10(request): return render(request,'mca/strike_off.html')
def mca_11(request): return render(request,'mca/business_conversions.html')

# ===== HEAD 6 =====
def accounts_1(request): return render(request,'accounting/cloud_bookkeeping.html')
def accounts_2(request): return render(request,'accounting/bank_reconciliation.html')
def accounts_3(request): return render(request,'accounting/financial_statements.html')
def accounts_4(request): return render(request,'accounting/ap_ar.html')
def accounts_5(request): return render(request,'accounting/mis_reports.html')
def accounts_6(request): return render(request,'accounting/payroll_processing.html')
def accounts_7(request): return render(request,'accounting/pf_esi_pt.html')
def accounts_8(request): return render(request,'accounting/virtual_ca.html')

# ===== HEAD 7 =====
def nri_1(request): return render(request,'nri/nri_itr.html')
def nri_2(request): return render(request,'nri/form15ca.html')
def nri_3(request): return render(request,'nri/dtaa.html')
def nri_4(request): return render(request,'nri/fema_fdi.html')
def nri_5(request): return render(request,'nri/india_entry.html')
def nri_6(request): return render(request,'nri/us_tax_return.html')
def nri_7(request): return render(request,'nri/us_bookkeeping.html')
def nri_8(request): return render(request,'nri/us_payroll.html')
def nri_9(request): return render(request,'nri/uk_bookkeeping.html')
def nri_10(request): return render(request,'nri/uk_accounts.html')
def nri_11(request): return render(request,'nri/uk_payroll.html')
def nri_12(request): return render(request,'nri/offshore_uk_accounting_team.html')
def nri_13(request): return render(request,'nri/repatriation_of_funds_advisory.html')
def nri_14(request): return render(request,'nri/nro_nre_account_advisory.html')
def nri_15(request): return render(request,'nri/nri_property_sale_tax_planning_compliance.html')

# ===== HEAD 8 =====
def vcfo_1(request): return render(request,'virtual_cfo/basic_virtual_cfo.html')
def vcfo_2(request): return render(request,'virtual_cfo/growth_virtual_cfo.html')
def vcfo_3(request): return render(request,'virtual_cfo/startup_advisory.html')

# ===== HEAD 9 =====
def other_0(request): return render(request,'other_services/dpdp_act_compliance_services.html')
def other_1(request): return render(request,'other_services/trademark.html')
def other_2(request): return render(request,'other_services/rera.html')
def other_3(request): return render(request,'other_services/legal_agreements.html')
def other_4(request): return render(request,'other_services/business_valuation.html')
def other_5(request): return render(request,'other_services/financial_planning.html')
def other_6(request): return render(request,'other_services/loan_credit.html')
def other_7(request): return render(request,'other_services/cashflow.html')
def other_8(request): return render(request,'other_services/project_reports.html')
def other_9(request): return render(request,'other_services/govt_schemes.html')
def other_10(request): return render(request,'other_services/software_setup.html')
def other_11(request): return render(request,'other_services/ibc.html')
def other_12(request): return render(request,'other_services/audit_services.html')