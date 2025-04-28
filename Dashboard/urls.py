from django.urls import path
from Dashboard import views

urlpatterns = [
    #Acceuil
    path('acceuil/', views.acceuil, name='acceuil'),
    path('acceuil_pie/', views.acceuil_pie, name='acceuil_pie'),
    path('acceuil_pie_error/', views.acceuil_pie_error, name='acceuil_pie_error'),
    path('acceuil_area/', views.acceuil_area, name='acceuil_area'),
    path('acceuil_bar/', views.acceuil_bar, name='acceuil_bar'),
    path('acceuil_bar_line/', views.acceuil_bar_line, name='acceuil_bar_line'),
    path('acceuil_bar_line_error/', views.acceuil_bar_line_error, name='acceuil_bar_line_error'),
    path('charts/', views.charts, name='charts'), 
    path('tables/', views.tables, name='tables'),
    
    #Erreur
    path('404/', views.error, name='404'),
    path('blank/', views.blank, name='blank'),
    
    #DMC
    path('dmc/', views.dmc_datatable, name='dmc'),
    path('dmc_pie/', views.dmc_pie, name='dmc_pie'),
    path('dmc_pie_error/', views.dmc_pie_error, name='dmc_pie_error'),
    path('dmc_area/', views.dmc_area, name='dmc_area'),
    path('dmc_bar/', views.dmc_bar, name='dmc_bar'),
    path('dmc_bar_line/', views.dmc_bar_line, name='dmc_bar_line'),
    path('dmc_bar_line_error/', views.dmc_bar_line_error, name='dmc_bar_line_error'),
    
    #EIR
    path('eir/', views.eir_datatable, name='eir'),
    path('eir_pie/', views.eir_pie, name='eir_pie'),
    path('eir_pie_error/', views.eir_pie_error, name='eir_pie_error'),
    path('eir_area/', views.eir_area, name='eir_area'),
    path('eir_bar/', views.eir_bar, name='eir_bar'),
    path('eir_bar_line/', views.eir_bar_line, name='eir_bar_line'),
    path('eir_bar_line_error/', views.eir_bar_line_error, name='eir_bar_line_error'),
    
    #MCN
    path('mcn/', views.mcn_datatable, name='mcn'),
    path('mcn_pie/', views.mcn_pie, name='mcn_pie'),
    path('mcn_pie_error/', views.mcn_pie_error, name='mcn_pie_error'),
    path('mcn_area/', views.mcn_area, name='mcn_area'),
    path('mcn_bar/', views.mcn_bar, name='mcn_bar'),
    path('mcn_bar_line/', views.mcn_bar_line, name='mcn_bar_line'),
    path('mcn_bar_line_error/', views.mcn_bar_line_error, name='mcn_bar_line_error'),
    
    #VMS
    path('vms/', views.vms_datatable, name='vms'),
    path('vms_pie/', views.vms_pie, name='vms_pie'),
    path('vms_pie_error/', views.vms_pie_error, name='vms_pie_error'),
    path('vms_area/', views.vms_area, name='vms_area'),
    path('vms_bar/', views.vms_bar, name='vms_bar'),
    path('vms_bar_line/', views.vms_bar_line, name='vms_bar_line'),
    path('vms_bar_line_error/', views.vms_bar_line_error, name='vms_bar_line_error'),
    
    #IVR
    path('ivr/', views.ivr_datatable, name='ivr'),
    path('ivr_pie/', views.ivr_pie, name='ivr_pie'),
    path('ivr_pie_error/', views.ivr_pie_error, name='ivr_pie_error'),
    path('ivr_area/', views.ivr_area, name='ivr_area'),
    path('ivr_bar/', views.ivr_bar, name='ivr_bar'),
    path('ivr_bar_line/', views.ivr_bar_line, name='ivr_bar_line'),
    path('ivr_bar_line_error/', views.ivr_bar_line_error, name='ivr_bar_line_error'),
    
    #OBD
    path('obd/', views.obd_datatable, name='obd'),
    path('obd_pie/', views.obd_pie, name='obd_pie'),
    path('obd_pie_error/', views.obd_pie_error, name='obd_pie_error'),
    path('obd_area/', views.obd_area, name='obd_area'),
    path('obd_bar/', views.obd_bar, name='obd_bar'),
    path('obd_bar_line/', views.obd_bar_line, name='obd_bar_line'),
    path('obd_bar_line_error/', views.obd_bar_line_error, name='obd_bar_line_error'),
    
    #Collect Call
    path('collect_call/', views.collect_call_datatable, name='collect_call'),
    path('collect_call_pie/', views.collect_call_pie, name='collect_call_pie'),
    path('collect_call_pie_error/', views.collect_call_pie_error, name='collect_call_pie_error'),
    path('collect_call_area/', views.collect_call_area, name='collect_call_area'),
    path('collect_call_bar/', views.collect_call_bar, name='collect_call_bar'),
    path('collect_call_bar_line/', views.collect_call_bar_line, name='collect_call_bar_line'),
    path('collect_call_bar_line_error/', views.collect_call_bar_line_error, name='collect_call_bar_line_error'),
    
    #Autocall Completion
    path('autocall_completion/', views.autocall_completion_datatable, name='autocall_completion'),
    path('autocall_completion_pie/', views.autocall_completion_pie, name='autocall_completion_pie'),
    path('autocall_completion_pie_error/', views.autocall_completion_pie_error, name='autocall_completion_pie_error'),
    path('autocall_completion_area/', views.autocall_completion_area, name='autocall_completion_area'),
    path('autocall_completion_bar/', views.autocall_completion_bar, name='autocall_completion_bar'),
    path('autocall_completion_bar_line/', views.autocall_completion_bar_line, name='autocall_completion_bar_line'),
    path('autocall_completion_bar_line_error/', views.autocall_completion_bar_line_error, name='autocall_completion_bar_line_error'),
    
    #CRBT
    path('crbt/', views.crbt_datatable, name='crbt'),
    path('crbt_pie/', views.crbt_pie, name='crbt_pie'),
    path('crbt_pie_error/', views.crbt_pie_error, name='crbt_pie_error'),
    path('crbt_area/', views.crbt_area, name='crbt_area'),
    path('crbt_bar/', views.crbt_bar, name='crbt_bar'),
    path('crbt_bar_line/', views.crbt_bar_line, name='crbt_bar_line'),
    path('crbt_bar_line_error/', views.crbt_bar_line_error, name='crbt_bar_line_error'),
    
    #SMS PRO
    path('sms_pro/', views.sms_pro_view1, name='sms_pro'),
    path('sms_pro_pie/', views.sms_pro_pie, name='sms_pro_pie'),
    path('sms_pro_pie_error/', views.sms_pro_pie_error, name='sms_pro_pie_error'),
    path('sms_pro_area/', views.sms_pro_area, name='sms_pro_area'),
    path('sms_pro_bar/', views.sms_pro_bar, name='sms_pro_bar'),
    path('sms_pro_bar_line/', views.sms_pro_bar_line, name='sms_pro_bar_line'),
    path('sms_Pro_bar_line_error/', views.sms_Pro_bar_line_error, name='sms_Pro_bar_line_error'),
    path('get_sheets/', views.get_sheets, name='get_sheets'),
    path('get_sheets_error/', views.get_sheets_error, name='get_sheets_error'),
    
    #SMS
    path('sms/', views.sms_datatable, name='sms'),
    path('sms_pie/', views.sms_pie, name='sms_pie'),
    path('sms_pie_error/', views.sms_pie_error, name='sms_pie_error'),
    path('sms_area/', views.sms_area, name='sms_area'),
    path('sms_bar/', views.sms_bar, name='sms_bar'),
    path('sms_bar_line/', views.sms_bar_line, name='sms_bar_line'),
    path('sms_bar_line_error/', views.sms_bar_line_error, name='sms_bar_line_error'),
    
    #USSD
    path('ussd/', views.ussd_datatable, name='ussd'),
    path('ussd_pie/', views.ussd_pie, name='ussd_pie'),
    path('ussd_pie_error/', views.ussd_pie_error, name='ussd_pie_error'),
    path('ussd_area/', views.ussd_area, name='ussd_area'),
    path('ussd_bar/', views.ussd_bar, name='ussd_bar'),
    path('ussd_bar_line/', views.ussd_bar_line, name='ussd_bar_line'),
    path('ussd_bar_line_error/', views.ussd_bar_line_error, name='ussd_bar_line_error'),
    # Utiliser le nom de fonction correct
    # path('register/', views.signup, name="register"),
    # path('deconnexion/', views.deconnexion, name="logout"),
]