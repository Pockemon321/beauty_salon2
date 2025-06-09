from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Сброс пароля администратора'

    def handle(self, *args, **kwargs):
        try:
            admin = User.objects.get(username='admin')
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Пароль администратора успешно сброшен'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Пользователь admin не найден')) 