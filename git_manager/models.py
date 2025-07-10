from django.db import models
from django.contrib.auth.models import User

class GitHubToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - GitHub Token"

class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    html_url = models.URLField()
    is_active = models.BooleanField(default=False)
    last_synced = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Repositories"
        ordering = ['-is_active', 'name']
    
    def __str__(self):
        return self.full_name
