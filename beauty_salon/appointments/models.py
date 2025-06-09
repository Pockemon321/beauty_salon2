from django.db import models
from django.conf import settings
from services.models import Service, Master
from django.utils import timezone
from users.models import User

# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client} - {self.service} ({self.date} {self.time})"

    class Meta:
        ordering = ['-date', '-time']
        
    def clean(self):
        from django.core.exceptions import ValidationError
        # Проверяем, что дата не в прошлом
        if self.date < timezone.now().date():
            raise ValidationError('Дата записи не может быть в прошлом')
        
        # Проверяем, что мастер может оказывать выбранную услугу
        if self.master and self.service and not self.master.services.filter(id=self.service.id).exists():
            raise ValidationError('Выбранный мастер не оказывает данную услугу')
        
        # Проверяем, нет ли пересечений с другими записями
        overlapping = Appointment.objects.filter(
            master=self.master,
            date=self.date,
            status__in=['pending', 'confirmed']
        ).exclude(id=self.id)
        
        # Получаем время окончания текущей записи
        end_time = (
            timezone.datetime.combine(timezone.now().date(), self.time) + 
            timezone.timedelta(minutes=self.service.duration)
        ).time()
        
        for app in overlapping:
            app_end_time = (
                timezone.datetime.combine(timezone.now().date(), app.time) + 
                timezone.timedelta(minutes=app.service.duration)
            ).time()
            
            if (self.time <= app.time < end_time) or (app.time <= self.time < app_end_time):
                raise ValidationError('У мастера уже есть запись на это время')
