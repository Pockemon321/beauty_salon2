from django.core.management.base import BaseCommand
from services.models import ServiceCategory, Service

class Command(BaseCommand):
    help = 'Загружает категории и услуги в базу данных'

    def handle(self, *args, **kwargs):
        # Создаем категории
        categories = {
            'hair': {
                'name': 'Парикмахерские услуги',
                'description': 'Стрижки, окрашивание, укладки и другие услуги для волос',
                'icon': 'cut'
            },
            'nails': {
                'name': 'Ногтевой сервис',
                'description': 'Маникюр, педикюр, наращивание ногтей',
                'icon': 'hand-sparkles'
            },
            'face': {
                'name': 'Уход за лицом',
                'description': 'Чистка лица, пилинги, маски и другие процедуры',
                'icon': 'spa'
            },
            'massage': {
                'name': 'Массаж',
                'description': 'Различные виды массажа для тела',
                'icon': 'hands'
            },
            'makeup': {
                'name': 'Макияж',
                'description': 'Повседневный, вечерний и свадебный макияж',
                'icon': 'paint-brush'
            }
        }

        created_categories = {}
        for key, data in categories.items():
            category, created = ServiceCategory.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'icon': data['icon']
                }
            )
            created_categories[key] = category
            if created:
                self.stdout.write(f'Создана категория: {category.name}')

        # Создаем услуги
        services = {
            'hair': [
                {
                    'name': 'Женская стрижка',
                    'description': 'Стрижка с учетом формы лица и типа волос',
                    'price': 2000,
                    'duration': 60,
                    'is_popular': True
                },
                {
                    'name': 'Мужская стрижка',
                    'description': 'Классическая или современная стрижка',
                    'price': 1500,
                    'duration': 45,
                    'is_popular': True
                },
                {
                    'name': 'Окрашивание волос',
                    'description': 'Окрашивание в один тон или сложное окрашивание',
                    'price': 3500,
                    'duration': 120,
                    'is_popular': True
                },
                {
                    'name': 'Укладка',
                    'description': 'Повседневная или праздничная укладка',
                    'price': 2000,
                    'duration': 60,
                    'is_popular': False
                }
            ],
            'nails': [
                {
                    'name': 'Маникюр',
                    'description': 'Классический или аппаратный маникюр',
                    'price': 1500,
                    'duration': 60,
                    'is_popular': True
                },
                {
                    'name': 'Педикюр',
                    'description': 'Классический или аппаратный педикюр',
                    'price': 2000,
                    'duration': 90,
                    'is_popular': True
                },
                {
                    'name': 'Наращивание ногтей',
                    'description': 'Наращивание гелем или акрилом',
                    'price': 4000,
                    'duration': 120,
                    'is_popular': False
                }
            ],
            'face': [
                {
                    'name': 'Чистка лица',
                    'description': 'Глубокая чистка пор и удаление черных точек',
                    'price': 3000,
                    'duration': 90,
                    'is_popular': True
                },
                {
                    'name': 'Пилинг',
                    'description': 'Химический или механический пилинг',
                    'price': 2500,
                    'duration': 60,
                    'is_popular': False
                },
                {
                    'name': 'Маска для лица',
                    'description': 'Увлажняющая или очищающая маска',
                    'price': 2000,
                    'duration': 30,
                    'is_popular': False
                }
            ],
            'massage': [
                {
                    'name': 'Классический массаж',
                    'description': 'Общий массаж всего тела',
                    'price': 3000,
                    'duration': 60,
                    'is_popular': True
                },
                {
                    'name': 'Антицеллюлитный массаж',
                    'description': 'Массаж проблемных зон',
                    'price': 3500,
                    'duration': 90,
                    'is_popular': False
                }
            ],
            'makeup': [
                {
                    'name': 'Повседневный макияж',
                    'description': 'Естественный макияж для ежедневного использования',
                    'price': 2000,
                    'duration': 45,
                    'is_popular': True
                },
                {
                    'name': 'Вечерний макияж',
                    'description': 'Яркий макияж для особых случаев',
                    'price': 3000,
                    'duration': 60,
                    'is_popular': True
                },
                {
                    'name': 'Свадебный макияж',
                    'description': 'Макияж невесты с предварительной консультацией',
                    'price': 5000,
                    'duration': 90,
                    'is_popular': False
                }
            ]
        }

        for category_key, category_services in services.items():
            category = created_categories[category_key]
            for service_data in category_services:
                service, created = Service.objects.get_or_create(
                    category=category,
                    name=service_data['name'],
                    defaults={
                        'description': service_data['description'],
                        'price': service_data['price'],
                        'duration': service_data['duration'],
                        'is_popular': service_data['is_popular']
                    }
                )
                if created:
                    self.stdout.write(f'Создана услуга: {service.name} в категории {category.name}') 