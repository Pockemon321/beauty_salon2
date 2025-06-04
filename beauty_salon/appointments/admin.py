from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Appointment

# Register your models here.

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_link', 'service_link', 'master_link', 'date', 'time', 'status_badge', 'created_at')
    list_filter = ('status', 'date', 'master', 'service')
    search_fields = ('client__username', 'client__first_name', 'client__last_name', 'master__name', 'service__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('client', 'service', 'master', 'status')
        }),
        ('Время записи', {
            'fields': ('date', 'time')
        }),
        ('Дополнительно', {
            'fields': ('notes', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def client_link(self, obj):
        url = reverse('admin:users_user_change', args=[obj.client.id])
        return format_html('<a href="{}">{}</a>', url, obj.client.get_full_name() or obj.client.username)
    client_link.short_description = 'Клиент'

    def service_link(self, obj):
        url = reverse('admin:services_service_change', args=[obj.service.id])
        return format_html('<a href="{}">{}</a>', url, obj.service.name)
    service_link.short_description = 'Услуга'

    def master_link(self, obj):
        url = reverse('admin:services_master_change', args=[obj.master.id])
        return format_html('<a href="{}">{}</a>', url, obj.master.name)
    master_link.short_description = 'Мастер'

    def status_badge(self, obj):
        status_colors = {
            'pending': 'warning',
            'confirmed': 'info',
            'completed': 'success',
            'cancelled': 'danger'
        }
        color = status_colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Статус'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Если пользователь не суперпользователь, показываем только записи на сегодня и будущие
        if not request.user.is_superuser:
            from django.utils import timezone
            today = timezone.now().date()
            return qs.filter(date__gte=today)
        return qs

    def has_delete_permission(self, request, obj=None):
        # Только суперпользователь может удалять записи
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        # Суперпользователь может менять любые записи
        if request.user.is_superuser:
            return True
        # Обычный админ может менять только записи на сегодня и будущие
        from django.utils import timezone
        today = timezone.now().date()
        return obj.date >= today

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
