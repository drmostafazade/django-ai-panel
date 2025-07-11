from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import AIProvider, APIKey, TokenUsage
import json
import anthropic
import openai
from decimal import Decimal

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
        
        if provider_id and api_key and model_name:
            try:
                provider = AIProvider.objects.get(id=provider_id)
                
                # ذخیره یا آپدیت
                api_key_obj, created = APIKey.objects.update_or_create(
                    user=request.user,
                    provider=provider,
                    defaults={
                        'key': api_key,
                        'model_name': model_name,
                        'is_active': True,
                        'is_verified': True,  # باید از نتیجه تست بیاید
                        'last_tested': timezone.now()
                    }
                )
                
                action = "ذخیره" if created else "آپدیت"
                messages.success(request, f'کلید API {provider.get_name_display()} {action} شد.')
                return redirect('api_settings')
                
            except AIProvider.DoesNotExist:
                messages.error(request, 'سرویس انتخاب شده معتبر نیست.')
    
    providers = AIProvider.objects.filter(is_active=True)
    user_keys = APIKey.objects.filter(user=request.user)
    
    context = {
        'providers': providers,
        'user_keys': user_keys,
    }
    return render(request, 'ai_manager/api_settings.html', context)

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
def get_available_models(request):
    """دریافت لیست مدل‌های موجود از API"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        provider_name = data.get('provider')
        api_key = data.get('api_key')
        
        if provider_name == 'openai':
            client = openai.OpenAI(api_key=api_key)
            models = client.models.list()
            
            # فیلتر مدل‌های مناسب برای چت
            chat_models = []
            for model in models.data:
                if any(x in model.id for x in ['gpt', 'davinci', 'turbo']):
                    chat_models.append({
                        'id': model.id,
                        'name': model.id,
                        'created': model.created,
                        'owned_by': model.owned_by
                    })
            
            return JsonResponse({
                'success': True,
                'models': sorted(chat_models, key=lambda x: x['name'], reverse=True)
            })
            
        elif provider_name == 'claude':
            # Anthropic API مستقیماً لیست مدل ندارد
            # اما می‌توانیم اطلاعات اکانت را بگیریم
            client = anthropic.Anthropic(api_key=api_key)
            
            # لیست مدل‌های فعلی Claude
            models = [
                {'id': 'claude-3-opus-20240229', 'name': 'Claude 3 Opus (قوی‌ترین)', 'context': '200K'},
                {'id': 'claude-3-sonnet-20240229', 'name': 'Claude 3 Sonnet (متعادل)', 'context': '200K'},
                {'id': 'claude-3-haiku-20240307', 'name': 'Claude 3 Haiku (سریع)', 'context': '200K'},
                {'id': 'claude-2.1', 'name': 'Claude 2.1', 'context': '200K'},
                {'id': 'claude-2.0', 'name': 'Claude 2.0', 'context': '100K'},
                {'id': 'claude-instant-1.2', 'name': 'Claude Instant 1.2', 'context': '100K'}
            ]
            
            return JsonResponse({'success': True, 'models': models})
            
        else:
            return JsonResponse({
                'success': False,
                'error': 'این سرویس هنوز پیاده‌سازی نشده'
            })
            
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
        
        if provider.name == 'openai':
            client = openai.OpenAI(api_key=api_key)
            
            # تست ساده
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
            
            # دریافت اطلاعات usage (در صورت موجود بودن)
            usage_info = {
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0,
                'model': model_name,
                'rate_limit': 'بر اساس طرح شما'
            }
            
            return JsonResponse({
                'success': True,
                'model': model_name,
                'usage': usage_info,
                'available_tokens': 'بر اساس طرح OpenAI'
            })
            
        elif provider.name == 'claude':
            client = anthropic.Anthropic(api_key=api_key)
            
            # تست ساده
            response = client.messages.create(
                model=model_name,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            
            usage_info = {
                'tokens_used': response.usage.input_tokens + response.usage.output_tokens,
                'model': model_name,
                'rate_limit': 'بر اساس طرح شما'
            }
            
            return JsonResponse({
                'success': True,
                'model': model_name,
                'usage': usage_info,
                'available_tokens': 'بر اساس طرح Anthropic'
            })
            
        else:
            return JsonResponse({
                'success': False,
                'error': 'این سرویس هنوز پیاده‌سازی نشده'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def retest_api_key(request):
    """تست مجدد API Key ذخیره شده"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        key_id = data.get('key_id')
        
        api_key = APIKey.objects.get(id=key_id, user=request.user)
        
        # اینجا می‌توانیم دوباره تست کنیم
        api_key.last_tested = timezone.now()
        api_key.save()
        
        return JsonResponse({'success': True})
        
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
        
        # دریافت API key
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
        
        # استفاده واقعی از AI
        try:
            if provider == 'openai':
                client = openai.OpenAI(api_key=api_key.key)
                response = client.chat.completions.create(
                    model=api_key.model_name,
                    messages=[{"role": "user", "content": message}]
                )
                
                content = response.choices[0].message.content
                usage = response.usage
                
                # ذخیره مصرف توکن
                TokenUsage.objects.create(
                    api_key=api_key,
                    prompt_tokens=usage.prompt_tokens,
                    completion_tokens=usage.completion_tokens,
                    total_tokens=usage.total_tokens
                )
                
                # آپدیت مصرف کل
                api_key.used_tokens += usage.total_tokens
                api_key.last_used = timezone.now()
                api_key.save()
                
            elif provider == 'claude':
                client = anthropic.Anthropic(api_key=api_key.key)
                response = client.messages.create(
                    model=api_key.model_name,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": message}]
                )
                
                content = response.content[0].text
                usage = response.usage
                
                # ذخیره مصرف توکن
                TokenUsage.objects.create(
                    api_key=api_key,
                    prompt_tokens=usage.input_tokens,
                    completion_tokens=usage.output_tokens,
                    total_tokens=usage.input_tokens + usage.output_tokens
                )
                
                # آپدیت مصرف کل
                api_key.used_tokens += (usage.input_tokens + usage.output_tokens)
                api_key.last_used = timezone.now()
                api_key.save()
                
            else:
                content = f"سرویس {provider} هنوز پیاده‌سازی نشده است."
                usage = None
            
            return JsonResponse({
                'success': True,
                'content': content,
                'usage': {
                    'prompt_tokens': usage.prompt_tokens if usage else 0,
                    'completion_tokens': usage.completion_tokens if usage else 0,
                    'total_tokens': usage.total_tokens if usage and hasattr(usage, 'total_tokens') else 0,
                    'total_used': api_key.used_tokens,
                    'remaining': api_key.remaining_tokens
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'خطا در ارتباط با {provider}: {str(e)}'
            })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def test_api_connection(request):
   """تست اتصال API"""
   if request.method != 'POST':
       return JsonResponse({'error': 'Method not allowed'}, status=405)
   
   try:
       data = json.loads(request.body)
       provider_id = data.get('provider')
       api_key = data.get('api_key')
       model_name = data.get('model_name')
       
       provider = AIProvider.objects.get(id=provider_id)
       
       # تست بر اساس نوع provider
       if provider.name == 'claude':
           import anthropic
           client = anthropic.Anthropic(api_key=api_key)
           # تست ساده
           response = client.messages.create(
               model=model_name,
               max_tokens=10,
               messages=[{"role": "user", "content": "Hi"}]
           )
           return JsonResponse({
               'success': True,
               'model': model_name,
               'available_tokens': 'نامحدود'
           })
           
       elif provider.name == 'openai':
           import openai
           client = openai.OpenAI(api_key=api_key)
           response = client.chat.completions.create(
               model=model_name,
               messages=[{"role": "user", "content": "Hi"}],
               max_tokens=10
           )
           return JsonResponse({
               'success': True,
               'model': model_name,
               'available_tokens': 'بر اساس طرح'
           })
           
       else:
           return JsonResponse({
               'success': False,
               'error': 'این سرویس هنوز پیاده‌سازی نشده'
           })
           
   except Exception as e:
       return JsonResponse({
           'success': False,
           'error': str(e)
       })

@login_required
def retest_api_key(request):
   """تست مجدد API Key ذخیره شده"""
   if request.method != 'POST':
       return JsonResponse({'error': 'Method not allowed'}, status=405)
   
   try:
       data = json.loads(request.body)
       key_id = data.get('key_id')
       
       api_key = APIKey.objects.get(id=key_id, user=request.user)
       
       # اینجا کد تست را اضافه کنید
       # فعلاً فقط وضعیت را آپدیت می‌کنیم
       api_key.last_tested = timezone.now()
       api_key.is_verified = True  # باید بر اساس نتیجه تست باشد
       api_key.save()
       
       return JsonResponse({'success': True})
       
   except APIKey.DoesNotExist:
       return JsonResponse({'error': 'API Key یافت نشد'}, status=403)
   except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)

