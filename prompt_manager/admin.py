from django.contrib import admin
from django.urls import path
from .models import PersonalizationProfile, PromptTemplate
from .views import generate_prompt_view
from api_manager.models import APIKey

@admin.register(PersonalizationProfile)
class PersonalizationProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active')
    change_form_template = "admin/prompt_manager/personalizationprofile/change_form.html"

    # We don't need get_form anymore for this purpose
    # We will use add_view and change_view to pass extra context

    def add_view(self, request, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['api_keys'] = APIKey.objects.filter(user=request.user, is_active=True)
        return super().add_view(request, form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context['api_keys'] = APIKey.objects.filter(user=request.user, is_active=True)
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('generate-prompt/', self.admin_site.admin_view(generate_prompt_view), name='prompt_manager_personalizationprofile_generate_prompt')
        ]
        return custom_urls + urls

@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active')
