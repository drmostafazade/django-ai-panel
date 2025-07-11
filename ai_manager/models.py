from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class AIProvider(models.Model):
    PROVIDER_CHOICES = [        ('claude', 'Claude (Anthropic)'),        ('openai', 'OpenAI (GPT)'),        ('gemini', 'Google Gemini'),        ('deepseek', 'DeepSeek'),        ('groq', 'Groq'),        ('github', 'GitHub Copilot'),        ('cohere', 'Cohere'),        ('mistral', 'Mistral AI'),    ]
    
    name = models.CharField(max_length=50, choices=PROVIDER_CHOICES, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_name_display()

class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    provider = models.ForeignKey(AIProvider, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    model_name = models.CharField(max_length=100, blank=True)
    model_info = models.JSONField(default=dict, blank=True)  # اطلاعات مدل
    
    # Token limits and usage
    total_tokens = models.IntegerField(default=0, help_text='کل توکن‌های موجود')
    used_tokens = models.IntegerField(default=0, help_text='توکن‌های مصرف شده')
    rate_limit = models.CharField(max_length=100, blank=True, help_text='محدودیت نرخ')
    
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    last_tested = models.DateTimeField(null=True, blank=True)
    
    @property
    def remaining_tokens(self):
        if self.total_tokens == 0:
            return "نامحدود"
        return self.total_tokens - self.used_tokens
    
    def __str__(self):
        return f"{self.provider.name} - {self.user.username} - {self.model_name or 'No model'}"
    
    class Meta:
        unique_together = ['user', 'provider']
        ordering = ['-created_at']

class TokenUsage(models.Model):
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE, related_name='usage')
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
