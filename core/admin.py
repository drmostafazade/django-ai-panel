from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.models import User
from git_integration.models import Repository, GitHubToken

class DashboardAdmin(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        context = {
            'title': 'داشبورد',
            'total_users': User.objects.count(),
            'total_repos': Repository.objects.count(),
            'active_repos': Repository.objects.filter(is_active=True).count(),
            'has_token': GitHubToken.objects.filter(user=request.user).exists(),
        }
        return render(request, 'admin/dashboard.html', context)

# اگر می‌خواهید از این استفاده کنید:
# admin_site = DashboardAdmin(name='custom_admin')
