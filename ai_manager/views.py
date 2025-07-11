from django.shortcuts import render, redirect
from .services import AIService, AIModelRegistry
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from .models import AIProvider, APIKey, TokenUsage
from .services import AIService
import json
from datetime import datetime, timedelta

@login_required
def ai_chat(request):
    """صفحه اصلی چت AI"""
    user_keys = APIKey.objects.filter(user=request.user, is_active=True)
    providers = AIProvider.objects.filter(is_active=True)
    
    context = {
        'user_keys': user_keys,
        'providers': providers,
        'has_keys': user_keys.exists(),
    }
    return render(request, 'ai_manager/chat.html', context)

@login_required
def api_settings(request):
    """مدیریت API Keys"""
    if request.method == 'POST':
        provider_id = request.POST.get('provider')
        api_key = request.POST.get('api_key')
        model_name = request.POST.get('model_name')
        model_info = request.POST.get('model_info', '{}')
        
        if provider_id and api_key and model_name:
            try:
                provider = AIProvider.objects.get(id=provider_id)
                
                # تست API key قبل از ذخیره
                test_result = AIService.test_api_key(provider.name, api_key, model_name)
                
                if test_result['success']:
                    # ذخیره یا آپدیت
                    api_key_obj, created = APIKey.objects.update_or_create(
                        user=request.user,
                        provider=provider,
                        defaults={
                            'key': api_key,
                            'model_name': model_name,
                            'model_info': json.loads(model_info),
                            'is_active': True,
                            'is_verified': True,
                            'last_tested': timezone.now()
                        }
                    )
                    
                    action = "ذخیره" if created else "آپدیت"
                    messages.success(request, f'کلید API {provider.get_name_display()} {action} شد.')
                else:
                    messages.error(request, f'خطا در تست API: {test_result.get("error", "Unknown error")}')
                    
                return redirect('api_settings')
                
            except AIProvider.DoesNotExist:
                messages.error(request, 'سرویس انتخاب شده معتبر نیست.')
            except Exception as e:
                messages.error(request, f'خطا: {str(e)}')
    
    # محاسبه آمار ماهانه
    start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    month_stats = TokenUsage.objects.filter(
        api_key__user=request.user,
        timestamp__gte=start_of_month
    ).aggregate(
        total_tokens=Sum('total_tokens'),
        total_cost=Sum('cost')
    )
    
    providers = AIProvider.objects.filter(is_active=True)
    user_keys = APIKey.objects.filter(user=request.user)
    
    context = {
        'providers': providers,
        'user_keys': user_keys,
        'total_tokens_month': month_stats['total_tokens'] or 0,
        'total_cost_month': month_stats['total_cost'] or 0,
    }
    return render(request, 'ai_manager/api_settings.html', context)

@login_required
def get_available_models(request):
    """دریافت لیست مدل‌های موجود از API"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        provider_name = data.get('provider')
        api_key = data.get('api_key')
        
        if provider_name == 'claude':
            result = AIService.get_claude_models(api_key)
        elif provider_name == 'openai':
            result = AIService.get_openai_models(api_key)
        else:
            result = {
                'success': False,
                'error': f'Provider {provider_name} not implemented yet'
            }
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def test_api_connection(request):
    """تست اتصال و دریافت اطلاعات حساب"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        provider_id = data.get('provider')
        api_key = data.get('api_key')
        model_name = data.get('model_name')
        
        provider = AIProvider.objects.get(id=provider_id)
        result = AIService.test_api_key(provider.name, api_key, model_name)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def toggle_api_key(request):
    """فعال/غیرفعال کردن API Key"""
    if request.method == 'POST':
        key_id = request.POST.get('key_id')
        try:
            api_key = APIKey.objects.get(id=key_id, user=request.user)
            api_key.is_active = not api_key.is_active
            api_key.save()
            status = "فعال" if api_key.is_active else "غیرفعال"
            messages.success(request, f'API Key {status} شد.')
        except APIKey.DoesNotExist:
            messages.error(request, 'API Key یافت نشد.')
    
    return redirect('api_settings')

