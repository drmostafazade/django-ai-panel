from django.db import models
from django.contrib.auth.models import User

class GitHubToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Token"

class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    html_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Repositories"
