from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from services.models import Service, Master
from users.models import User
from .forms import AppointmentForm, MasterForm, ServiceForm

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)

    context = {
        # Статистика записей
        'total_appointments': Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'today_appointments': Appointment.objects.filter(date=today).count(),
        'tomorrow_appointments': Appointment.objects.filter(date=tomorrow).count(),
        
        # Статистика мастеров
        'total_masters': Master.objects.count(),
        'active_masters': Master.objects.filter(is_active=True).count(),
        
        # Статистика услуг
        'total_services': Service.objects.count(),
        'active_services': Service.objects.filter(is_active=True).count(),
        
        # График работы на сегодня
        'today_schedule': Appointment.objects.filter(
            date=today
        ).select_related('client', 'service', 'master').order_by('time')
    }
    
    return render(request, 'appointments/admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_appointment_list(request):
    # Фильтрация
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    master = request.GET.get('master')
    search = request.GET.get('search')

    appointments = Appointment.objects.all()

    if status:
        appointments = appointments.filter(status=status)
    if date_from:
        appointments = appointments.filter(date__gte=date_from)
    if date_to:
        appointments = appointments.filter(date__lte=date_to)
    if master:
        appointments = appointments.filter(master_id=master)
    if search:
        appointments = appointments.filter(
            Q(client__first_name__icontains=search) |
            Q(client__last_name__icontains=search) |
            Q(service__name__icontains=search)
        )

    appointments = appointments.order_by('-date', '-time')

    context = {
        'appointments': appointments,
        'masters': Master.objects.all(),
        'statuses': Appointment.STATUS_CHOICES,
    }
    return render(request, 'appointments/admin/appointment_list.html', context)

@login_required
@user_passes_test(is_admin)
def admin_appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена')
            return redirect('admin_appointments')
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'appointments/admin/appointment_form.html', {
        'form': form,
        'appointment': appointment
    })

@login_required
@user_passes_test(is_admin)
def admin_appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Запись успешно удалена')
        return redirect('admin_appointments')
    
    return render(request, 'appointments/admin/appointment_delete.html', {
        'appointment': appointment
    })

@login_required
@user_passes_test(is_admin)
def admin_masters_list(request):
    masters = Master.objects.all()
    return render(request, 'appointments/admin/masters_list.html', {'masters': masters})

@login_required
@user_passes_test(is_admin)
def admin_master_create(request):
    if request.method == 'POST':
        form = MasterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_masters_list')
    else:
        form = MasterForm()
    return render(request, 'appointments/admin/master_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_master_edit(request, pk):
    master = get_object_or_404(Master, pk=pk)
    if request.method == 'POST':
        form = MasterForm(request.POST, instance=master)
        if form.is_valid():
            form.save()
            return redirect('admin_masters_list')
    else:
        form = MasterForm(instance=master)
    return render(request, 'appointments/admin/master_form.html', {'form': form, 'master': master})

@login_required
@user_passes_test(is_admin)
def admin_master_delete(request, pk):
    master = get_object_or_404(Master, pk=pk)
    if request.method == 'POST':
        master.delete()
        return redirect('admin_masters_list')
    return render(request, 'appointments/admin/master_delete.html', {'master': master})

@login_required
@user_passes_test(is_admin)
def admin_services_list(request):
    services = Service.objects.all()
    return render(request, 'appointments/admin/services_list.html', {'services': services})

@login_required
@user_passes_test(is_admin)
def admin_service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_services_list')
    else:
        form = ServiceForm()
    return render(request, 'appointments/admin/service_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def admin_service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('admin_services_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'appointments/admin/service_form.html', {'form': form, 'service': service})

@login_required
@user_passes_test(is_admin)
def admin_service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('admin_services_list')
    return render(request, 'appointments/admin/service_delete.html', {'service': service}) 