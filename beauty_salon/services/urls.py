from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.service_list, name='services'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('masters/', views.master_list, name='masters'),
    path('masters/<int:pk>/', views.master_detail, name='master_detail'),
]
