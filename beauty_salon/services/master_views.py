from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from appointments.models import Appointment
from services.models import Service, Master
from django.utils import timezone
from django.db.models import Q

def is_master(user):
    return user.role == 'master'

@login_required
@user_passes_test(is_master)
def master_dashboard(request):
    # Получаем мастера
    master = get_object_or_404(Master, user=request.user)
    
    # Получаем статистику
    today = timezone.now().date()
    total_appointments = Appointment.objects.filter(master=master).count()
    today_appointments = Appointment.objects.filter(master=master, date=today).count()
    pending_appointments = Appointment.objects.filter(master=master, status='pending').count()
    
    # Получаем ближайшие записи
    upcoming_appointments = Appointment.objects.filter(
        master=master,
        date__gte=today
    ).order_by('date', 'time')[:5]
    
    context = {
        'master': master,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'pending_appointments': pending_appointments,
        'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'services/master/dashboard.html', context)

@login_required
@user_passes_test(is_master)
def master_appointments(request):
    master = get_object_or_404(Master, user=request.user)
    
    # Фильтрация
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    search = request.GET.get('search')
    
    appointments = Appointment.objects.filter(master=master)
    
    if status:
        appointments = appointments.filter(status=status)
    if date_from:
        appointments = appointments.filter(date__gte=date_from)
    if date_to:
        appointments = appointments.filter(date__lte=date_to)
    if search:
        appointments = appointments.filter(
            Q(client__first_name__icontains=search) |
            Q(client__last_name__icontains=search) |
            Q(service__name__icontains=search)
        )
    
    appointments = appointments.order_by('-date', '-time')
    
    context = {
        'appointments': appointments,
        'statuses': Appointment.STATUS_CHOICES,
    }
    return render(request, 'services/master/appointments.html', context)

@login_required
@user_passes_test(is_master)
def master_services(request):
    master = get_object_or_404(Master, user=request.user)
    
    if request.method == 'POST':
        service_ids = request.POST.getlist('services')
        master.services.set(service_ids)
        messages.success(request, 'Список услуг успешно обновлен!')
        return redirect('master_services')
    
    # Получаем все услуги и отмечаем те, которые оказывает мастер
    all_services = Service.objects.all()
    master_services = master.services.all()
    
    context = {
        'master': master,
        'all_services': all_services,
        'master_services': master_services,
    }
    return render(request, 'services/master/services.html', context)

@login_required
@user_passes_test(is_master)
def master_profile(request):
    master = get_object_or_404(Master, user=request.user)
    
    if request.method == 'POST':
        # Обновляем информацию о мастере
        master.description = request.POST.get('description', '')
        master.experience = request.POST.get('experience', 0)
        
        # Обработка загруженного фото
        if 'photo' in request.FILES:
            master.photo = request.FILES['photo']
        
        master.save()
        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('master_profile')
    
    context = {
        'master': master,
    }
    return render(request, 'services/master/profile.html', context) 