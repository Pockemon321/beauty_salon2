from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Client

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'phone'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('username',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_phone', 'get_email')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__phone')
    
    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = 'Телефон'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
