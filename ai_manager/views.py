from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import AIProvider, APIKey
import json

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
       
       if provider_id and api_key:
           try:
               provider = AIProvider.objects.get(id=provider_id)
               APIKey.objects.update_or_create(
                   user=request.user,
                   provider=provider,
                   defaults={'key': api_key, 'is_active': True}
               )
               messages.success(request, f'کلید API {provider.get_name_display()} ذخیره شد.')
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
       
       # فعلاً پاسخ ساده
       return JsonResponse({
           'success': True,
           'content': f'دریافت شد: {message}\n\n(سرویس {provider} در حال توسعه است)',
           'usage': {'tokens': 0}
       })
       
   except Exception as e:
       return JsonResponse({'error': str(e)}, status=500)
