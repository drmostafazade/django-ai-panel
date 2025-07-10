from django.contrib import admin
from django.utils.html import format_html
from .models import GitHubToken, Repository

admin.site.site_header = "پنل توسعه هوشمند بسپار"
admin.site.site_title = "پنل بسپار"
admin.site.index_title = "خوش آمدید"

@admin.register(GitHubToken)
class GitHubTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'masked_token', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def masked_token(self, obj):
        if obj.token:
            return f"{obj.token[:10]}..." if len(obj.token) > 10 else "***"
        return "-"
    masked_token.short_description = "توکن"

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'status_icon', 'created_at']
    list_filter = ['is_active', 'user', 'created_at']
    search_fields = ['name', 'full_name', 'description']
    actions = ['activate_repos', 'deactivate_repos']
    
    def status_icon(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✅ فعال</span>')
        return format_html('<span style="color: gray;">⭕ غیرفعال</span>')
    status_icon.short_description = "وضعیت"
    
    def activate_repos(self, request, queryset):
        queryset.update(is_active=True)
    activate_repos.short_description = "فعال کردن مخازن انتخابی"
    
    def deactivate_repos(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_repos.short_description = "غیرفعال کردن مخازن انتخابی"
