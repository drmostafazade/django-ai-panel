from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def ai_chat(request):
    """صفحه اصلی چت AI"""
    return render(request, 'ai_manager/chat.html', {
        'title': 'چت با هوش مصنوعی'
    })

@login_required
def api_settings(request):
    """مدیریت API Keys"""
    return render(request, 'ai_manager/api_settings.html', {
        'title': 'تنظیمات API'
    })

from django.utils import timezone

@login_required
def save_api_key(request):
    """ذخیره API Key"""
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
            except AIProvider.DoesNotExist:
                messages.error(request, 'سرویس نامعتبر.')
                
        return redirect('api_settings')
    
    return redirect('api_settings')

from django.utils import timezone

@login_required
def save_api_key(request):
    """ذخیره API Key"""
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
            except AIProvider.DoesNotExist:
                messages.error(request, 'سرویس نامعتبر.')
                
        return redirect('api_settings')
    
    return redirect('api_settings')
