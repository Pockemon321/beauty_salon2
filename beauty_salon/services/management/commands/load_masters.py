from django.core.management.base import BaseCommand
from services.models import Master, ServiceCategory, Service

class Command(BaseCommand):
    help = 'Загружает мастеров в базу данных'

    def handle(self, *args, **kwargs):
        # Получаем все категории
        categories = {
            'hair': ServiceCategory.objects.get(name='Парикмахерские услуги'),
            'nails': ServiceCategory.objects.get(name='Ногтевой сервис'),
            'face': ServiceCategory.objects.get(name='Уход за лицом'),
            'massage': ServiceCategory.objects.get(name='Массаж'),
            'makeup': ServiceCategory.objects.get(name='Макияж')
        }

        # Получаем все услуги
        services = {
            'hair': Service.objects.filter(category=categories['hair']),
            'nails': Service.objects.filter(category=categories['nails']),
            'face': Service.objects.filter(category=categories['face']),
            'massage': Service.objects.filter(category=categories['massage']),
            'makeup': Service.objects.filter(category=categories['makeup'])
        }

        # Создаем мастеров
        masters_data = [
            {
                'name': 'Анна Петрова',
                'description': 'Опытный мастер-парикмахер с 8-летним стажем. Специализируется на современных стрижках и окрашивании.',
                'experience': 8,
                'categories': ['hair'],
                'services': services['hair']
            },
            {
                'name': 'Мария Иванова',
                'description': 'Профессиональный мастер маникюра и педикюра. Создает уникальный дизайн ногтей.',
                'experience': 5,
                'categories': ['nails'],
                'services': services['nails']
            },
            {
                'name': 'Елена Смирнова',
                'description': 'Косметолог с медицинским образованием. Специализируется на уходе за лицом и пилингах.',
                'experience': 6,
                'categories': ['face'],
                'services': services['face']
            },
            {
                'name': 'Александр Козлов',
                'description': 'Мастер массажа с 10-летним опытом. Специализируется на классическом и лечебном массаже.',
                'experience': 10,
                'categories': ['massage'],
                'services': services['massage']
            },
            {
                'name': 'Ольга Новикова',
                'description': 'Профессиональный визажист. Создает как повседневный, так и праздничный макияж.',
                'experience': 7,
                'categories': ['makeup'],
                'services': services['makeup']
            },
            {
                'name': 'Ирина Соколова',
                'description': 'Универсальный мастер с опытом в парикмахерском искусстве и макияже.',
                'experience': 9,
                'categories': ['hair', 'makeup'],
                'services': list(services['hair']) + list(services['makeup'])
            },
            {
                'name': 'Татьяна Морозова',
                'description': 'Мастер по уходу за лицом и массажу. Создает комплексные программы ухода.',
                'experience': 6,
                'categories': ['face', 'massage'],
                'services': list(services['face']) + list(services['massage'])
            },
            {
                'name': 'Наталья Волкова',
                'description': 'Мастер маникюра и педикюра с дополнительной специализацией в косметологии.',
                'experience': 5,
                'categories': ['nails', 'face'],
                'services': list(services['nails']) + list(services['face'])
            }
        ]

        for master_data in masters_data:
            master, created = Master.objects.get_or_create(
                name=master_data['name'],
                defaults={
                    'description': master_data['description'],
                    'experience': master_data['experience']
                }
            )
            
            if created:
                # Добавляем специализации
                for category_key in master_data['categories']:
                    master.specialization.add(categories[category_key])
                
                # Добавляем услуги
                for service in master_data['services']:
                    master.services.add(service)
                
                self.stdout.write(f'Создан мастер: {master.name}')
            else:
                self.stdout.write(f'Мастер уже существует: {master.name}') 