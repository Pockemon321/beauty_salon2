from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$',
        message="Номер телефона должен быть в формате: '+7 (999) 999-99-99'"
    )
    phone = models.CharField(validators=[phone_regex], max_length=19, blank=True)
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_staff = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client', verbose_name="Пользователь")
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        
    def __str__(self):
        return f"Клиент: {self.user.get_full_name() or self.user.username}"
