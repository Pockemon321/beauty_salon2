from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Создание администратора'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Администратор',
                last_name='Салона',
                phone='+79990000000'
            )
            self.stdout.write(self.style.SUCCESS('Администратор успешно создан'))
        else:
            self.stdout.write('Администратор уже существует') 