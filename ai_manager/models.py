from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class AIProvider(models.Model):
    PROVIDER_CHOICES = [        ('claude', 'Claude (Anthropic)'),        ('openai', 'OpenAI (GPT)'),        ('gemini', 'Google Gemini'),        ('deepseek', 'DeepSeek'),        ('groq', 'Groq'),        ('github', 'GitHub Copilot'),        ('cohere', 'Cohere'),        ('mistral', 'Mistral AI'),    ]
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

class PersonalPrompt(models.Model):
    """پرامپت‌های شخصی‌سازی شده"""
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE, related_name='prompts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('general', 'عمومی'),
        ('odoo', 'Odoo Development'),
        ('wordpress', 'WordPress'),
        ('django', 'Django'),
        ('debug', 'Debug & Fix'),
    ], default='general')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', '-created_at']
        verbose_name = 'Personal Prompt'
        verbose_name_plural = 'Personal Prompts'
    
    def __str__(self):
        return f"{self.title} - {self.api_key.provider.name}"

class APIKey(models.Model):
    # ... فیلدهای قبلی ...
    
    # اضافه کردن فیلدهای جدید
    token_balance = models.BigIntegerField(default=0, help_text='موجودی توکن')
    token_limit = models.BigIntegerField(default=0, help_text='سقف توکن')
    subscription_plan = models.CharField(max_length=100, blank=True, help_text='نوع اشتراک')
    last_balance_check = models.DateTimeField(null=True, blank=True)
    
    # ذخیره prompts شخصی‌سازی شده
    personal_prompts = models.JSONField(default=dict, blank=True)
    
    @property
    def token_percentage(self):
        """درصد توکن‌های باقی‌مانده"""
        if self.token_limit > 0:
            return int((self.token_balance / self.token_limit) * 100)
        return 100

class PersonalPrompt(models.Model):
    """پرامپت‌های شخصی‌سازی شده"""
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE, related_name='prompts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('general', 'عمومی'),
        ('odoo', 'Odoo Development'),
        ('wordpress', 'WordPress'),
        ('django', 'Django'),
        ('debug', 'Debug & Fix'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', '-created_at']
