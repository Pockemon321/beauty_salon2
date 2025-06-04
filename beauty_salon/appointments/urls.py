from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.appointment_create, name='appointment_create'),
    path('list/', views.appointment_list, name='appointment_list'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
    path('get-masters/', views.get_masters_for_service, name='get_masters_for_service'),
]
