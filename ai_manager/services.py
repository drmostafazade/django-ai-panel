import anthropic
import openai
import google.generativeai as genai
from datetime import datetime
import json
import requests
from typing import Dict, List, Optional, Tuple

class AIModelRegistry:
    """رجیستری مرکزی برای مدیریت مدل‌های AI"""
    
    # آخرین مدل‌های Claude (بر اساس داکیومنت search-results)
    CLAUDE_MODELS = {
        # مدل‌های جدید با قابلیت Search Results
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
        # مدل‌های قدیمی‌تر
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
    
    @classmethod
    def get_available_models(cls, provider: str) -> List[Dict]:
        """دریافت لیست مدل‌های موجود برای هر provider"""
        if provider == 'claude':
            return [
                {
                    'id': model_id,
                    'name': info['name'],
                    'description': info['description'],
                    'context_window': info['context'],
                    'features': info['features'],
                    'pricing': info['pricing']
                }
                for model_id, info in cls.CLAUDE_MODELS.items()
            ]
        return []

class AIService:
    """سرویس اصلی برای مدیریت ارتباط با AI providers"""
    
    @staticmethod
    def get_claude_models(api_key: str) -> Dict:
        """دریافت و تست مدل‌های Claude"""
        try:
            client = anthropic.Anthropic(api_key=api_key)
            available_models = []
            
            # دریافت مدل‌ها از رجیستری
            all_models = AIModelRegistry.get_available_models('claude')
            
            for model in all_models:
                try:
                    # تست سریع برای بررسی دسترسی
                    response = client.messages.create(
                        model=model['id'],
                        max_tokens=1,
                        messages=[{"role": "user", "content": "."}]
                    )
                    
                    model['available'] = True
                    model['test_successful'] = True
                    available_models.append(model)
                    
                except anthropic.NotFoundError:
                    # مدل وجود ندارد
                    model['available'] = False
                    model['error'] = 'Model not found'
                    available_models.append(model)
                    
                except anthropic.AuthenticationError:
                    # مشکل احراز هویت
                    return {
                        'success': False,
                        'error': 'Invalid API key',
                        'models': []
                    }
                    
                except Exception as e:
                    # سایر خطاها
                    model['available'] = False
                    model['error'] = str(e)
                    available_models.append(model)
            
            # دریافت اطلاعات حساب (اگر API موجود باشد)
            account_info = AIService._get_claude_account_info(client)
            
            return {
                'success': True,
                'models': available_models,
                'account_info': account_info
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'models': []
            }
    
    @staticmethod
    def _get_claude_account_info(client) -> Dict:
        """دریافت اطلاعات حساب Claude"""
        try:
            # متاسفانه Anthropic API فعلاً endpoint مستقیم برای account info ندارد
            # اما می‌توانیم از response headers استفاده کنیم
            return {
                'api_key_valid': True,
                'rate_limits': 'بر اساس طرح شما',
                'organization': 'Personal',
                'usage_available': False
            }
        except:
            return {'api_key_valid': True}
    
    @staticmethod
    def get_openai_models(api_key: str) -> Dict:
        """دریافت مدل‌های OpenAI به صورت dynamic"""
        try:
            client = openai.OpenAI(api_key=api_key)
            
            # دریافت لیست مدل‌ها از API
            models = client.models.list()
            
            # دریافت اطلاعات usage
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            # تلاش برای دریافت اطلاعات billing
            usage_info = {}
            try:
                # دریافت اطلاعات subscription
                subscription_resp = requests.get(
                    'https://api.openai.com/v1/dashboard/billing/subscription',
                    headers=headers
                )
                if subscription_resp.status_code == 200:
                    usage_info['subscription'] = subscription_resp.json()
                
                # دریافت usage
                today = datetime.now()
                start_date = today.replace(day=1).strftime('%Y-%m-%d')
                end_date = today.strftime('%Y-%m-%d')
                
                usage_resp = requests.get(
                    f'https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}',
                    headers=headers
                )
                if usage_resp.status_code == 200:
                    usage_info['usage'] = usage_resp.json()
                    
            except:
                pass
            
            # فیلتر و دسته‌بندی مدل‌ها
            chat_models = []
            for model in models.data:
                if any(x in model.id for x in ['gpt-4', 'gpt-3.5', 'gpt-4o']):
                    model_info = {
                        'id': model.id,
                        'name': model.id,
                        'created': datetime.fromtimestamp(model.created).strftime('%Y-%m-%d'),
                        'owned_by': model.owned_by,
                        'context_window': AIService._get_openai_context(model.id),
                        'available': True,
                        'capabilities': AIService._get_model_capabilities(model.id)
                    }
                    chat_models.append(model_info)
            
            # مرتب‌سازی بر اساس قدرت و تاریخ
            chat_models.sort(key=lambda x: (
                'gpt-4o' in x['id'],
                'gpt-4-turbo' in x['id'], 
                'gpt-4' in x['id'],
                x['created']
            ), reverse=True)
            
            return {
                'success': True,
                'models': chat_models,
                'account_info': {
                    'api_key_valid': True,
                    'usage_info': usage_info,
                    'organization': models.data[0].owned_by if models.data else 'Unknown'
                }
            }
            
        except openai.AuthenticationError:
            return {
                'success': False,
                'error': 'Invalid API key',
                'models': []
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'models': []
            }
    
    @staticmethod
    def _get_openai_context(model_id: str) -> int:
        """Context window برای مدل‌های OpenAI"""
        contexts = {
            'gpt-4o': 128000,
            'gpt-4o-mini': 128000,
            'gpt-4-turbo': 128000,
            'gpt-4-turbo-preview': 128000,
            'gpt-4-vision-preview': 128000,
            'gpt-4': 8192,
            'gpt-4-32k': 32768,
            'gpt-3.5-turbo': 16385,
            'gpt-3.5-turbo-16k': 16385,
            'gpt-3.5-turbo-instruct': 4096
        }
        
        # پیدا کردن بهترین match
        for key, value in contexts.items():
            if key in model_id:
                return value
        return 4096
    
    @staticmethod
    def _get_model_capabilities(model_id: str) -> List[str]:
        """قابلیت‌های هر مدل"""
        capabilities = []
        
        if 'vision' in model_id or 'gpt-4o' in model_id:
            capabilities.append('vision')
        
        if 'turbo' in model_id:
            capabilities.append('fast')
            
        if any(x in model_id for x in ['gpt-4', 'gpt-4o']):
            capabilities.append('advanced-reasoning')
            
        if 'function' in model_id or 'gpt' in model_id:
            capabilities.append('function-calling')
            
        return capabilities
    
    @staticmethod
    def get_gemini_models(api_key: str) -> Dict:
        """دریافت مدل‌های Google Gemini"""
        try:
            genai.configure(api_key=api_key)
            
            # دریافت لیست مدل‌ها
            models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    model_info = {
                        'id': model.name.split('/')[-1],
                        'name': model.display_name,
                        'description': model.description,
                        'context_window': getattr(model, 'input_token_limit', 0),
                        'output_limit': getattr(model, 'output_token_limit', 0),
                        'available': True,
                        'capabilities': []
                    }
                    
                    # بررسی قابلیت‌ها
                    if hasattr(model, 'supported_generation_methods'):
                        model_info['capabilities'] = list(model.supported_generation_methods)
                    
                    models.append(model_info)
            
            return {
                'success': True,
                'models': models,
                'account_info': {
                    'api_key_valid': True,
                    'service': 'Google AI Studio'
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'models': []
            }
    
    @staticmethod
    def test_api_key(provider: str, api_key: str, model_name: str) -> Dict:
        """تست کامل API key با دریافت اطلاعات کامل"""
        try:
            if provider == 'claude':
                client = anthropic.Anthropic(api_key=api_key)
                
                # تست با استفاده از beta header برای مدل‌های جدید
                model_info = AIModelRegistry.CLAUDE_MODELS.get(model_name, {})
                
                kwargs = {
                    'model': model_name,
                    'max_tokens': 10,
                    'messages': [{"role": "user", "content": "test"}]
                }
                
                # اگر مدل از search-results پشتیبانی می‌کند
                if 'search-results' in model_info.get('features', []):
                    client = anthropic.Anthropic(
                        api_key=api_key,
                        default_headers={'anthropic-beta': 'search-results-2025-06-09'}
                    )
                
                response = client.messages.create(**kwargs)
                usage = response.usage
                pricing = model_info.get('pricing', {'input': 0, 'output': 0})
                
                # محاسبه هزینه
                cost = (
                    (usage.input_tokens * pricing['input'] / 1_000_000) +
                    (usage.output_tokens * pricing['output'] / 1_000_000)
                )
                
                return {
                    'success': True,
                    'model': model_name,
                    'model_details': model_info,
                    'usage': {
                        'input_tokens': usage.input_tokens,
                        'output_tokens': usage.output_tokens,
                        'total_tokens': usage.input_tokens + usage.output_tokens,
                        'estimated_cost': f"${cost:.6f}"
                    },
                    'features': model_info.get('features', []),
                    'limits': {
                        'context_window': model_info.get('context', 200000),
                        'max_output': 4096
                    }
                }
                
            elif provider == 'openai':
                client = openai.OpenAI(api_key=api_key)
                
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=10
                )
                
                usage = response.usage
                
                # محاسبه هزینه تقریبی
                pricing = AIService._get_openai_pricing(model_name)
                cost = (
                    (usage.prompt_tokens * pricing['input'] / 1_000_000) +
                    (usage.completion_tokens * pricing['output'] / 1_000_000)
                )
                
                return {
                    'success': True,
                    'model': model_name,
                    'usage': {
                        'prompt_tokens': usage.prompt_tokens,
                        'completion_tokens': usage.completion_tokens,
                        'total_tokens': usage.total_tokens,
                        'estimated_cost': f"${cost:.6f}"
                    },
                    'limits': {
                        'context_window': AIService._get_openai_context(model_name),
                        'rate_limit': 'بر اساس طرح شما'
                    }
                }
                
            elif provider == 'gemini':
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name)
                
                response = model.generate_content("test")
                
                return {
                    'success': True,
                    'model': model_name,
                    'usage': {
                        'total_tokens': response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
                    }
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def _get_openai_pricing(model_id: str) -> Dict[str, float]:
        """قیمت‌گذاری OpenAI (per 1M tokens)"""
        pricing = {
            'gpt-4o': {'input': 2.50, 'output': 10.00},
            'gpt-4o-mini': {'input': 0.15, 'output': 0.60},
            'gpt-4-turbo': {'input': 10.00, 'output': 30.00},
            'gpt-4': {'input': 30.00, 'output': 60.00},
            'gpt-3.5-turbo': {'input': 0.50, 'output': 1.50}
        }
        
        for key, value in pricing.items():
            if key in model_id:
                return value
                
        return {'input': 0, 'output': 0}
