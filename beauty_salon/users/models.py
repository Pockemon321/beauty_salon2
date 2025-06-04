from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр разрешено."
    )
    
    phone = models.CharField('Телефон', validators=[phone_regex], max_length=17, blank=True)
    is_client = models.BooleanField('Клиент', default=True)
    is_master = models.BooleanField('Мастер', default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name() or self.username
