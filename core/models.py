from django.db import models
class AIProviderSetting(models.Model):
    class ProviderChoices(models.TextChoices): OPENAI='openai', 'OpenAI'; CLAUDE='claude', 'Anthropic (Claude)'; GEMINI='gemini', 'Google (Gemini)'; GROQ='groq', 'Groq'
    provider = models.CharField(max_length=50, choices=ProviderChoices.choices, unique=True)
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
