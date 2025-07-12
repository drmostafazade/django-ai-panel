from django.db import models
from django.conf import settings
import json

class AIProvider(models.Model):
    class ProviderName(models.TextChoices):
        CLAUDE = 'claude', 'Anthropic (Claude)'
        OPENAI = 'openai', 'OpenAI'
        GEMINI = 'gemini', 'Google (Gemini)'
        GROQ = 'groq', 'Groq'
        DEEPSEEK = 'deepseek', 'DeepSeek'
        GITHUB = 'github', 'GitHub'

    name = models.CharField(max_length=50, choices=ProviderName.choices, unique=True)
    is_active = models.BooleanField(default=True)

    @property
    def display_name(self):
        return f"{self.provider.get_name_display()} - {self.model_name}"

    def __str__(self):
        return self.get_name_display()

class APIKey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    provider = models.ForeignKey(AIProvider, on_delete=models.CASCADE)
    key = models.CharField(max_length=255) # Should be encrypted in production
    model_name = models.CharField(max_length=100, blank=True, null=True)
    model_info = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    last_used = models.DateTimeField(null=True, blank=True)
    used_tokens = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def display_name(self):
        return f"{self.provider.get_name_display()} - {self.model_name}"

    def __str__(self):
        return f"{self.user.username} - {self.provider.get_name_display()} ({self.model_name or 'N/A'})"
