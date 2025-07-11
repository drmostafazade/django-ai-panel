from django.db import migrations

def add_providers(apps, schema_editor):
    AIProvider = apps.get_model('ai_manager', 'AIProvider')
    
    providers = [
        ('gemini', 'Google Gemini'),
        ('deepseek', 'DeepSeek'),
        ('groq', 'Groq'),
        ('github', 'GitHub Copilot'),
        ('cohere', 'Cohere'),
        ('mistral', 'Mistral AI'),
    ]
    
    for name, display in providers:
        AIProvider.objects.get_or_create(name=name, defaults={'is_active': True})

def remove_providers(apps, schema_editor):
    AIProvider = apps.get_model('ai_manager', 'AIProvider')
    AIProvider.objects.filter(name__in=['gemini', 'deepseek', 'groq', 'github', 'cohere', 'mistral']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('ai_manager', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(add_providers, remove_providers),
    ]
from django.db import migrations

def add_providers(apps, schema_editor):
    AIProvider = apps.get_model('ai_manager', 'AIProvider')
    
    providers = [
        ('gemini', 'Google Gemini'),
        ('deepseek', 'DeepSeek'),
        ('groq', 'Groq'),
        ('github', 'GitHub Copilot'),
        ('cohere', 'Cohere'),
        ('mistral', 'Mistral AI'),
    ]
    
    for name, display in providers:
        AIProvider.objects.get_or_create(name=name, defaults={'is_active': True})

def remove_providers(apps, schema_editor):
    AIProvider = apps.get_model('ai_manager', 'AIProvider')
    AIProvider.objects.filter(name__in=['gemini', 'deepseek', 'groq', 'github', 'cohere', 'mistral']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('ai_manager', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(add_providers, remove_providers),
    ]