@login_required
def delete_api_key(request):
    """حذف API Key"""
    if request.method == 'POST':
        key_id = request.POST.get('key_id')
        try:
            api_key = APIKey.objects.get(id=key_id, user=request.user)
            provider_name = api_key.provider.get_name_display()
            api_key.delete()
            messages.success(request, f'API Key {provider_name} حذف شد.')
        except APIKey.DoesNotExist:
            messages.error(request, 'API Key یافت نشد.')
    
    return redirect('api_settings')

@login_required
def retest_api_key(request):
    """تست مجدد API Key ذخیره شده"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        key_id = data.get('key_id')
        
        api_key = APIKey.objects.get(id=key_id, user=request.user)
        
        # تست مجدد
        result = AIService.test_api_key(
            api_key.provider.name,
            api_key.key,
            api_key.model_name
        )
        
        if result['success']:
            api_key.last_tested = timezone.now()
            api_key.is_verified = True
            api_key.save()
        
        return JsonResponse(result)
        
    except APIKey.DoesNotExist:
        return JsonResponse({'error': 'API Key یافت نشد'}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@csrf_exempt
def chat_api(request):
    """API endpoint برای چت"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        message = data.get('message')
        provider = data.get('provider', 'claude')
        
        if not message:
            return JsonResponse({'error': 'پیام الزامی است'}, status=400)
        
        # دریافت API key فعال
        try:
            api_key = APIKey.objects.get(
                user=request.user,
                provider__name=provider,
                is_active=True
            )
        except APIKey.DoesNotExist:
            return JsonResponse({
                'error': f'API Key فعال برای {provider} یافت نشد'
            }, status=400)
        
        # ارسال به AI
        if provider == 'claude':
            import anthropic
            client = anthropic.Anthropic(api_key=api_key.key)
            
            response = client.messages.create(
                model=api_key.model_name,
                max_tokens=1024,
                messages=[{"role": "user", "content": message}]
            )
            
            content = response.content[0].text
            usage = response.usage
            
            # محاسبه هزینه
            pricing = AIService.get_model_pricing(api_key.model_name)
            cost = (
                (usage.input_tokens * pricing['input'] / 1_000_000) +
                (usage.output_tokens * pricing['output'] / 1_000_000)
            )
            
            # ذخیره مصرف
            TokenUsage.objects.create(
                api_key=api_key,
                prompt_tokens=usage.input_tokens,
                completion_tokens=usage.output_tokens,
                total_tokens=usage.input_tokens + usage.output_tokens,
                cost=cost
            )
            
            api_key.used_tokens += (usage.input_tokens + usage.output_tokens)
            api_key.last_used = timezone.now()
            api_key.save()
            
            return JsonResponse({
                'success': True,
                'content': content,
                'usage': {
                    'prompt_tokens': usage.input_tokens,
                    'completion_tokens': usage.output_tokens,
                    'total_tokens': usage.input_tokens + usage.output_tokens,
                    'cost': f"${cost:.4f}",
                    'total_used': api_key.used_tokens
                }
            })
            
        elif provider == 'openai':
            import openai
            client = openai.OpenAI(api_key=api_key.key)
            
            response = client.chat.completions.create(
                model=api_key.model_name,
                messages=[{"role": "user", "content": message}]
            )
            
            content = response.choices[0].message.content
            usage = response.usage
            
            # ذخیره مصرف
            TokenUsage.objects.create(
                api_key=api_key,
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens
            )
            
            api_key.used_tokens += usage.total_tokens
            api_key.last_used = timezone.now()
            api_key.save()
            
            return JsonResponse({
                'success': True,
                'content': content,
                'usage': {
                    'prompt_tokens': usage.prompt_tokens,
                    'completion_tokens': usage.completion_tokens,
                    'total_tokens': usage.total_tokens,
                    'total_used': api_key.used_tokens
                }
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
