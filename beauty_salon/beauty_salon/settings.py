INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'services',
    'appointments',
    'django_extensions',
]

# Настройки аутентификации
LOGIN_REDIRECT_URL = '/'  # Перенаправление на главную страницу после входа
LOGIN_URL = 'login'  # URL для страницы входа
LOGOUT_REDIRECT_URL = '/'  # Перенаправление на главную страницу после выхода 