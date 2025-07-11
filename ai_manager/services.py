import anthropic
import openai
import google.generativeai as genai
from groq import Groq
import cohere
from mistralai.client import MistralClient
from datetime import datetime
import json
import requests
from typing import Dict, List, Optional, Tuple

class AIModelRegistry:
    """رجیستری مرکزی برای مدیریت مدل‌های AI"""
    
    # آخرین مدل‌های Claude
    CLAUDE_MODELS = {
        'claude-3-5-haiku-20241022': {
            'name': 'Claude 3.5 Haiku',
            'description': 'سریع‌ترین - مناسب برای کارهای ساده',
            'context': 200000,
            'features': ['search-results'],
            'pricing': {'input': 0.80, 'output': 4.00}
        },
        'claude-3-5-sonnet-20241022': {
            'name': 'Claude 3.5 Sonnet', 
            'description': 'متعادل - بهترین نسبت قیمت به عملکرد',
            'context': 200000,
            'features': ['search-results'],
            'pricing': {'input': 3.00, 'output': 15.00}
        },
        'claude-3-7-sonnet-20250219': {
            'name': 'Claude 3.7 Sonnet',
            'description': 'جدیدترین نسخه Sonnet',
            'context': 200000,
            'features': ['search-results'],
            'pricing': {'input': 3.00, 'output': 15.00}
        },
        'claude-opus-4-20250514': {
            'name': 'Claude Opus 4',
            'description': 'قوی‌ترین - مناسب برای کارهای پیچیده',
            'context': 200000,
            'features': ['search-results'],
            'pricing': {'input': 15.00, 'output': 75.00}
        },
        'claude-sonnet-4-20250514': {
            'name': 'Claude Sonnet 4',
            'description': 'آخرین نسخه Sonnet 4',
            'context': 200000,
            'features': ['search-results'],
            'pricing': {'input': 3.00, 'output': 15.00}
        },
        'claude-3-opus-20240229': {
            'name': 'Claude 3 Opus',
            'description': 'مدل قدرتمند نسل 3',
            'context': 200000,
            'features': [],
            'pricing': {'input': 15.00, 'output': 75.00}
        },
        'claude-3-sonnet-20240229': {
            'name': 'Claude 3 Sonnet',
            'description': 'مدل متعادل نسل 3',
            'context': 200000,
            'features': [],
            'pricing': {'input': 3.00, 'output': 15.00}
        },
        'claude-3-haiku-20240307': {
            'name': 'Claude 3 Haiku',
            'description': 'مدل سریع نسل 3',
            'context': 200000,
            'features': [],
            'pricing': {'input': 0.25, 'output': 1.25}
        }
    }
    
    # مدل‌های Groq
    GROQ_MODELS = {
        'llama3-70b-8192': {
            'name': 'Llama 3 70B',
            'description': 'قوی‌ترین مدل Groq',
            'context': 8192,
            'pricing': {'input': 0.59, 'output': 0.79}
        },
        'llama3-8b-8192': {
            'name': 'Llama 3 8B',
            'description': 'مدل سریع و کارآمد',
            'context': 8192,
            'pricing': {'input': 0.05, 'output': 0.08}
        },
        'mixtral-8x7b-32768': {
            'name': 'Mixtral 8x7B',
            'description': 'مدل قدرتمند با context بزرگ',
            'context': 32768,
            'pricing': {'input': 0.24, 'output': 0.24}
        },
        'gemma-7b-it': {
            'name': 'Gemma 7B',
            'description': 'مدل Google متن‌باز',
            'context': 8192,
            'pricing': {'input': 0.07, 'output': 0.07}
        }
    }
    
    # مدل‌های DeepSeek
    DEEPSEEK_MODELS = {
        'deepseek-chat': {
            'name': 'DeepSeek Chat',
            'description': 'مدل چت عمومی',
            'context': 32768,
            'pricing': {'input': 0.14, 'output': 0.28}
        },
        'deepseek-coder': {
            'name': 'DeepSeek Coder',
            'description': 'مخصوص برنامه‌نویسی',
            'context': 16384,
            'pricing': {'input': 0.14, 'output': 0.28}
        }
    }
    
    # مدل‌های GitHub Copilot
    GITHUB_MODELS = {
        'gpt-4o': {
            'name': 'GPT-4 Optimized',
            'description': 'مدل بهینه شده GitHub',
            'context': 128000,
            'features': ['code-completion', 'chat'],
            'pricing': {'input': 0.01, 'output': 0.03}
        },
        'gpt-3.5-turbo': {
            'name': 'GPT-3.5 Turbo',
            'description': 'مدل سریع',
            'context': 16385,
            'features': ['code-completion', 'chat'],
            'pricing': {'input': 0.002, 'output': 0.002}
        }
    }

