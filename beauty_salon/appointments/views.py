from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import Appointment, Service, Master
from .forms import AppointmentForm, ServiceForm, MasterForm
from users.models import User, Client
from django.db import models

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.status = 'pending'  # Устанавливаем статус "в ожидании"
            
            # Проверка на прошедшую дату
            appointment_datetime = timezone.make_aware(
                timezone.datetime.combine(form.cleaned_data['date'], form.cleaned_data['time'])
            )
            if appointment_datetime < timezone.now():
                form.add_error('date', 'Нельзя создать запись на прошедшее время')
                form.add_error('time', 'Нельзя создать запись на прошедшее время')
            else:
                appointment.save()
                messages.success(request, 'Запись успешно создана!')
                return redirect('appointment_list')
    else:
        initial_data = {}
        if 'service' in request.GET:
            service_id = request.GET.get('service')
            initial_data['service'] = service_id
            # Если выбрана услуга, ограничиваем выбор мастеров
            form = AppointmentForm(initial=initial_data)
            form.fields['master'].queryset = Master.objects.filter(services=service_id)
        else:
            form = AppointmentForm()

    context = {
        'form': form,
        'services': Service.objects.all(),
    }
    return render(request, 'appointments/appointment_form.html', context)

@login_required
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    
    # Проверяем, можно ли редактировать запись
    if appointment.status not in ['pending', 'confirmed']:
        messages.error(request, 'Нельзя редактировать завершенную или отмененную запись!')
        return redirect('appointment_detail', pk=appointment.pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись успешно обновлена!')
            return redirect('appointment_detail', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
        # Ограничиваем выбор мастеров теми, кто оказывает выбранную услугу
        form.fields['master'].queryset = Master.objects.filter(services=appointment.service)

    context = {
        'form': form,
        'appointment': appointment
    }
    return render(request, 'appointments/appointment_edit.html', context)

@login_required
def get_masters_for_service(request):
    service_id = request.GET.get('service_id')
    if service_id:
        masters = Master.objects.filter(services__id=service_id)
        masters_data = [{'id': master.id, 'name': master.name} for master in masters]
        return JsonResponse({'masters': masters_data})
    return JsonResponse({'masters': []})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(client=request.user).order_by('-date', '-time')
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments
    })

@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment
    })

@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, client=request.user)
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Запись успешно отменена!')
        return redirect('appointment_list')
    
    return render(request, 'appointments/appointment_cancel.html', {
        'appointment': appointment
    })

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Получаем статистику
    total_appointments = Appointment.objects.count()
    total_masters = Master.objects.count()
    total_services = Service.objects.count()
    total_clients = Client.objects.count()
    
    # Получаем последние 5 записей
    recent_appointments = Appointment.objects.select_related('client', 'service', 'master').order_by('-created_at')[:5]
    
    context = {
        'total_appointments': total_appointments,
        'total_masters': total_masters,
        'total_services': total_services,
        'total_clients': total_clients,
        'recent_appointments': recent_appointments,
    }
    
    return render(request, 'appointments/admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_masters_list(request):
    masters = Master.objects.all().order_by('name')
    paginator = Paginator(masters, 10)
    page = request.GET.get('page')
    masters = paginator.get_page(page)
    return render(request, 'appointments/admin/masters_list.html', {'masters': masters})

@login_required
@user_passes_test(is_admin)
def admin_master_create(request):
    if request.method == 'POST':
        form = MasterForm(request.POST, request.FILES)
        if form.is_valid():
            master = form.save(commit=False)
            # Создаем пользователя для мастера
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=User.objects.make_random_password(),
                is_staff=True  # Даем мастеру доступ к админ-панели
            )
            master.user = user
            master.save()
            form.save_m2m()  # Сохраняем many-to-many поля
            messages.success(request, 'Мастер успешно добавлен')
            return redirect('admin_masters_list')
    else:
        form = MasterForm()
    return render(request, 'appointments/admin/master_form.html', {'form': form, 'title': 'Добавление мастера'})

@login_required
@user_passes_test(is_admin)
def admin_master_edit(request, pk):
    master = get_object_or_404(Master, pk=pk)
    if request.method == 'POST':
        form = MasterForm(request.POST, request.FILES, instance=master)
        if form.is_valid():
            master = form.save()
            messages.success(request, 'Данные мастера обновлены')
            return redirect('admin_masters_list')
    else:
        form = MasterForm(instance=master)
    return render(request, 'appointments/admin/master_form.html', {'form': form, 'title': 'Редактирование мастера'})

@login_required
@user_passes_test(is_admin)
def admin_master_delete(request, pk):
    master = get_object_or_404(Master, pk=pk)
    if request.method == 'POST':
        if master.user:
            master.user.delete()  # Удаляем связанного пользователя
        master.delete()
        messages.success(request, 'Мастер успешно удален')
        return redirect('admin_masters_list')
    return render(request, 'appointments/admin/master_delete.html', {'master': master})

@login_required
@user_passes_test(is_admin)
def admin_services_list(request):
    services = Service.objects.all().order_by('name')
    paginator = Paginator(services, 10)
    page = request.GET.get('page')
    services = paginator.get_page(page)
    return render(request, 'appointments/admin/services_list.html', {'services': services})

@login_required
@user_passes_test(is_admin)
def admin_service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Услуга успешно добавлена')
            return redirect('admin_services_list')
    else:
        form = ServiceForm()
    return render(request, 'appointments/admin/service_form.html', {'form': form, 'title': 'Добавление услуги'})

@login_required
@user_passes_test(is_admin)
def admin_service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            service = form.save()
            messages.success(request, 'Услуга успешно обновлена')
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
        messages.success(request, 'Услуга успешно удалена')
        return redirect('admin_services_list')
    return render(request, 'appointments/admin/service_delete.html', {'service': service})

@login_required
@user_passes_test(is_admin)
def admin_appointments(request):
    # Получаем параметры фильтрации
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    master = request.GET.get('master')
    search = request.GET.get('search')

    # Базовый QuerySet
    appointments = Appointment.objects.select_related('client', 'service', 'master').order_by('-date', '-time')

    # Применяем фильтры
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
            models.Q(client__first_name__icontains=search) |
            models.Q(client__last_name__icontains=search) |
            models.Q(service__name__icontains=search)
        )

    # Пагинация
    paginator = Paginator(appointments, 10)
    page = request.GET.get('page')
    appointments = paginator.get_page(page)

    # Получаем список мастеров для фильтра
    masters = Master.objects.filter(is_active=True)

    context = {
        'appointments': appointments,
        'masters': masters,
        'current_status': status,
        'current_date_from': date_from,
        'current_date_to': date_to,
        'current_master': master,
        'current_search': search,
    }

    return render(request, 'appointments/admin/appointments.html', context)

@login_required
@user_passes_test(is_admin)
def admin_appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Appointment.STATUS_CHOICES):
            appointment.status = status
            appointment.save()
            messages.success(request, 'Статус записи успешно обновлен!')
            return redirect('admin_appointments')
    
    context = {
        'appointment': appointment,
        'statuses': Appointment.STATUS_CHOICES,
    }
    return render(request, 'appointments/admin/appointment_edit.html', context)

def about(request):
    """Страница 'О нас'"""
    return render(request, 'about.html')
