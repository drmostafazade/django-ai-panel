from django.contrib import admin
from django.urls import path
from .models import PersonalizationProfile, PromptTemplate
from .views import generate_prompt_view

@admin.register(PersonalizationProfile)
class PersonalizationProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active')
    # Editable fields are listed here
    fields = ('user', 'name', 'is_active')
    # Non-editable fields are listed here
    readonly_fields = ('system_prompt',)
    
    # This remains the same to include our custom UI
    change_form_template = "admin/prompt_manager/personalizationprofile/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'generate-prompt/',
                self.admin_site.admin_view(generate_prompt_view),
                name='prompt_manager_personalizationprofile_generate_prompt'
            )
        ]
        return custom_urls + urls

@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active')
