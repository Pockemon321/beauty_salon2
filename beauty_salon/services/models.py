from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# Create your models here.

class ServiceCategory(models.Model):
    name = models.CharField('Название категории', max_length=100)
    description = models.TextField('Описание категории', blank=True)
    icon = models.CharField('Иконка', max_length=50, blank=True, help_text='Название иконки из Font Awesome')

    class Meta:
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'
        ordering = ['name']

    def __str__(self):
        return self.name

class Specialization(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField('Название услуги', max_length=100)
    description = models.TextField('Описание')
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.IntegerField('Длительность (минут)', validators=[MinValueValidator(1)])
    image = models.ImageField('Изображение', upload_to='services/', null=True, blank=True)
    is_popular = models.BooleanField('Популярная услуга', default=False)
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Master(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    name = models.CharField('ФИО мастера', max_length=100)
    services = models.ManyToManyField(Service, verbose_name='Услуги')
    photo = models.ImageField('Фото', upload_to='masters/', null=True, blank=True)
    description = models.TextField('О мастере', blank=True)
    experience = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        verbose_name="Опыт работы (лет)"
    )
    specialization = models.ManyToManyField(Specialization, verbose_name='Специализация')
    is_active = models.BooleanField('Активен', default=True)
    schedule_start = models.TimeField('Начало рабочего дня', default='09:00')
    schedule_end = models.TimeField('Конец рабочего дня', default='18:00')

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.user and not self.name:
            self.name = self.user.get_full_name() or self.user.username
        super().save(*args, **kwargs)
