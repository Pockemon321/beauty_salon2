from django.core.management.base import BaseCommand
from services.models import ServiceCategory, Service, Master, Specialization
from decimal import Decimal
from django.core.files import File
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Adds sample services and masters'

    def handle(self, *args, **kwargs):
        # Создаем категории услуг
        categories = {
            'hair': ServiceCategory.objects.create(
                name='Парикмахерские услуги',
                description='Стрижки, окрашивание, укладки и другие услуги для ваших волос',
                icon='fa-scissors'
            ),
            'nails': ServiceCategory.objects.create(
                name='Ногтевой сервис',
                description='Маникюр, педикюр, наращивание и дизайн ногтей',
                icon='fa-hand-sparkles'
            ),
            'face': ServiceCategory.objects.create(
                name='Уход за лицом',
                description='Чистка лица, массаж, маски и другие процедуры',
                icon='fa-face-smile'
            ),
            'brows': ServiceCategory.objects.create(
                name='Брови и ресницы',
                description='Оформление бровей, наращивание ресниц',
                icon='fa-eye'
            ),
            'massage': ServiceCategory.objects.create(
                name='Массаж',
                description='Различные виды массажа для вашего здоровья и красоты',
                icon='fa-spa'
            ),
            'makeup': ServiceCategory.objects.create(
                name='Макияж',
                description='Дневной, вечерний, свадебный макияж',
                icon='fa-paint-brush'
            )
        }

        # Создаем специализации
        specializations = {
            'hair': Specialization.objects.create(name='Парикмахер-стилист'),
            'colorist': Specialization.objects.create(name='Колорист'),
            'nail': Specialization.objects.create(name='Мастер маникюра'),
            'cosmetologist': Specialization.objects.create(name='Косметолог'),
            'brow': Specialization.objects.create(name='Бровист'),
            'massage': Specialization.objects.create(name='Массажист'),
            'makeup': Specialization.objects.create(name='Визажист')
        }

        # Создаем услуги
        services = []
        
        # Парикмахерские услуги
        hair_services = [
            ('Женская стрижка', 2500, 60),
            ('Мужская стрижка', 1500, 40),
            ('Окрашивание волос', 5000, 180),
            ('Мелирование', 4500, 150),
            ('Укладка волос', 2000, 40),
            ('Свадебная прическа', 5000, 120),
            ('Лечение волос', 3000, 60),
            ('Тонирование', 4000, 120)
        ]
        for name, price, duration in hair_services:
            services.append(Service.objects.create(
                category=categories['hair'],
                name=name,
                description=f'Профессиональная услуга {name.lower()}',
                price=Decimal(price),
                duration=duration,
                is_popular=True if price > 4000 else False
            ))

        # Ногтевой сервис
        nail_services = [
            ('Маникюр классический', 1500, 60),
            ('Педикюр классический', 2000, 90),
            ('Маникюр с гель-лаком', 2500, 90),
            ('Педикюр с гель-лаком', 3000, 120),
            ('Наращивание ногтей', 4000, 150),
            ('Дизайн ногтей', 500, 30),
            ('Снятие гель-лака', 500, 30),
            ('Парафинотерапия', 1000, 30)
        ]
        for name, price, duration in nail_services:
            services.append(Service.objects.create(
                category=categories['nails'],
                name=name,
                description=f'Профессиональная услуга {name.lower()}',
                price=Decimal(price),
                duration=duration,
                is_popular=True if 'гель-лак' in name.lower() else False
            ))

        # Уход за лицом
        face_services = [
            ('Чистка лица', 3500, 90),
            ('Массаж лица', 2000, 40),
            ('Пилинг', 3000, 60),
            ('Уход за кожей', 4000, 90),
            ('Маска для лица', 1500, 30),
            ('RF-лифтинг', 5000, 60),
            ('Микротоковая терапия', 3500, 45),
            ('Фотоомоложение', 6000, 60)
        ]
        for name, price, duration in face_services:
            services.append(Service.objects.create(
                category=categories['face'],
                name=name,
                description=f'Профессиональная услуга {name.lower()}',
                price=Decimal(price),
                duration=duration,
                is_popular=True if price > 4000 else False
            ))

        # Брови и ресницы
        brow_services = [
            ('Коррекция бровей', 1000, 30),
            ('Окрашивание бровей', 1200, 30),
            ('Ламинирование бровей', 2500, 60),
            ('Наращивание ресниц (классика)', 2500, 120),
            ('Наращивание ресниц (2D)', 3000, 150),
            ('Наращивание ресниц (3D)', 3500, 180),
            ('Ламинирование ресниц', 2500, 60),
            ('Снятие ресниц', 500, 30)
        ]
        for name, price, duration in brow_services:
            services.append(Service.objects.create(
                category=categories['brows'],
                name=name,
                description=f'Профессиональная услуга {name.lower()}',
                price=Decimal(price),
                duration=duration,
                is_popular='наращивание' in name.lower()
            ))

        # Массаж
        massage_services = [
            ('Классический массаж', 2500, 60),
            ('Спортивный массаж', 3000, 90),
            ('Антицеллюлитный массаж', 3000, 60),
            ('Лимфодренажный массаж', 3500, 90),
            ('Массаж шейно-воротниковой зоны', 1500, 30),
            ('Массаж спины', 2000, 45),
            ('Массаж головы', 1000, 30),
            ('Стоун-терапия', 4000, 90)
        ]
        for name, price, duration in massage_services:
            services.append(Service.objects.create(
                category=categories['massage'],
                name=name,
                description=f'Профессиональная услуга {name.lower()}',
                price=Decimal(price),
                duration=duration,
                is_popular=price > 3000
            ))

        # Макияж
        makeup_services = [
            ('Дневной макияж', 2500, 60),
            ('Вечерний макияж', 3500, 90),
            ('Свадебный макияж', 5000, 120),
            ('Макияж для фотосессии', 4000, 90),
            ('Экспресс-макияж', 1500, 30),
            ('Макияж с накладными ресницами', 3000, 90),
            ('Коррекция макияжа', 1000, 30),
            ('Обучение макияжу', 5000, 120)
        ]
        for name, price, duration in makeup_services:
            services.append(Service.objects.create(
                category=categories['makeup'],
                name=name,
                description=f'Профессиональная услуга {name.lower()}',
                price=Decimal(price),
                duration=duration,
                is_popular='свадебный' in name.lower() or 'фотосессии' in name.lower()
            ))

        # Создаем мастеров
        masters_data = [
            {
                'name': 'Анна Иванова',
                'description': 'Опытный парикмахер-стилист с международными сертификатами',
                'experience': 8,
                'specializations': ['hair', 'colorist'],
                'services_categories': ['hair']
            },
            {
                'name': 'Мария Петрова',
                'description': 'Мастер ногтевого сервиса высшей категории',
                'experience': 6,
                'specializations': ['nail'],
                'services_categories': ['nails']
            },
            {
                'name': 'Елена Сидорова',
                'description': 'Профессиональный косметолог с медицинским образованием',
                'experience': 10,
                'specializations': ['cosmetologist'],
                'services_categories': ['face']
            },
            {
                'name': 'Ольга Козлова',
                'description': 'Сертифицированный бровист и лэшмейкер',
                'experience': 5,
                'specializations': ['brow'],
                'services_categories': ['brows']
            },
            {
                'name': 'Татьяна Морозова',
                'description': 'Массажист с опытом работы в ведущих спа-салонах',
                'experience': 12,
                'specializations': ['massage'],
                'services_categories': ['massage']
            },
            {
                'name': 'Екатерина Волкова',
                'description': 'Визажист-стилист, работает с профессиональной косметикой',
                'experience': 7,
                'specializations': ['makeup'],
                'services_categories': ['makeup']
            },
            {
                'name': 'Наталья Соколова',
                'description': 'Мастер-универсал по волосам с опытом работы в Европе',
                'experience': 15,
                'specializations': ['hair', 'colorist'],
                'services_categories': ['hair']
            },
            {
                'name': 'Ирина Попова',
                'description': 'Мастер маникюра и педикюра, призер конкурсов',
                'experience': 9,
                'specializations': ['nail'],
                'services_categories': ['nails']
            },
            {
                'name': 'Светлана Новикова',
                'description': 'Косметолог-эстетист с авторскими методиками',
                'experience': 11,
                'specializations': ['cosmetologist'],
                'services_categories': ['face']
            },
            {
                'name': 'Юлия Морозова',
                'description': 'Бровист-перфекционист, создает идеальные брови',
                'experience': 6,
                'specializations': ['brow'],
                'services_categories': ['brows']
            },
            {
                'name': 'Алина Кузнецова',
                'description': 'Массажист с медицинским образованием',
                'experience': 8,
                'specializations': ['massage'],
                'services_categories': ['massage']
            },
            {
                'name': 'Дарья Лебедева',
                'description': 'Визажист с опытом работы на телевидении',
                'experience': 10,
                'specializations': ['makeup'],
                'services_categories': ['makeup']
            }
        ]

        for master_data in masters_data:
            master = Master.objects.create(
                name=master_data['name'],
                description=master_data['description'],
                experience=master_data['experience']
            )
            
            # Добавляем специализации
            for spec in master_data['specializations']:
                master.specialization.add(specializations[spec])
            
            # Добавляем услуги
            for category in master_data['services_categories']:
                category_services = Service.objects.filter(category=categories[category])
                for service in category_services:
                    master.services.add(service)

        self.stdout.write(self.style.SUCCESS('Successfully added sample data')) 