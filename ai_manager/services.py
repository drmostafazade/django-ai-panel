import anthropic
import openai
from google import generativeai as genai
import json
from django.conf import settings
from .models import APIKey, TokenUsage

class AIService:
    """Base class for AI services"""
    def __init__(self, api_key):
        self.api_key = api_key
        
    def send_message(self, message):
        raise NotImplementedError

class ClaudeService(AIService):
    """Claude (Anthropic) API integration"""
    def __init__(self, api_key):
        super().__init__(api_key)
        self.client = anthropic.Anthropic(api_key=api_key.key)
        
    def send_message(self, message, model="claude-3-sonnet-20240229"):
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{"role": "user", "content": message}]
            )
            
            # ذخیره مصرف توکن
            TokenUsage.objects.create(
                api_key=self.api_key,
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens
            )
            
            return {
                'success': True,
                'content': response.content[0].text,
                'usage': {
                    'prompt_tokens': response.usage.input_tokens,
                    'completion_tokens': response.usage.output_tokens,
                    'total_tokens': response.usage.input_tokens + response.usage.output_tokens
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

class OpenAIService(AIService):
    """OpenAI (GPT) API integration"""
    def __init__(self, api_key):
        super().__init__(api_key)
        openai.api_key = api_key.key
        self.client = openai.OpenAI(api_key=api_key.key)
        
    def send_message(self, message, model="gpt-3.5-turbo"):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": message}]
            )
            
            # ذخیره مصرف توکن
            TokenUsage.objects.create(
                api_key=self.api_key,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens
            )
            
            return {
                'success': True,
                'content': response.choices[0].message.content,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

def get_ai_service(provider_name, api_key):
    """Factory function to get appropriate AI service"""
    services = {
        'claude': ClaudeService,
        'openai': OpenAIService,
    }
    
    service_class = services.get(provider_name)
    if service_class:
        return service_class(api_key)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