class AIService:
    """سرویس اصلی برای مدیریت ارتباط با AI providers"""
    
    @staticmethod
    def get_claude_models(api_key: str) -> Dict:
        """دریافت و تست مدل‌های Claude"""
        try:
            client = anthropic.Anthropic(api_key=api_key)
            available_models = []
            
            for model_id, info in AIModelRegistry.CLAUDE_MODELS.items():
                model_data = {
                    'id': model_id,
                    'name': info['name'],
                    'description': info['description'],
                    'context_window': info['context'],
                    'features': info['features'],
                    'pricing': info['pricing']
                }
                
                try:
                    # تست سریع
                    response = client.messages.create(
                        model=model_id,
                        max_tokens=1,
                        messages=[{"role": "user", "content": "."}]
                    )
                    model_data['available'] = True
                except:
                    model_data['available'] = False
                
                available_models.append(model_data)
            
            return {
                'success': True,
                'models': available_models,
                'account_info': {'api_key_valid': True}
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'models': []}
    
    @staticmethod
    def get_openai_models(api_key: str) -> Dict:
        """دریافت مدل‌های OpenAI"""
        try:
            client = openai.OpenAI(api_key=api_key)
            models = client.models.list()
            
            chat_models = []
            for model in models.data:
                if any(x in model.id for x in ['gpt-4', 'gpt-3.5', 'gpt-4o']):
                    model_info = {
                        'id': model.id,
                        'name': model.id,
                        'created': datetime.fromtimestamp(model.created).strftime('%Y-%m-%d'),
                        'context_window': AIService._get_openai_context(model.id),
                        'available': True
                    }
                    chat_models.append(model_info)
            
            return {
                'success': True,
                'models': sorted(chat_models, key=lambda x: x['name'], reverse=True),
                'account_info': {'api_key_valid': True}
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'models': []}
    
    @staticmethod
    def get_gemini_models(api_key: str) -> Dict:
        """دریافت مدل‌های Google Gemini"""
        try:
            genai.configure(api_key=api_key)
            
            models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    model_info = {
                        'id': model.name.split('/')[-1],
                        'name': model.display_name,
                        'description': model.description,
                        'context_window': getattr(model, 'input_token_limit', 0),
                        'output_limit': getattr(model, 'output_token_limit', 0),
                        'available': True
                    }
                    models.append(model_info)
            
            return {'success': True, 'models': models, 'account_info': {'api_key_valid': True}}
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'models': []}
    
    @staticmethod
    def get_groq_models(api_key: str) -> Dict:
        """دریافت مدل‌های Groq"""
        try:
            client = Groq(api_key=api_key)
            
            available_models = []
            for model_id, info in AIModelRegistry.GROQ_MODELS.items():
                model_data = {
                    'id': model_id,
                    'name': info['name'],
                    'description': info['description'],
                    'context_window': info['context'],
                    'pricing': info['pricing'],
                    'available': True
                }
                available_models.append(model_data)
            
            return {'success': True, 'models': available_models, 'account_info': {'api_key_valid': True}}
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'models': []}
    
    @staticmethod
    def get_deepseek_models(api_key: str) -> Dict:
        """دریافت مدل‌های DeepSeek"""
        try:
            # DeepSeek از OpenAI-compatible API استفاده می‌کند
            available_models = []
            for model_id, info in AIModelRegistry.DEEPSEEK_MODELS.items():
                model_data = {
                    'id': model_id,
                    'name': info['name'],
                    'description': info['description'],
                    'context_window': info['context'],
                    'pricing': info['pricing'],
                    'available': True
                }
                available_models.append(model_data)
            
            return {'success': True, 'models': available_models, 'account_info': {'api_key_valid': True}}
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'models': []}
    
    @staticmethod
    def get_github_models(api_key: str) -> Dict:
        """دریافت مدل‌های GitHub Copilot"""
        try:
            # GitHub Copilot از Azure OpenAI استفاده می‌کند
            available_models = []
            for model_id, info in AIModelRegistry.GITHUB_MODELS.items():
                model_data = {
                    'id': model_id,
                    'name': info['name'],
                    'description': info['description'],
                    'context_window': info['context'],
                    'features': info.get('features', []),
                    'pricing': info['pricing'],
                    'available': True
                }
                available_models.append(model_data)
            
            return {'success': True, 'models': available_models, 'account_info': {'api_key_valid': True}}
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'models': []}
    
    @staticmethod
    def test_api_key(provider: str, api_key: str, model_name: str) -> Dict:
        """تست کامل API key"""
        try:
            if provider == 'claude':
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model=model_name,
                    max_tokens=10,
                    messages=[{"role": "user", "content": "test"}]
                )
                return {
                    'success': True,
                    'model': model_name,
                    'usage': {
                        'total_tokens': response.usage.input_tokens + response.usage.output_tokens
                    }
                }
                
            elif provider == 'openai':
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=10
                )
                return {
                    'success': True,
                    'model': model_name,
                    'usage': {'total_tokens': response.usage.total_tokens}
                }
                
            elif provider == 'gemini':
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("test")
                return {'success': True, 'model': model_name}
                
            elif provider == 'groq':
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=10
                )
                return {'success': True, 'model': model_name}
                
            elif provider == 'deepseek':
                # DeepSeek API endpoint
                headers = {'Authorization': f'Bearer {api_key}'}
                response = requests.post(
                    'https://api.deepseek.com/v1/chat/completions',
                    headers=headers,
                    json={
                        'model': model_name,
                        'messages': [{"role": "user", "content": "test"}],
                        'max_tokens': 10
                    }
                )
                if response.status_code == 200:
                    return {'success': True, 'model': model_name}
                else:
                    return {'success': False, 'error': response.text}
                    
            elif provider == 'github':
                # GitHub Copilot endpoint
                headers = {'Authorization': f'Bearer {api_key}'}
                response = requests.post(
                    'https://api.githubcopilot.com/v1/chat/completions',
                    headers=headers,
                    json={
                        'model': model_name,
                        'messages': [{"role": "user", "content": "test"}],
                        'max_tokens': 10
                    }
                )
                if response.status_code == 200:
                    return {'success': True, 'model': model_name}
                else:
                    return {'success': False, 'error': 'GitHub Copilot API key invalid'}
                    
            else:
                return {'success': False, 'error': f'Provider {provider} not supported'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def _get_openai_context(model_id: str) -> int:
        contexts = {
            'gpt-4o': 128000,
            'gpt-4-turbo': 128000,
            'gpt-4': 8192,
            'gpt-3.5-turbo': 16385
        }
        for key, value in contexts.items():
            if key in model_id:
                return value
        return 4096

    @staticmethod
    def get_token_balance(provider: str, api_key: str) -> Dict:
        """دریافت موجودی توکن از API"""
        try:
            if provider == 'claude':
                # متاسفانه Anthropic API مستقیماً موجودی ندارد
                # اما می‌توانیم از rate limits استفاده کنیم
                client = anthropic.Anthropic(api_key=api_key)
                
                # تست برای بررسی
                try:
                    response = client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=1,
                        messages=[{"role": "user", "content": "."}]
                    )
                    
                    return {
                        'success': True,
                        'balance': 'نامحدود',
                        'rate_limit': '400,000 tokens/minute',
                        'plan': 'Pay-as-you-go'
                    }
                except anthropic.RateLimitError as e:
                    return {
                        'success': True,
                        'balance': 'محدود شده',
                        'error': str(e)
                    }
                    
            elif provider == 'openai':
                # دریافت موجودی از OpenAI
                headers = {'Authorization': f'Bearer {api_key}'}
                
                # بررسی موجودی حساب
                usage_resp = requests.get(
                    'https://api.openai.com/v1/dashboard/billing/credit_grants',
                    headers=headers
                )
                
                if usage_resp.status_code == 200:
                    data = usage_resp.json()
                    total_granted = data.get('total_granted', 0)
                    total_used = data.get('total_used', 0)
                    total_available = data.get('total_available', 0)
                    
                    return {
                        'success': True,
                        'balance': total_available,
                        'used': total_used,
                        'granted': total_granted,
                        'plan': data.get('plan', 'Unknown')
                    }
                else:
                    # اگر credit grants نبود، subscription را چک کن
                    sub_resp = requests.get(
                        'https://api.openai.com/v1/dashboard/billing/subscription',
                        headers=headers
                    )
                    
                    if sub_resp.status_code == 200:
                        sub_data = sub_resp.json()
                        return {
                            'success': True,
                            'balance': 'بر اساس اشتراک',
                            'hard_limit_usd': sub_data.get('hard_limit_usd', 0),
                            'plan': sub_data.get('plan', {}).get('title', 'Unknown')
                        }
                        
            elif provider == 'gemini':
                # Google Gemini معمولاً رایگان است با محدودیت rate
                return {
                    'success': True,
                    'balance': 'رایگان',
                    'rate_limit': '60 requests/minute',
                    'plan': 'Free Tier'
                }
                
            return {'success': False, 'error': 'Provider not supported'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    @staticmethod
    def format_token_display(balance_info: Dict) -> str:
        """فرمت نمایش موجودی توکن"""
        if isinstance(balance_info.get('balance'), (int, float)):
            balance = balance_info['balance']
            if balance > 1_000_000:
                return f"{balance/1_000_000:.1f}M"
            elif balance > 1_000:
                return f"{balance/1_000:.1f}K"
            else:
                return str(int(balance))
        return str(balance_info.get('balance', 'نامشخص'))
