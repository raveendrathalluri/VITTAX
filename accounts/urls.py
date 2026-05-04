# accounts/urls.py
# COMPLETE ALL 9 HEADS (ready structure)

from django.urls import path
from . import views

urlpatterns = [

    # Main Pages
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('about/', views.about_view, name='about'),
    path('pricing/', views.pricing_view, name='pricing'),

    # ==================================================
    # HEAD 1 - Start a Business
    # ==================================================
    path('start_business/proprietorship/', views.proprietorship, name='proprietorship'),
    path('start_business/partnership_firm/', views.partnership_firm, name='partnership_firm'),
    path('start_business/llp/', views.llp, name='llp'),
    path('start_business/opc/', views.opc, name='opc'),
    path('start_business/private_limited_company/', views.private_limited_company, name='private_limited_company'),
    path('start_business/section8_company/', views.section8_company, name='section8_company'),
    path('start_business/producer_company/', views.producer_company, name='producer_company'),
    path('start_business/nidhi_company/', views.nidhi_company, name='nidhi_company'),
    path('start_business/trust_registration/', views.trust_registration, name='trust_registration'),

    # ==================================================
    # HEAD 2 - Registrations
    # ==================================================
    path('registrations/gst_registration/', views.gst_registration, name='gst_registration'),
    path('registrations/msme_registration/', views.msme_registration, name='msme_registration'),
    path('registrations/shop_establishment/', views.shop_establishment, name='shop_establishment'),
    
    path('registrations/trade_license/', views.trade_license, name='trade_license'),
    path('registrations/local_labour_licences/', views.local_labour_licences, name='local_labour_licences'),
    path('registrations/professional_tax/', views.professional_tax, name='professional_tax'),
    
    path('registrations/pf_registration/', views.pf_registration, name='pf_registration'),
    path('registrations/esi_registration/', views.esi_registration, name='esi_registration'),
    path('registrations/fssai/', views.fssai, name='fssai'),
    
    path('registrations/import_export_code/', views.import_export_code, name='import_export_code'),
    path('registrations/bis_registration/', views.bis_registration, name='bis_registration'),
    path('registrations/barcode_registration/', views.barcode_registration, name='barcode_registration'),
    
    path('registrations/drug_license/', views.drug_license, name='drug_license'),
    path('registrations/startup_registration/', views.startup_registration, name='startup_registration'),
    path('registrations/dpiit_recognition/', views.dpiit_recognition, name='dpiit_recognition'),
    
    path('registrations/darpan_registration/', views.darpan_registration, name='darpan_registration'),
    path('registrations/12a_registration/', views.a12_registration, name='12a_registration'),
    path('registrations/80g_registration/', views.g80_registration, name='80g_registration'),

    path('registrations/dsc/', views.dsc, name='dsc'),
    path('registrations/iso_advisory/', views.iso_advisory, name='iso_advisory'),

    # =========================
# HEAD 3 : GST & Indirect Tax
# =========================
path('gst/gst_registration/', views.gst_service_1, name='gst_service_1'),
path('gst/gst_returns/', views.gst_service_2, name='gst_service_2'),
path('gst/gst_returns_correction/', views.gst_service_3, name='gst_service_3'),
path('gst/gst_invoicing_setup/', views.gst_service_4, name='gst_service_4'),
path('gst/e_way_bill/', views.gst_service_5, name='gst_service_5'),
path('gst/itc_advisory/', views.gst_service_6, name='gst_service_6'),
path('gst/gstr9_audit/', views.gst_service_7, name='gst_service_7'),
path('gst/gst_refund/', views.gst_service_8, name='gst_service_8'),
path('gst/gst_notices/', views.gst_service_9, name='gst_service_9'),
path('gst/gst_health_check/', views.gst_service_10, name='gst_service_10'),
path('gst/export_sez/', views.gst_service_11, name='gst_service_11'),
path('gst/ecommerce_gst/', views.gst_service_12, name='gst_service_12'),
path('gst/gst_training/', views.gst_service_13, name='gst_service_13'),

# =========================
# HEAD 4 : Income Tax
# =========================
path('income_tax/itr_filing/', views.income_tax_1, name='income_tax_1'),
path('income_tax/tax_planning/', views.income_tax_2, name='income_tax_2'),
path('income_tax/tds_tcs/', views.income_tax_3, name='income_tax_3'),
path('income_tax/capital_gains/', views.income_tax_4, name='income_tax_4'),
path('income_tax/advance_tax/', views.income_tax_5, name='income_tax_5'),
path('income_tax/tax_notices/', views.income_tax_6, name='income_tax_6'),
path('income_tax/appeals/', views.income_tax_7, name='income_tax_7'),
path('income_tax/form15ca_15cb/', views.income_tax_8, name='income_tax_8'),
path('income_tax/pan_tan/', views.income_tax_9, name='income_tax_9'),

# =========================
# HEAD 5 : MCA
# =========================
path('mca/company_annual_filings/', views.mca_1, name='mca_1'),
path('mca/llp_annual_filings/', views.mca_2, name='mca_2'),
path('mca/director_kyc/', views.mca_3, name='mca_3'),
path('mca/auditor_appointment/', views.mca_4, name='mca_4'),
path('mca/company_amendments/', views.mca_5, name='mca_5'),
path('mca/llp_amendments/', views.mca_6, name='mca_6'),
path('mca/share_transfer/', views.mca_7, name='mca_7'),
path('mca/registers_minutes/', views.mca_8, name='mca_8'),
path('mca/xbrl/', views.mca_9, name='mca_9'),
path('mca/strike_off/', views.mca_10, name='mca_10'),
path('mca/business_conversions/', views.mca_11, name='mca_11'),

# =========================
# HEAD 6 : Accounting
# =========================
path('accounting/cloud_bookkeeping/', views.accounts_1, name='accounts_1'),
path('accounting/bank_reconciliation/', views.accounts_2, name='accounts_2'),
path('accounting/financial_statements/', views.accounts_3, name='accounts_3'),
path('accounting/ap_ar/', views.accounts_4, name='accounts_4'),
path('accounting/mis_reports/', views.accounts_5, name='accounts_5'),
path('accounting/payroll_processing/', views.accounts_6, name='accounts_6'),
path('accounting/pf_esi_pt/', views.accounts_7, name='accounts_7'),
path('accounting/virtual_ca/', views.accounts_8, name='accounts_8'),

# =========================
# HEAD 7 : NRI
# =========================
path('nri/nri_itr/', views.nri_1, name='nri_1'),
path('nri/form15ca/', views.nri_2, name='nri_2'),
path('nri/dtaa/', views.nri_3, name='nri_3'),
path('nri/fema_fdi/', views.nri_4, name='nri_4'),
path('nri/india_entry/', views.nri_5, name='nri_5'),
path('nri/us_tax_return/', views.nri_6, name='nri_6'),
path('nri/us_bookkeeping/', views.nri_7, name='nri_7'),
path('nri/us_payroll/', views.nri_8, name='nri_8'),
path('nri/uk_bookkeeping/', views.nri_9, name='nri_9'),
path('nri/uk_accounts/', views.nri_10, name='nri_10'),
path('nri/uk_payroll/', views.nri_11, name='nri_11'),
path('nri/offshore_uk_accounting_team/', views.nri_12, name='nri_12'),
path('nri/repatriation_of_funds_advisory/', views.nri_13, name='nri_13'),
path('nri/nro_nre_account_advisory/', views.nri_14, name='nri_14'),
path('nri/nri_property_sale_tax_planning_compliance/', views.nri_15, name='nri_15'),

# =========================
# HEAD 8 : Virtual CFO
# =========================
path('virtual_cfo/basic_virtual_cfo/', views.vcfo_1, name='vcfo_1'),
path('virtual_cfo/growth_virtual_cfo/', views.vcfo_2, name='vcfo_2'),
path('virtual_cfo/startup_advisory/', views.vcfo_3, name='vcfo_3'),

# =========================
# HEAD 9 : Other Services
# =========================
path('other_services/dpdp_act_compliance_services/', views.other_0, name='other_0'),
path('other_services/trademark/', views.other_1, name='other_1'),
path('other_services/rera/', views.other_2, name='other_2'),
path('other_services/legal_agreements/', views.other_3, name='other_3'),
path('other_services/business_valuation/', views.other_4, name='other_4'),
path('other_services/financial_planning/', views.other_5, name='other_5'),
path('other_services/loan_credit/', views.other_6, name='other_6'),
path('other_services/cashflow/', views.other_7, name='other_7'),
path('other_services/project_reports/', views.other_8, name='other_8'),
path('other_services/govt_schemes/', views.other_9, name='other_9'),
path('other_services/software_setup/', views.other_10, name='other_10'),
path('other_services/ibc/', views.other_11, name='other_11'),
path('other_services/audit_services/', views.other_12, name='other_12'),
]