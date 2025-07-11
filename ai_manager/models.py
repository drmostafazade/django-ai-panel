from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AIProvider(models.Model):
    PROVIDER_CHOICES = [
        ('claude', 'Claude (Anthropic)'),
        ('openai', 'OpenAI (GPT)'),
        ('gemini', 'Google Gemini'),
        ('deepseek', 'DeepSeek'),
    ]
    
    name = models.CharField(max_length=50, choices=PROVIDER_CHOICES, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_name_display()

class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    provider = models.ForeignKey(AIProvider, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.provider.name} - {self.user.username}"
    
    class Meta:
        unique_together = ['user', 'provider']
