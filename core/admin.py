from django.contrib import admin
from .models import AIProviderSetting
@admin.register(AIProviderSetting)
class AIProviderSettingAdmin(admin.ModelAdmin):
    list_display = ('provider', 'is_active')
