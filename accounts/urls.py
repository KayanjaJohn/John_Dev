from django.urls import path
from . import views

urlpatterns = [
    path('', views.userLogin, name='userLogin'),
    path('userLogout/', views.userLogout, name='userLogout'),
    path('userRegistration/', views.userRegistration, name='userRegistration'),
    path('adminDashboard/', views.adminDashboard, name='adminDashboard'),
    path('users/', views.users_info, name='users'),
    path('members/update/<int:pk>/', views.update_member, name='update_member'),
    path('delete/<int:pk>/', views.delete_member, name='delete'),
    path('send-email/', views.send_email, name='send_email'),


    path('directorDashboard/', views.workPlanManagerDashboard, name='workPlanManagerDashboard'),
    path('workPlanManagerDashboard/', views.workPlanManagerDashboard, name='workPlanManagerDashboard'),
    path('strategyDashboard/', views.strategyDashboard, name='strategyDashboard'),
    path('managerDashboard/', views.managerDashboard, name='managerDashboard'),

    path('awp/', views.awp, name='awp'),
    path('awp_sc_Customer/', views.awp_sc_Customer, name='awp_sc_Customer'),
    path('awp_sc_Finance/', views.awp_sc_Finance, name='awp_sc_Finance'),
    path('awp_sc_InternalBusinessProcesses/', views.awp_sc_InternalBusinessProcesses, name='awp_sc_InternalBusinessProcesses'),
    path('awp_sc_OrganizationalCapacity', views.awp_sc_OrganizationalCapacity, name='awp_sc_OrganizationalCapacity'),

    path('awp_wp_Customer/', views.awp_wp_Customer, name='awp_wp_Customer'),
    path('awp_wp_Finance/', views.awp_wp_Finance, name='awp_wp_Finance'),
    path('awp_wp_InternalBusinessProcesses/', views.awp_wp_InternalBusinessProcesses, name='awp_wp_InternalBusinessProcesses'),
    path('awp_wp_OrganizationalCapacity/', views.awp_wp_OrganizationalCapacity, name='awp_wp_OrganizationalCapacity'),

    path('par/', views.par, name='par'),
    path('par_sc_Customer/', views.par_sc_Customer, name='par_sc_Customer'),
    path('par_sc_Finance/', views.par_sc_Finance, name='par_sc_Finance'),
    path('par_sc_InternalBusinessProcesses/', views.par_sc_InternalBusinessProcesses, name='par_sc_InternalBusinessProcesses'),
    path('par_sc_OrganizationalCapacity/', views.par_sc_OrganizationalCapacity, name='par_sc_OrganizationalCapacity'),

    path('par_wp_Customer/', views.par_wp_Customer, name='par_wp_Customer'),
    path('par_wp_Finance/', views.par_wp_Finance, name='par_wp_Finance'),
    path('par_wp_InternalBusinessProcesses/', views.par_wp_InternalBusinessProcesses, name='par_wp_InternalBusinessProcesses'),
    path('par_wp_OrganizationalCapacity/', views.par_wp_OrganizationalCapacity, name='par_wp_OrganizationalCapacity'),

    path('my_par/', views.my_par, name='my_par'),
    path('my_par_customer/', views.my_par_customer, name='my_par_customer'),
    path('my_par_finance/', views.my_par_finance, name='my_par_finance'),
    path('my_par_internal_business_processes/', views.my_par_internal_business_processes, name='my_par_internal_business_processes'),
    path('my_par_organizational_capacity/', views.my_par_organizational_capacity, name='my_par_organizational_capacity'),

    # path('test_registration/', views.test_registration, name='test_registration'),

    # Departments AWP and Departments PAR
    path('departments_awp/', views.departments_awp, name='departments_awp'),
    path('departments_par/', views.departments_par, name='departments_par'),

    #Template - Strategy
    path('templates/', views.templates_info, name='templates' ),


    #Change password
    path('reset-password/<token>/', views.change_password, name='reset_password'),
    path('forgot-password/', views.ForgetPassword, name='forgot_password'),

    #settings
    path('settings/', views.settings_page, name='settings'),

  
    path('adminSettings/', views.adminSettings, name='adminSettings'),


]