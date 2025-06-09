from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Service, Master, ServiceCategory

def home(request):
    services = Service.objects.all()[:3]  # Показываем только 3 услуги на главной
    masters = Master.objects.all()[:3]    # Показываем только 3 мастера на главной
    return render(request, 'home.html', {
        'services': services,
        'masters': masters
    })

def service_list(request):
    services = Service.objects.all()
    categories = ServiceCategory.objects.all()
    
    # Поиск по названию или описанию
    search = request.GET.get('search')
    if search and search.lower() != 'none':
        services = services.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category and category.isdigit():
        services = services.filter(category_id=category)
    
    # Фильтрация по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and min_price.isdigit():
        services = services.filter(price__gte=min_price)
    if max_price and max_price.isdigit():
        services = services.filter(price__lte=max_price)
    
    # Фильтрация по длительности
    min_duration = request.GET.get('min_duration')
    max_duration = request.GET.get('max_duration')
    if min_duration and min_duration.isdigit():
        services = services.filter(duration__gte=min_duration)
    if max_duration and max_duration.isdigit():
        services = services.filter(duration__lte=max_duration)
    
    # Сортировка
    sort = request.GET.get('sort', 'name')
    if sort == 'price_asc':
        services = services.order_by('price')
    elif sort == 'price_desc':
        services = services.order_by('-price')
    elif sort == 'duration':
        services = services.order_by('duration')
    else:
        services = services.order_by('name')
    
    context = {
        'services': services,
        'categories': categories,
        'current_category': category,
        'current_sort': sort,
        'min_price': min_price,
        'max_price': max_price,
        'min_duration': min_duration,
        'max_duration': max_duration,
        'search': search
    }
    
    return render(request, 'services/service_list.html', context)

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    masters = Master.objects.filter(services=service)
    return render(request, 'services/service_detail.html', {
        'service': service,
        'masters': masters
    })

def master_list(request):
    masters = Master.objects.all()
    categories = ServiceCategory.objects.all()
    
    # Поиск по имени или описанию
    search = request.GET.get('search')
    if search and search.lower() != 'none':
        masters = masters.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Фильтрация по специализации
    specialization = request.GET.get('specialization')
    if specialization and specialization.isdigit():
        masters = masters.filter(specialization=specialization)
    
    # Фильтрация по опыту работы
    min_experience = request.GET.get('min_experience')
    max_experience = request.GET.get('max_experience')
    if min_experience and min_experience.isdigit():
        masters = masters.filter(experience__gte=min_experience)
    if max_experience and max_experience.isdigit():
        masters = masters.filter(experience__lte=max_experience)
    
    # Фильтрация по услуге
    service = request.GET.get('service')
    if service and service.isdigit():
        masters = masters.filter(services=service)
    
    # Сортировка
    sort = request.GET.get('sort', 'name')
    if sort == 'experience_asc':
        masters = masters.order_by('experience')
    elif sort == 'experience_desc':
        masters = masters.order_by('-experience')
    else:
        masters = masters.order_by('name')
    
    context = {
        'masters': masters,
        'categories': categories,
        'current_specialization': specialization,
        'current_service': service,
        'current_sort': sort,
        'min_experience': min_experience,
        'max_experience': max_experience,
        'search': search
    }
    
    return render(request, 'services/master_list.html', context)

def master_detail(request, pk):
    master = get_object_or_404(Master, pk=pk)
    return render(request, 'services/master_detail.html', {
        'master': master
    })
