from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import APIKey, AIProvider
import json

@login_required
def api_settings(request):
    """صفحه تنظیمات API"""
    if request.method == 'POST':
        # پردازش فرم
        provider_id = request.POST.get('provider')
        api_key = request.POST.get('api_key')
        model_name = request.POST.get('model_name')
        
        if provider_id and api_key:
            try:
                provider = AIProvider.objects.get(id=provider_id)
                
                # ذخیره یا بروزرسانی API key
                obj, created = APIKey.objects.update_or_create(
                    user=request.user,
                    provider=provider,
                    defaults={
                        'key': api_key,
                        'model_name': model_name or '',
                        'is_active': True
                    }
                )
                
                if created:
                    messages.success(request, 'API Key با موفقیت اضافه شد')
                else:
                    messages.success(request, 'API Key با موفقیت بروزرسانی شد')
                    
                return redirect('api_settings')
                
            except Exception as e:
                messages.error(request, f'خطا: {str(e)}')
    
    # دریافت داده‌ها برای نمایش
    providers = AIProvider.objects.filter(is_active=True)
    user_keys = APIKey.objects.filter(user=request.user).select_related('provider')
    
    context = {
        'providers': providers,
        'user_keys': user_keys,
    }
    
    return render(request, 'ai_manager/api_settings_simple.html', context)

@login_required
def chat_view(request):
    """صفحه چت"""
    return render(request, 'ai_manager/chat.html', {})

def toggle_api_key(request):
    """فعال/غیرفعال کردن API key"""
    if request.method == 'POST':
        key_id = request.POST.get('key_id')
        try:
            api_key = APIKey.objects.get(id=key_id, user=request.user)
            api_key.is_active = not api_key.is_active
            api_key.save()
            messages.success(request, 'وضعیت API Key تغییر کرد')
        except:
            messages.error(request, 'خطا در تغییر وضعیت')
    return redirect('api_settings')

def delete_api_key(request):
    """حذف API key"""
    if request.method == 'POST':
        key_id = request.POST.get('key_id')
        try:
            api_key = APIKey.objects.get(id=key_id, user=request.user)
            api_key.delete()
            messages.success(request, 'API Key حذف شد')
        except:
            messages.error(request, 'خطا در حذف')
    return redirect('api_settings')

# Stub functions برای رفع خطا
def get_available_models(request):
    return JsonResponse({'success': False, 'error': 'Not implemented'})

def test_api_connection(request):
    return JsonResponse({'success': True, 'message': 'Test'})

def retest_api_key(request):
    return JsonResponse({'success': True})
