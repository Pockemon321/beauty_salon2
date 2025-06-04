from django.db import models
from django.conf import settings
from services.models import Service, Master

# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Клиент')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name='Мастер')
    date = models.DateField('Дата')
    time = models.TimeField('Время')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    notes = models.TextField('Дополнительные пожелания', blank=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date', '-time']

    def __str__(self):
        return f'Запись клиента {self.client} к мастеру {self.master} на {self.date} {self.time}'
