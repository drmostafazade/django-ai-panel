from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import GitHubToken, Repository
import requests

admin.site.site_header = "پنل توسعه هوشمند بسپار"
admin.site.site_title = "پنل بسپار"
admin.site.index_title = "خوش آمدید"

@admin.register(GitHubToken)
class GitHubTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'masked_token', 'is_valid', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['test_token']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('settings/', self.admin_site.admin_view(self.settings_view), name='git_settings'),
        ]
        return custom_urls + urls
    
    def settings_view(self, request):
        try:
            token = GitHubToken.objects.get(user=request.user)
        except GitHubToken.DoesNotExist:
            token = None
        
        if request.method == 'POST':
            github_token = request.POST.get('github_token')
            if github_token and not github_token.startswith('•'):
                if token:
                    token.token = github_token
                    token.save()
                else:
                    GitHubToken.objects.create(user=request.user, token=github_token)
                messages.success(request, 'توکن با موفقیت ذخیره شد!')
                return redirect('admin:git_settings')
        
        context = {
            'title': 'تنظیمات GitHub',
            'token': token,
            'site_header': admin.site.site_header,
            'has_permission': True,
        }
        return render(request, 'admin/git_settings.html', context)
    
    def masked_token(self, obj):
        if obj.token:
            return f"{obj.token[:10]}..." if len(obj.token) > 10 else "***"
        return "-"
    masked_token.short_description = "توکن"
    
    def is_valid(self, obj):
        # در آینده می‌توان چک کرد
        return format_html('<span style="color: green;">✅</span>')
    is_valid.short_description = "معتبر"
    
    def test_token(self, request, queryset):
        for token in queryset:
            try:
                headers = {'Authorization': f'token {token.token}'}
                response = requests.get('https://api.github.com/user', headers=headers)
                if response.status_code == 200:
                    messages.success(request, f'توکن {token.user} معتبر است!')
                else:
                    messages.error(request, f'توکن {token.user} نامعتبر است!')
            except:
                messages.error(request, f'خطا در تست توکن {token.user}')
    test_token.short_description = "تست توکن‌های انتخابی"

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'status_icon', 'created_at']
    list_filter = ['is_active', 'user', 'created_at']
    search_fields = ['name', 'full_name', 'description']
    actions = ['activate_repos', 'deactivate_repos', 'sync_repositories']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sync/', self.admin_site.admin_view(self.sync_view), name='sync_repos'),
        ]
        return custom_urls + urls
    
    def sync_view(self, request):
        try:
            token = GitHubToken.objects.get(user=request.user)
            headers = {'Authorization': f'token {token.token}'}
            response = requests.get('https://api.github.com/user/repos', headers=headers)
            
            if response.status_code == 200:
                repos = response.json()
                count = 0
                for repo in repos:
                    Repository.objects.update_or_create(
                        user=request.user,
                        name=repo['name'],
                        defaults={
                            'full_name': repo['full_name'],
                            'description': repo.get('description', ''),
                            'html_url': repo['html_url'],
                        }
                    )
                    count += 1
                messages.success(request, f'{count} مخزن همگام‌سازی شد!')
            else:
                messages.error(request, 'خطا در دریافت مخازن')
        except GitHubToken.DoesNotExist:
            messages.error(request, 'ابتدا توکن GitHub را تنظیم کنید')
        
        return redirect('admin:git_integration_repository_changelist')
    
    def status_icon(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✅ فعال</span>')
        return format_html('<span style="color: gray;">⭕ غیرفعال</span>')
    status_icon.short_description = "وضعیت"
    
    def activate_repos(self, request, queryset):
        count = queryset.update(is_active=True)
        messages.success(request, f'{count} مخزن فعال شد')
    activate_repos.short_description = "فعال کردن مخازن انتخابی"
    
    def deactivate_repos(self, request, queryset):
        count = queryset.update(is_active=False)
        messages.success(request, f'{count} مخزن غیرفعال شد')
    deactivate_repos.short_description = "غیرفعال کردن مخازن انتخابی"
    
    def sync_repositories(self, request, queryset):
        return redirect('admin:sync_repos')
    sync_repositories.short_description = "همگام‌سازی با GitHub"
