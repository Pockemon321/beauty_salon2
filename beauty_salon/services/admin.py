from django.contrib import admin
from .models import Service, Master, ServiceCategory

# Register your models here.

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_popular')
    list_filter = ('category', 'is_popular')
    search_fields = ('name', 'description')
    list_editable = ('price', 'duration', 'is_popular')

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience')
    filter_horizontal = ('services', 'specialization')
    search_fields = ('name', 'description')
