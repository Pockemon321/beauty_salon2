from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from services.models import Specialization, Service, Master, ServiceCategory
from users.models import Client
from datetime import time
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Загрузка начальных данных'

    def handle(self, *args, **kwargs):
        self.stdout.write('Загрузка начальных данных...')

        # Создаем категории услуг
        categories_data = [
            {
                'name': 'Парикмахерские услуги',
                'description': 'Стрижки, окрашивание, укладки',
            },
            {
                'name': 'Ногтевой сервис',
                'description': 'Маникюр, педикюр, наращивание ногтей',
            },
            {
                'name': 'Уход за лицом',
                'description': 'Чистка лица, массаж, уходовые процедуры',
            },
            {
                'name': 'Ресницы и брови',
                'description': 'Наращивание ресниц, оформление бровей',
            },
        ]

        categories = {}
        for category_data in categories_data:
            category, created = ServiceCategory.objects.get_or_create(**category_data)
            categories[category.name] = category
            action = 'создана' if created else 'уже существует'
            self.stdout.write(f'Категория услуг "{category.name}" {action}')

        # Создаем специализации
        specializations_data = [
            {'name': 'Парикмахер', 'description': 'Стрижки, окрашивание, укладки'},
            {'name': 'Визажист', 'description': 'Макияж, оформление бровей'},
            {'name': 'Мастер маникюра', 'description': 'Маникюр, педикюр, наращивание ногтей'},
            {'name': 'Косметолог', 'description': 'Уход за кожей, чистка лица, массаж'},
            {'name': 'Мастер по наращиванию ресниц', 'description': 'Наращивание и ламинирование ресниц'},
        ]

        specializations = []
        for spec_data in specializations_data:
            spec, created = Specialization.objects.get_or_create(**spec_data)
            specializations.append(spec)
            action = 'создана' if created else 'уже существует'
            self.stdout.write(f'Специализация "{spec.name}" {action}')

        # Создаем услуги
        services_data = [
            {
                'name': 'Женская стрижка',
                'description': 'Стрижка любой сложности',
                'price': Decimal('2000.00'),
                'duration': 60,
                'category': categories['Парикмахерские услуги'],
            },
            {
                'name': 'Окрашивание волос',
                'description': 'Окрашивание в один тон',
                'price': Decimal('4000.00'),
                'duration': 120,
                'category': categories['Парикмахерские услуги'],
            },
            {
                'name': 'Маникюр',
                'description': 'Классический маникюр с покрытием',
                'price': Decimal('2500.00'),
                'duration': 90,
                'category': categories['Ногтевой сервис'],
            },
            {
                'name': 'Педикюр',
                'description': 'Классический педикюр с покрытием',
                'price': Decimal('3000.00'),
                'duration': 90,
                'category': categories['Ногтевой сервис'],
            },
            {
                'name': 'Наращивание ресниц',
                'description': '2D эффект',
                'price': Decimal('3500.00'),
                'duration': 120,
                'category': categories['Ресницы и брови'],
            },
            {
                'name': 'Чистка лица',
                'description': 'Комбинированная чистка',
                'price': Decimal('4000.00'),
                'duration': 90,
                'category': categories['Уход за лицом'],
            },
        ]

        services = []
        for service_data in services_data:
            service, created = Service.objects.get_or_create(**service_data)
            services.append(service)
            action = 'создана' if created else 'уже существует'
            self.stdout.write(f'Услуга "{service.name}" {action}')

        # Создаем мастеров
        masters_data = [
            {
                'name': 'Анна Иванова',
                'experience': 5,
                'schedule_start': time(9, 0),
                'schedule_end': time(18, 0),
                'specializations': ['Парикмахер'],
                'services': ['Женская стрижка', 'Окрашивание волос'],
            },
            {
                'name': 'Мария Петрова',
                'experience': 3,
                'schedule_start': time(10, 0),
                'schedule_end': time(19, 0),
                'specializations': ['Мастер маникюра'],
                'services': ['Маникюр', 'Педикюр'],
            },
            {
                'name': 'Елена Сидорова',
                'experience': 7,
                'schedule_start': time(9, 0),
                'schedule_end': time(20, 0),
                'specializations': ['Косметолог'],
                'services': ['Чистка лица'],
            },
            {
                'name': 'Ольга Козлова',
                'experience': 4,
                'schedule_start': time(10, 0),
                'schedule_end': time(19, 0),
                'specializations': ['Мастер по наращиванию ресниц'],
                'services': ['Наращивание ресниц'],
            },
        ]

        for master_data in masters_data:
            specializations = master_data.pop('specializations')
            services_names = master_data.pop('services')
            
            master, created = Master.objects.get_or_create(**master_data)
            
            # Добавляем специализации
            for spec_name in specializations:
                spec = Specialization.objects.get(name=spec_name)
                master.specialization.add(spec)
            
            # Добавляем услуги
            for service_name in services_names:
                service = Service.objects.get(name=service_name)
                master.services.add(service)
            
            action = 'создан' if created else 'уже существует'
            self.stdout.write(f'Мастер "{master.name}" {action}')

        # Создаем клиентов
        clients_data = [
            {
                'username': 'client1',
                'password': 'testpass123',
                'email': 'client1@example.com',
                'first_name': 'Екатерина',
                'last_name': 'Смирнова',
                'phone': '+79991112233',
            },
            {
                'username': 'client2',
                'password': 'testpass123',
                'email': 'client2@example.com',
                'first_name': 'Наталья',
                'last_name': 'Морозова',
                'phone': '+79992223344',
            },
            {
                'username': 'client3',
                'password': 'testpass123',
                'email': 'client3@example.com',
                'first_name': 'Татьяна',
                'last_name': 'Волкова',
                'phone': '+79993334455',
            },
        ]

        for client_data in clients_data:
            username = client_data['username']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password=client_data['password'],
                    email=client_data['email'],
                    first_name=client_data['first_name'],
                    last_name=client_data['last_name'],
                    phone=client_data['phone'],
                )
                
                Client.objects.create(user=user)
                self.stdout.write(f'Клиент "{username}" создан')
            else:
                self.stdout.write(f'Клиент "{username}" уже существует')

        self.stdout.write(self.style.SUCCESS('Загрузка начальных данных завершена!')) 