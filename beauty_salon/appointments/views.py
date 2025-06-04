from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from services.models import Service, Master
from django.utils import timezone
from django.http import JsonResponse

@login_required
def appointment_create(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')
        master_id = request.POST.get('master')
        date = request.POST.get('date')
        time = request.POST.get('time')
        notes = request.POST.get('notes', '')

        service = get_object_or_404(Service, pk=service_id)
        master = get_object_or_404(Master, pk=master_id)

        appointment = Appointment.objects.create(
            client=request.user,
            service=service,
            master=master,
            date=date,
            time=time,
            notes=notes
        )
        messages.success(request, 'Запись успешно создана!')
        return redirect('appointment_detail', pk=appointment.pk)

    service_id = request.GET.get('service')
    master_id = request.GET.get('master')
    services = Service.objects.all()
    masters = Master.objects.all()

    if service_id:
        service = get_object_or_404(Service, pk=service_id)
        masters = masters.filter(services=service)

    context = {
        'services': services,
        'masters': masters,
        'selected_service': service_id,
        'selected_master': master_id,
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
        service_id = request.POST.get('service')
        master_id = request.POST.get('master')
        date = request.POST.get('date')
        time = request.POST.get('time')
        notes = request.POST.get('notes', '')

        service = get_object_or_404(Service, pk=service_id)
        master = get_object_or_404(Master, pk=master_id)

        appointment.service = service
        appointment.master = master
        appointment.date = date
        appointment.time = time
        appointment.notes = notes
        appointment.save()

        messages.success(request, 'Запись успешно обновлена!')
        return redirect('appointment_detail', pk=appointment.pk)

    services = Service.objects.all()
    masters = Master.objects.filter(services=appointment.service)

    context = {
        'appointment': appointment,
        'services': services,
        'masters': masters,
        'selected_service': appointment.service.id,
        'selected_master': appointment.master.id,
    }
    return render(request, 'appointments/appointment_edit.html', context)

@login_required
def get_masters_for_service(request):
    service_id = request.GET.get('service_id')
    masters = Master.objects.filter(services__id=service_id)
    masters_data = [{'id': master.id, 'name': master.name} for master in masters]
    return JsonResponse({'masters': masters_data})

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
