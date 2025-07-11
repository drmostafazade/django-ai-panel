import anthropic
import openai
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class BalanceService:
    """سرویس مدیریت موجودی حساب‌های AI"""
    
    @staticmethod
    def get_claude_balance(api_key: str) -> Dict:
        """دریافت موجودی Claude"""
        try:
            client = anthropic.Anthropic(api_key=api_key)
            # تست کوچک برای بررسی API
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1,
                messages=[{"role": "user", "content": "hi"}]
            )
            
            return {
                'success': True,
                'balance_type': 'unlimited',
                'status': 'فعال',
                'message': 'حساب فعال و کارآمد'
            }
        except Exception as e:
            error_msg = str(e)
            if "credit" in error_msg.lower() or "quota" in error_msg.lower():
                return {
                    'success': False,
                    'balance_type': 'depleted',
                    'error': 'موجودی تمام شده'
                }
            elif "invalid" in error_msg.lower():
                return {
                    'success': False,
                    'balance_type': 'invalid',
                    'error': 'API Key نامعتبر'
                }
            else:
                return {
                    'success': False,
                    'error': f'خطا: {error_msg}'
                }
    
    @staticmethod
    def get_openai_balance(api_key: str) -> Dict:
        """دریافت موجودی OpenAI"""
        try:
            client = openai.OpenAI(api_key=api_key)
            # تست ساده
            models = client.models.list()
            
            return {
                'success': True,
                'balance_type': 'active',
                'status': 'فعال',
                'message': f'{len(models.data)} مدل در دسترس'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_balance_for_provider(provider: str, api_key: str) -> Dict:
        """دریافت موجودی بر اساس provider"""
        try:
            if provider == 'claude':
                return BalanceService.get_claude_balance(api_key)
            elif provider == 'openai':
                return BalanceService.get_openai_balance(api_key)
            else:
                return {
                    'success': True,
                    'balance_type': 'unknown',
                    'status': 'در دسترس',
                    'message': 'پشتیبانی به زودی اضافه می‌شود'
                }
        except Exception as e:
            logger.error(f"Error in get_balance_for_provider: {e}")
            return {
                'success': False,
                'error': str(e)
            }
