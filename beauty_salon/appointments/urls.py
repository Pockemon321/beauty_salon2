from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('create/', views.appointment_create, name='appointment_create'),
    path('list/', views.appointment_list, name='appointment_list'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
    path('get-masters/', views.get_masters_for_service, name='get_masters_for_service'),
    
    # Административные URL
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/appointments/', views.admin_appointments, name='admin_appointments'),
    path('admin/appointments/<int:pk>/edit/', views.admin_appointment_edit, name='admin_appointment_edit'),
    path('admin/appointments/<int:pk>/delete/', admin_views.admin_appointment_delete, name='admin_appointment_delete'),
    
    # Управление мастерами
    path('admin/masters/', views.admin_masters_list, name='admin_masters_list'),
    path('admin/masters/create/', views.admin_master_create, name='admin_master_create'),
    path('admin/masters/<int:pk>/edit/', views.admin_master_edit, name='admin_master_edit'),
    path('admin/masters/<int:pk>/delete/', views.admin_master_delete, name='admin_master_delete'),
    
    # Управление услугами
    path('admin/services/', views.admin_services_list, name='admin_services_list'),
    path('admin/services/create/', views.admin_service_create, name='admin_service_create'),
    path('admin/services/<int:pk>/edit/', views.admin_service_edit, name='admin_service_edit'),
    path('admin/services/<int:pk>/delete/', views.admin_service_delete, name='admin_service_delete'),
]
