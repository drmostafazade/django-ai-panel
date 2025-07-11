import anthropic
import openai
from datetime import datetime
import json

class AIService:
    """سرویس مدیریت ارتباط با AI providers"""
    
    @staticmethod
    def get_claude_models(api_key):
        """دریافت مدل‌های Claude از API"""
        try:
            client = anthropic.Anthropic(api_key=api_key)
            
            # لیست مدل‌های فعلی Claude - این لیست باید از API گرفته شود
            # متاسفانه Anthropic API فعلاً endpoint برای لیست مدل‌ها ندارد
            # اما می‌توانیم با تست هر مدل، موجود بودن آن را بررسی کنیم
            
            available_models = []
            
            # مدل‌های شناخته شده Claude
            known_models = [
                'claude-3-opus-20240229',
                'claude-3-sonnet-20240229', 
                'claude-3-haiku-20240307',
                'claude-2.1',
                'claude-2.0',
                'claude-instant-1.2'
            ]
            
            for model_id in known_models:
                try:
                    # تست سریع برای بررسی دسترسی به مدل
                    response = client.messages.create(
                        model=model_id,
                        max_tokens=1,
                        messages=[{"role": "user", "content": "."}]
                    )
                    
                    # اگر موفق بود، مدل موجود است
                    model_info = {
                        'id': model_id,
                        'name': AIService.get_model_display_name(model_id),
                        'context_window': AIService.get_context_window(model_id),
                        'available': True,
                        'input_cost': AIService.get_model_pricing(model_id)['input'],
                        'output_cost': AIService.get_model_pricing(model_id)['output']
                    }
                    available_models.append(model_info)
                    
                except Exception:
                    # مدل موجود نیست یا دسترسی نداریم
                    pass
            
            return {
                'success': True,
                'models': available_models,
                'account_info': {
                    'api_key_valid': True,
                    'rate_limits': 'بر اساس طرح شما'
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'models': []
            }
    
    @staticmethod
    def get_openai_models(api_key):
        """دریافت مدل‌های OpenAI از API"""
        try:
            client = openai.OpenAI(api_key=api_key)
            models = client.models.list()
            
            chat_models = []
            for model in models.data:
                # فقط مدل‌های چت را نمایش می‌دهیم
                if any(x in model.id for x in ['gpt-4', 'gpt-3.5']):
                    model_info = {
                        'id': model.id,
                        'name': model.id,
                        'created': datetime.fromtimestamp(model.created).strftime('%Y-%m-%d'),
                        'owned_by': model.owned_by,
                        'context_window': AIService.get_openai_context(model.id),
                        'available': True
                    }
                    chat_models.append(model_info)
            
            # مرتب‌سازی بر اساس قدرت مدل
            priority_order = ['gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo']
            chat_models.sort(
                key=lambda x: next((i for i, p in enumerate(priority_order) if p in x['id']), 999)
            )
            
            return {
                'success': True,
                'models': chat_models,
                'account_info': {
                    'api_key_valid': True
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'models': []
            }
    
    @staticmethod
    def get_model_display_name(model_id):
        """نام نمایشی مدل"""
        names = {
            'claude-3-opus-20240229': 'Claude 3 Opus (قوی‌ترین)',
            'claude-3-sonnet-20240229': 'Claude 3 Sonnet (متعادل)',
            'claude-3-haiku-20240307': 'Claude 3 Haiku (سریع)',
            'claude-2.1': 'Claude 2.1',
            'claude-2.0': 'Claude 2.0',
            'claude-instant-1.2': 'Claude Instant 1.2'
        }
        return names.get(model_id, model_id)
    
    @staticmethod
    def get_context_window(model_id):
        """اندازه context window"""
        windows = {
            'claude-3-opus-20240229': 200000,
            'claude-3-sonnet-20240229': 200000,
            'claude-3-haiku-20240307': 200000,
            'claude-2.1': 200000,
            'claude-2.0': 100000,
            'claude-instant-1.2': 100000
        }
        return windows.get(model_id, 100000)
    
    @staticmethod
    def get_openai_context(model_id):
        """Context window برای OpenAI"""
        windows = {
            'gpt-4-turbo-preview': 128000,
            'gpt-4-turbo': 128000,
            'gpt-4': 8192,
            'gpt-4-32k': 32768,
            'gpt-3.5-turbo': 16385,
            'gpt-3.5-turbo-16k': 16385
        }
        return windows.get(model_id, 4096)
    
    @staticmethod
    def get_model_pricing(model_id):
        """قیمت‌گذاری مدل‌ها (per 1M tokens)"""
        pricing = {
            'claude-3-opus-20240229': {'input': 15.00, 'output': 75.00},
            'claude-3-sonnet-20240229': {'input': 3.00, 'output': 15.00},
            'claude-3-haiku-20240307': {'input': 0.25, 'output': 1.25},
            'claude-2.1': {'input': 8.00, 'output': 24.00},
            'claude-2.0': {'input': 8.00, 'output': 24.00},
            'claude-instant-1.2': {'input': 0.80, 'output': 2.40}
        }
        return pricing.get(model_id, {'input': 0, 'output': 0})
    
    @staticmethod
    def test_api_key(provider, api_key, model_name):
        """تست کامل API key با اطلاعات حساب"""
        try:
            if provider == 'claude':
                client = anthropic.Anthropic(api_key=api_key)
                
                # تست ارسال پیام
                response = client.messages.create(
                    model=model_name,
                    max_tokens=10,
                    messages=[{"role": "user", "content": "test"}]
                )
                
                usage = response.usage
                pricing = AIService.get_model_pricing(model_name)
                
                return {
                    'success': True,
                    'model': model_name,
                    'usage': {
                        'input_tokens': usage.input_tokens,
                        'output_tokens': usage.output_tokens,
                        'total_tokens': usage.input_tokens + usage.output_tokens,
                        'estimated_cost': (
                            (usage.input_tokens * pricing['input'] / 1_000_000) +
                            (usage.output_tokens * pricing['output'] / 1_000_000)
                        )
                    },
                    'model_info': {
                        'context_window': AIService.get_context_window(model_name),
                        'input_price': f"${pricing['input']}/1M tokens",
                        'output_price': f"${pricing['output']}/1M tokens"
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
                
                return {
                    'success': True,
                    'model': model_name,
                    'usage': {
                        'prompt_tokens': usage.prompt_tokens,
                        'completion_tokens': usage.completion_tokens,
                        'total_tokens': usage.total_tokens
                    },
                    'model_info': {
                        'context_window': AIService.get_openai_context(model_name)
                    }
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
