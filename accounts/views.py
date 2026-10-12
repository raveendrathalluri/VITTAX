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


def service_list_view(request):
    """Service list directory displaying all top-bar services & sub-services with filters"""
    categories = [
        {
            'slug': 'start-business',
            'title': 'Start a Business',
            'description': 'End-to-end entity registration and business setup solutions for entrepreneurs.',
            'icon': 'fas fa-rocket',
            'sub_services': [
                {'title': 'Sole Proprietorship Setup', 'url_name': 'proprietorship', 'desc': 'Quick registration for single-owner businesses with full GST & MSME setup.', 'icon': 'fas fa-user-tie', 'badge': 'Registration'},
                {'title': 'Partnership Firm Registration', 'url_name': 'partnership_firm', 'desc': 'Deed drafting, notarisation & registrar filing for partnership firms.', 'icon': 'fas fa-users', 'badge': 'Registration'},
                {'title': 'Limited Liability Partnership (LLP)', 'url_name': 'llp', 'desc': 'Combine limited liability protection with operational flexibility of partnerships.', 'icon': 'fas fa-handshake', 'badge': 'Popular'},
                {'title': 'One Person Company (OPC)', 'url_name': 'opc', 'desc': 'Corporate structure tailored for solo entrepreneurs with limited liability.', 'icon': 'fas fa-user-shield', 'badge': 'Corporate'},
                {'title': 'Private Limited Company', 'url_name': 'private_limited_company', 'desc': 'India’s most popular company structure for startups & growing enterprises.', 'icon': 'fas fa-building', 'badge': 'Popular'},
                {'title': 'Section 8 Company (NGO / Non-Profit)', 'url_name': 'section8_company', 'desc': 'Establish a non-profit organization registered under the Companies Act.', 'icon': 'fas fa-hands-helping', 'badge': 'NGO'},
                {'title': 'Producer Company Registration', 'url_name': 'producer_company', 'desc': 'Registration for agricultural and primary producer collectives.', 'icon': 'fas fa-tractor', 'badge': 'Agri'},
                {'title': 'Nidhi Company Registration', 'url_name': 'nidhi_company', 'desc': 'Registration for non-banking finance entity operating among members.', 'icon': 'fas fa-piggy-bank', 'badge': 'NBFC'},
                {'title': 'Trust Registration', 'url_name': 'trust_registration', 'desc': 'Public or private trust deed registration & charity commissioner filing.', 'icon': 'fas fa-landmark', 'badge': 'Trust'},
            ]
        },
        {
            'slug': 'registrations',
            'title': 'Registrations & Licenses',
            'description': 'Mandatory government licenses, registrations, and certifications for business compliance.',
            'icon': 'fas fa-certificate',
            'sub_services': [
                {'title': 'GST Registration', 'url_name': 'gst_registration', 'desc': 'New GSTIN registration for businesses within 3-5 working days.', 'icon': 'fas fa-receipt', 'badge': 'Popular'},
                {'title': 'MSME / Udyam Registration', 'url_name': 'msme_registration', 'desc': 'Government MSME certification for subsidies, low interest & tender priority.', 'icon': 'fas fa-industry', 'badge': 'Govt Scheme'},
                {'title': 'Shops & Establishments', 'url_name': 'shop_establishment', 'desc': 'State labor department registration for physical shop or commercial office.', 'icon': 'fas fa-store', 'badge': 'State License'},
                {'title': 'Trade License', 'url_name': 'trade_license', 'desc': 'Municipal corporation permit to legally carry out business activities.', 'icon': 'fas fa-id-card', 'badge': 'Municipal'},
                {'title': 'Local Labour Licences', 'url_name': 'local_labour_licences', 'desc': 'Contract labor license & state labor registration compliance.', 'icon': 'fas fa-hard-hat', 'badge': 'Labour'},
                {'title': 'Professional Tax (PT)', 'url_name': 'professional_tax', 'desc': 'PT registration & return filing for employers and self-employed.', 'icon': 'fas fa-percent', 'badge': 'State Tax'},
                {'title': 'PF Registration', 'url_name': 'pf_registration', 'desc': 'Employee Provident Fund registration & code allocation.', 'icon': 'fas fa-piggy-bank', 'badge': 'PF'},
                {'title': 'ESI Registration', 'url_name': 'esi_registration', 'desc': 'Employees State Insurance registration & employer code setup.', 'icon': 'fas fa-heartbeat', 'badge': 'ESI'},
                {'title': 'FSSAI License', 'url_name': 'fssai', 'desc': 'Basic, State & Central FSSAI food license for food businesses & cloud kitchens.', 'icon': 'fas fa-utensils', 'badge': 'Food Safety'},
                {'title': 'IEC Registration', 'url_name': 'import_export_code', 'desc': 'Import Export Code registration from DGFT for international trade.', 'icon': 'fas fa-ship', 'badge': 'Import/Export'},
                {'title': 'BIS Registration', 'url_name': 'bis_registration', 'desc': 'Bureau of Indian Standards hallmarking & quality certification.', 'icon': 'fas fa-check-double', 'badge': 'Quality'},
                {'title': 'Barcode Registration', 'url_name': 'barcode_registration', 'desc': 'GS1 barcode registration for retail products & e-commerce listings.', 'icon': 'fas fa-barcode', 'badge': 'GS1'},
                {'title': 'Drug Licence', 'url_name': 'drug_license', 'desc': 'Retail & wholesale drug license registration from State FDA.', 'icon': 'fas fa-capsules', 'badge': 'Pharma'},
                {'title': 'Startup Registration', 'url_name': 'startup_registration', 'desc': 'Recognition under Startup India program for tax exemption benefits.', 'icon': 'fas fa-space-shuttle', 'badge': 'Startup'},
                {'title': 'DPIIT Recognition', 'url_name': 'dpiit_recognition', 'desc': 'DPIIT certificate for Section 56 exemption & IPR fast-tracking.', 'icon': 'fas fa-award', 'badge': 'DPIIT'},
                {'title': 'Darpan Registration', 'url_name': 'darpan_registration', 'desc': 'NITI Aayog NGO Darpan portal enrollment for government grants.', 'icon': 'fas fa-sitemap', 'badge': 'NGO'},
                {'title': '12A Registration', 'url_name': '12a_registration', 'desc': 'Income Tax 12A exemption certificate for trusts and NGOs.', 'icon': 'fas fa-file-contract', 'badge': 'Tax Exemption'},
                {'title': '80G Registration', 'url_name': '80g_registration', 'desc': '80G certification enabling donors to claim tax deductions.', 'icon': 'fas fa-donate', 'badge': 'Tax Exemption'},
                {'title': 'DSC (Digital Signature)', 'url_name': 'dsc', 'desc': 'Class 3 Digital Signature Certificate issuance with USB token.', 'icon': 'fas fa-key', 'badge': 'Digital'},
                {'title': 'ISO Advisory', 'url_name': 'iso_advisory', 'desc': 'ISO 9001, 27001 & 22000 quality audit & certification guidance.', 'icon': 'fas fa-medal', 'badge': 'ISO'},
            ]
        },
        {
            'slug': 'gst-tax',
            'title': 'GST & Indirect Tax',
            'description': 'Complete GST compliance, return filing, audits, advisory, and litigation management.',
            'icon': 'fas fa-receipt',
            'sub_services': [
                {'title': 'GST Registration', 'url_name': 'gst_service_1', 'desc': 'Hassle-free GSTIN registration with document verification.', 'icon': 'fas fa-file-invoice', 'badge': 'Registration'},
                {'title': 'GST Returns Filing', 'url_name': 'gst_service_2', 'desc': 'GSTR-1, GSTR-3B, QRMP & Composition scheme return filing.', 'icon': 'fas fa-file-alt', 'badge': 'Popular'},
                {'title': 'GST Returns Correction', 'url_name': 'gst_service_3', 'desc': 'Rectification of errors in previous returns & ITC reconciliations.', 'icon': 'fas fa-edit', 'badge': 'Correction'},
                {'title': 'GST Invoicing Setup', 'url_name': 'gst_service_4', 'desc': 'E-invoicing integration & compliant invoice template design.', 'icon': 'fas fa-cash-register', 'badge': 'Setup'},
                {'title': 'E-Way Bill Management', 'url_name': 'gst_service_5', 'desc': 'E-Way bill generation, extension & transit compliance support.', 'icon': 'fas fa-truck', 'badge': 'Logistics'},
                {'title': 'Input Tax Credit (ITC) Advisory', 'url_name': 'gst_service_6', 'desc': 'Maximize eligible ITC claims & 2A/2B monthly matching.', 'icon': 'fas fa-coins', 'badge': 'Advisory'},
                {'title': 'GST Annual Return (GSTR-9/9C)', 'url_name': 'gst_service_7', 'desc': 'Annual return filing & self-certified reconciliation statement.', 'icon': 'fas fa-clipboard-check', 'badge': 'Annual'},
                {'title': 'GST Refund Services', 'url_name': 'gst_service_8', 'desc': 'Refund processing for inverted duty structure & unutilized ITC.', 'icon': 'fas fa-undo-alt', 'badge': 'Refund'},
                {'title': 'GST Notices & Litigation', 'url_name': 'gst_service_9', 'desc': 'Drafting reply to ASMT-10, DRC-01 & representation before authorities.', 'icon': 'fas fa-balance-scale', 'badge': 'Legal'},
                {'title': 'GST Health Check', 'url_name': 'gst_service_10', 'desc': 'Comprehensive internal audit to identify tax exposure & risks.', 'icon': 'fas fa-stethoscope', 'badge': 'Audit'},
                {'title': 'Export & SEZ GST Advisory', 'url_name': 'gst_service_11', 'desc': 'LUT filing, zero-rated supply compliance & SEZ invoicing.', 'icon': 'fas fa-globe-asia', 'badge': 'Export'},
                {'title': 'E-commerce GST Compliance', 'url_name': 'gst_service_12', 'desc': 'TCS compliance & multi-state GST filing for online sellers.', 'icon': 'fas fa-shopping-cart', 'badge': 'E-commerce'},
                {'title': 'GST Training & Support', 'url_name': 'gst_service_13', 'desc': 'Customized staff training & on-call GST advisory support.', 'icon': 'fas fa-chalkboard-teacher', 'badge': 'Training'},
            ]
        },
        {
            'slug': 'income-tax',
            'title': 'Income Tax',
            'description': 'Personal and corporate tax filing, tax saving advisory, advance tax, and notice resolution.',
            'icon': 'fas fa-calculator',
            'sub_services': [
                {'title': 'ITR Filing (Individuals & Corporates)', 'url_name': 'income_tax_1', 'desc': 'Accurate ITR-1 to ITR-7 filing with maximum tax saving optimization.', 'icon': 'fas fa-file-invoice-dollar', 'badge': 'Popular'},
                {'title': 'Tax Planning & Advisory', 'url_name': 'income_tax_2', 'desc': 'Strategic tax optimization under Old vs New tax regimes.', 'icon': 'fas fa-chart-pie', 'badge': 'Planning'},
                {'title': 'TDS / TCS Compliance', 'url_name': 'income_tax_3', 'desc': 'Quarterly Form 24Q, 26Q, 27Q return filing & TDS certificate generation.', 'icon': 'fas fa-percentage', 'badge': 'TDS'},
                {'title': 'Capital Gains Tax Planning', 'url_name': 'income_tax_4', 'desc': 'Tax minimization on stock market gains, crypto & property sales.', 'icon': 'fas fa-chart-line', 'badge': 'Capital Gains'},
                {'title': 'Advance Tax Computation', 'url_name': 'income_tax_5', 'desc': 'Quarterly advance tax calculations to avoid Section 234B/C interest.', 'icon': 'fas fa-calendar-alt', 'badge': 'Tax Planning'},
                {'title': 'Tax Notice Representation', 'url_name': 'income_tax_6', 'desc': 'Expert handling of Section 142(1), 143(1), 148 notices.', 'icon': 'fas fa-exclamation-triangle', 'badge': 'Notices'},
                {'title': 'Income Tax Appeal Filing', 'url_name': 'income_tax_7', 'desc': 'Drafting grounds of appeal & representation before CIT(A) and ITAT.', 'icon': 'fas fa-gavel', 'badge': 'Appeals'},
                {'title': 'Form 15CA / 15CB Certificates', 'url_name': 'income_tax_8', 'desc': 'CA certification for foreign outward remittances & Bank filing.', 'icon': 'fas fa-exchange-alt', 'badge': 'Remittance'},
                {'title': 'PAN & TAN Registration', 'url_name': 'income_tax_9', 'desc': 'New PAN/TAN application, correction & instant e-PAN assistance.', 'icon': 'fas fa-id-badge', 'badge': 'PAN/TAN'},
            ]
        },
        {
            'slug': 'mca-corporate',
            'title': 'MCA & Corporate Compliance',
            'description': 'Annual ROC filings, director compliances, corporate amendments, and statutory registers.',
            'icon': 'fas fa-city',
            'sub_services': [
                {'title': 'Company Annual Filings (AOC-4 & MGT-7)', 'url_name': 'mca_1', 'desc': 'Mandatory annual ROC filing for Private Limited companies.', 'icon': 'fas fa-folder-open', 'badge': 'ROC Filing'},
                {'title': 'LLP Annual Filings (Form 11 & Form 8)', 'url_name': 'mca_2', 'desc': 'Annual solvency statement & annual return filing for LLPs.', 'icon': 'fas fa-file-signature', 'badge': 'LLP ROC'},
                {'title': 'Director’s KYC & DIN', 'url_name': 'mca_3', 'desc': 'Annual DIR-3 KYC filing, DIN activation & DSC renewal.', 'icon': 'fas fa-user-check', 'badge': 'Director'},
                {'title': 'ADT-1 Auditor Appointment', 'url_name': 'mca_4', 'desc': 'ROC filing for statutory auditor appointment or replacement.', 'icon': 'fas fa-user-tie', 'badge': 'Auditor'},
                {'title': 'Company Amendments', 'url_name': 'mca_5', 'desc': 'Change of name, registered office, capital increase, MOA/AOA update.', 'icon': 'fas fa-pen-fancy', 'badge': 'Amendment'},
                {'title': 'LLP Amendments', 'url_name': 'mca_6', 'desc': 'Add/remove partners, change LLP agreement & registered address.', 'icon': 'fas fa-user-edit', 'badge': 'LLP Amendment'},
                {'title': 'Share Transfer Assistance', 'url_name': 'mca_7', 'desc': 'SH-4 drafting, stamp duty payment & share transfer filing.', 'icon': 'fas fa-exchange-alt', 'badge': 'Shares'},
                {'title': 'Statutory Registers & Minutes', 'url_name': 'mca_8', 'desc': 'Preparation of Board meeting minutes, AGM records & statutory registers.', 'icon': 'fas fa-book-open', 'badge': 'Compliance'},
                {'title': 'XBRL Filing', 'url_name': 'mca_9', 'desc': 'XBRL conversion & filing for eligible companies.', 'icon': 'fas fa-code', 'badge': 'XBRL'},
                {'title': 'Strike Off & Winding Up', 'url_name': 'mca_10', 'desc': 'Defunct company or LLP closure through STK-2 / Form 24 filing.', 'icon': 'fas fa-window-close', 'badge': 'Closure'},
                {'title': 'Business Conversions', 'url_name': 'mca_11', 'desc': 'Seamless conversion of Partnership to LLP or LLP to Pvt Ltd.', 'icon': 'fas fa-sync-alt', 'badge': 'Conversion'},
            ]
        },
        {
            'slug': 'accounting-payroll',
            'title': 'Accounting & Payroll',
            'description': 'Cloud bookkeeping, bank reconciliation, financial statements, and employee payroll management.',
            'icon': 'fas fa-book',
            'sub_services': [
                {'title': 'Cloud Bookkeeping', 'url_name': 'accounts_1', 'desc': 'Real-time accounting on Tally, Zoho Books, QuickBooks & Xero.', 'icon': 'fas fa-cloud-upload-alt', 'badge': 'Popular'},
                {'title': 'Bank Reconciliation Statement', 'url_name': 'accounts_2', 'desc': 'Monthly bank statement matching with ledger entries.', 'icon': 'fas fa-university', 'badge': 'BRS'},
                {'title': 'Financial Statements Preparation', 'url_name': 'accounts_3', 'desc': 'Profit & Loss account, Balance Sheet & Cash Flow statements.', 'icon': 'fas fa-file-invoice', 'badge': 'Financials'},
                {'title': 'Accounts Payable & Receivable', 'url_name': 'accounts_4', 'desc': 'Vendor payment management & customer aging analysis.', 'icon': 'fas fa-money-bill-wave', 'badge': 'Cashflow'},
                {'title': 'MIS Reports & Analytics', 'url_name': 'accounts_5', 'desc': 'Customized management reporting for decision making.', 'icon': 'fas fa-chart-bar', 'badge': 'MIS'},
                {'title': 'Payroll Processing', 'url_name': 'accounts_6', 'desc': 'End-to-end salary processing, payslips & Form 16 issuance.', 'icon': 'fas fa-users-cog', 'badge': 'Payroll'},
                {'title': 'PF / ESI / PT Monthly Returns', 'url_name': 'accounts_7', 'desc': 'Monthly ECR filing, PT challan payment & compliance records.', 'icon': 'fas fa-shield-alt', 'badge': 'Labour Tax'},
                {'title': 'Virtual CA Services', 'url_name': 'accounts_8', 'desc': 'Dedicated Chartered Accountant for financial governance & advice.', 'icon': 'fas fa-user-astronaut', 'badge': 'Virtual CA'},
            ]
        },
        {
            'slug': 'nri-international',
            'title': 'NRI & International Services',
            'description': 'Cross-border tax advisory, foreign remittance certificates, DTAA, US/UK tax filing.',
            'icon': 'fas fa-globe',
            'sub_services': [
                {'title': 'NRI Income Tax Return (ITR)', 'url_name': 'nri_1', 'desc': 'Specialized ITR filing for NRIs with global income & Indian assets.', 'icon': 'fas fa-plane-departure', 'badge': 'NRI Tax'},
                {'title': 'Form 145/146 Remittance Certs', 'url_name': 'nri_2', 'desc': 'CA Certificate for money transfer from NRO to overseas bank.', 'icon': 'fas fa-stamp', 'badge': 'Remittance'},
                {'title': 'DTAA Advisory', 'url_name': 'nri_3', 'desc': 'Double Taxation Avoidance Agreement relief & Tax Credit advice.', 'icon': 'fas fa-handshake-alt-slash', 'badge': 'DTAA'},
                {'title': 'FEMA / FDI / ODI Compliance', 'url_name': 'nri_4', 'desc': 'Foreign Direct Investment reporting & RBI compliance filings.', 'icon': 'fas fa-passport', 'badge': 'FEMA'},
                {'title': 'India Entry Setup', 'url_name': 'nri_5', 'desc': 'Liaison office, branch office & wholly-owned subsidiary incorporation.', 'icon': 'fas fa-flag', 'badge': 'FDI'},
                {'title': 'US Tax Return (Form 1040/1040-NR)', 'url_name': 'nri_6', 'desc': 'US federal & state tax return filing for expat Indians & US citizens.', 'icon': 'fas fa-flag-usa', 'badge': 'US Tax'},
                {'title': 'US Bookkeeping & Accounting', 'url_name': 'nri_7', 'desc': 'QuickBooks online bookkeeping for US LLCs & corporations.', 'icon': 'fas fa-dollar-sign', 'badge': 'US Accounting'},
                {'title': 'US Payroll Processing', 'url_name': 'nri_8', 'desc': 'US employee & contractor payroll through Gusto/ADP.', 'icon': 'fas fa-money-check-alt', 'badge': 'US Payroll'},
                {'title': 'UK Bookkeeping & Accounting', 'url_name': 'nri_9', 'desc': 'Xero/Dext bookkeeping for UK Limited companies.', 'icon': 'fas fa-pound-sign', 'badge': 'UK Accounting'},
                {'title': 'UK Year-End Accounts & Tax', 'url_name': 'nri_10', 'desc': 'Companies House annual accounts & HMRC Corporation Tax (CT600).', 'icon': 'fas fa-file-contract', 'badge': 'UK Tax'},
                {'title': 'UK Payroll & PAYE Compliance', 'url_name': 'nri_11', 'desc': 'Real Time Information (RTI) payroll & pension auto-enrolment.', 'icon': 'fas fa-users', 'badge': 'UK Payroll'},
                {'title': 'Offshore UK Accounting Team', 'url_name': 'nri_12', 'desc': 'Dedicated back-office accounting staff for UK accounting firms.', 'icon': 'fas fa-headset', 'badge': 'Outsourcing'},
                {'title': 'Repatriation of Funds Advisory', 'url_name': 'nri_13', 'desc': 'Repatriate sale proceeds of inherited or purchased Indian property.', 'icon': 'fas fa-redo', 'badge': 'Repatriation'},
                {'title': 'NRO / NRE Account Advisory', 'url_name': 'nri_14', 'desc': 'Guidance on banking setup, NRO to NRE transfer & tax liability.', 'icon': 'fas fa-credit-card', 'badge': 'Banking'},
                {'title': 'NRI Property Sale Tax Planning', 'url_name': 'nri_15', 'desc': 'Lower TDS certificate (Form 13) application & property sale capital gains.', 'icon': 'fas fa-home', 'badge': 'Property Tax'},
            ]
        },
        {
            'slug': 'virtual-cfo',
            'title': 'Virtual CFO & Advisory',
            'description': 'High-level financial strategy, cashflow management, fundraising readiness, and CA advisory.',
            'icon': 'fas fa-briefcase',
            'sub_services': [
                {'title': 'Basic Virtual CFO', 'url_name': 'vcfo_1', 'desc': 'Core financial oversight, budgeting & monthly performance review.', 'icon': 'fas fa-chart-line', 'badge': 'CFO'},
                {'title': 'Growth Virtual CFO', 'url_name': 'vcfo_2', 'desc': 'Advanced financial modeling, unit economics & working capital optimization.', 'icon': 'fas fa-rocket', 'badge': 'Popular'},
                {'title': 'Startup Advisory & Fundraising', 'url_name': 'vcfo_3', 'desc': 'Pitch deck review, valuation report, cap table & investor due diligence.', 'icon': 'fas fa-lightbulb', 'badge': 'Startup'},
            ]
        },
        {
            'slug': 'other-services',
            'title': 'Other Specialized Services',
            'description': 'DPDP compliance, trademark registration, RERA, legal contracts, business valuation, and audits.',
            'icon': 'fas fa-th-large',
            'sub_services': [
                {'title': 'DPDP Act Compliance Services', 'url_name': 'other_0', 'desc': 'Digital Personal Data Protection Act compliance & data privacy audit.', 'icon': 'fas fa-user-shield', 'badge': 'DPDP'},
                {'title': 'Trademark Registration', 'url_name': 'other_1', 'desc': 'Brand name & logo trademark application & objection defense.', 'icon': 'fas fa-trademark', 'badge': 'IPR'},
                {'title': 'RERA Registration & Compliance', 'url_name': 'other_2', 'desc': 'Real estate promoter & agent RERA registration & quarterly filings.', 'icon': 'fas fa-building', 'badge': 'RERA'},
                {'title': 'Legal Agreements & Contracts', 'url_name': 'other_3', 'desc': 'Drafting NDA, Founders agreement, SLA & Employment contracts.', 'icon': 'fas fa-file-signature', 'badge': 'Legal'},
                {'title': 'Business Valuation Services', 'url_name': 'other_4', 'desc': 'DCF & Market Multiple valuation reports by Registered Valuers.', 'icon': 'fas fa-calculator', 'badge': 'Valuation'},
                {'title': 'Personal Financial Planning', 'url_name': 'other_5', 'desc': 'Wealth management, retirement planning & portfolio analysis.', 'icon': 'fas fa-wallet', 'badge': 'Wealth'},
                {'title': 'Loan & Credit Advisory', 'url_name': 'other_6', 'desc': 'Bank loan project report, credit limit syndication & SME funding.', 'icon': 'fas fa-hand-holding-usd', 'badge': 'Banking'},
                {'title': 'Cash Flow Forecasting', 'url_name': 'other_7', 'desc': '12-month rolling cashflow forecast & liquidity management.', 'icon': 'fas fa-chart-area', 'badge': 'Forecast'},
                {'title': 'Project Reports / CMA Data', 'url_name': 'other_8', 'desc': 'Detailed Project Report (DPR) & CMA data for bank loan approvals.', 'icon': 'fas fa-file-alt', 'badge': 'CMA'},
                {'title': 'Govt Scheme Advisory', 'url_name': 'other_9', 'desc': 'Guidance & application support for MSME subsidies & state incentives.', 'icon': 'fas fa-landmark', 'badge': 'Govt Scheme'},
                {'title': 'Accounting Software Setup', 'url_name': 'other_10', 'desc': 'Tally Prime, Zoho Books & QuickBooks initial setup & chart of accounts.', 'icon': 'fas fa-desktop', 'badge': 'Software'},
                {'title': 'Insolvency & IBC Advisory', 'url_name': 'other_11', 'desc': 'Insolvency resolution advisory & Debt recovery proceedings support.', 'icon': 'fas fa-balance-scale-left', 'badge': 'IBC'},
                {'title': 'Audit & Assurance Services', 'url_name': 'other_12', 'desc': 'Internal audit, stock audit, statutory audit & tax audit assistance.', 'icon': 'fas fa-search-dollar', 'badge': 'Audit'},
            ]
        }
    ]

    total_count = sum(len(cat['sub_services']) for cat in categories)

    return render(request, 'service_list.html', {
        'categories': categories,
        'total_services_count': total_count,
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