from django.urls import path
from . import views
from . import master_views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.service_list, name='services'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('masters/', views.master_list, name='masters'),
    path('masters/<int:pk>/', views.master_detail, name='master_detail'),
    
    # URL для мастеров
    path('master/dashboard/', master_views.master_dashboard, name='master_dashboard'),
    path('master/appointments/', master_views.master_appointments, name='master_appointments'),
    path('master/services/', master_views.master_services, name='master_services'),
    path('master/profile/', master_views.master_profile, name='master_profile'),
]
