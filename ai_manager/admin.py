from django.contrib import admin
from .models import AIProvider, APIKey

@admin.register(AIProvider)
class AIProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'provider', 'is_active', 'created_at']
    list_filter = ['provider', 'is_active']