@login_required
def test_api_connection(request):
   """تست اتصال API"""
   if request.method != 'POST':
       return JsonResponse({'error': 'Method not allowed'}, status=405)
   
   try:
       data = json.loads(request.body)
       provider_id = data.get('provider')
       api_key = data.get('api_key')
       model_name = data.get('model_name')
       
       provider = AIProvider.objects.get(id=provider_id)
       
       # تست بر اساس نوع provider
       if provider.name == 'claude':
           import anthropic
           client = anthropic.Anthropic(api_key=api_key)
           # تست ساده
           response = client.messages.create(
               model=model_name,
               max_tokens=10,
               messages=[{"role": "user", "content": "Hi"}]
           )
           return JsonResponse({
               'success': True,
               'model': model_name,
               'available_tokens': 'نامحدود'
           })
           
       elif provider.name == 'openai':
           import openai
           client = openai.OpenAI(api_key=api_key)
           response = client.chat.completions.create(
               model=model_name,
               messages=[{"role": "user", "content": "Hi"}],
               max_tokens=10
           )
           return JsonResponse({
               'success': True,
               'model': model_name,
               'available_tokens': 'بر اساس طرح'
           })
           
       else:
           return JsonResponse({
               'success': False,
               'error': 'این سرویس هنوز پیاده‌سازی نشده'
           })
           
   except Exception as e:
       return JsonResponse({
           'success': False,
           'error': str(e)
       })

@login_required
def retest_api_key(request):
   """تست مجدد API Key ذخیره شده"""
   if request.method != 'POST':
       return JsonResponse({'error': 'Method not allowed'}, status=405)
   
   try:
       data = json.loads(request.body)
       key_id = data.get('key_id')
       
       api_key = APIKey.objects.get(id=key_id, user=request.user)
       
       # اینجا کد تست را اضافه کنید
       # فعلاً فقط وضعیت را آپدیت می‌کنیم
       api_key.last_tested = timezone.now()
       api_key.is_verified = True  # باید بر اساس نتیجه تست باشد
       api_key.save()
       
       return JsonResponse({'success': True})
       
   except APIKey.DoesNotExist:
       return JsonResponse({'error': 'API Key یافت نشد'}, status=403)
   except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)
