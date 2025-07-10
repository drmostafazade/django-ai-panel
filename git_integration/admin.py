from django.contrib import admin
from .models import GitHubToken, Repository

@admin.register(GitHubToken)
class GitHubTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

@admin.register(Repository)  
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_active', 'last_synced']
    list_filter = ['is_active', 'user']
