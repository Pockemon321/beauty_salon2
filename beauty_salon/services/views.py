from django.shortcuts import render, get_object_or_404
from .models import Service, Master

def home(request):
    services = Service.objects.all()[:3]  # Показываем только 3 услуги на главной
    masters = Master.objects.all()[:3]    # Показываем только 3 мастера на главной
    return render(request, 'home.html', {
        'services': services,
        'masters': masters
    })

def service_list(request):
    services = Service.objects.all()
    return render(request, 'services/service_list.html', {
        'services': services
    })

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    masters = Master.objects.filter(services=service)
    return render(request, 'services/service_detail.html', {
        'service': service,
        'masters': masters
    })

def master_list(request):
    masters = Master.objects.all()
    return render(request, 'services/master_list.html', {
        'masters': masters
    })

def master_detail(request, pk):
    master = get_object_or_404(Master, pk=pk)
    return render(request, 'services/master_detail.html', {
        'master': master
    })
