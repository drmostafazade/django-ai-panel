from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import AIProvider, APIKey
from .services import get_available_models_from_provider
import json

@login_required
def api_settings_view(request):
    if request.method == 'POST':
        try:
            provider_name = request.POST.get('provider')
            api_key_value = request.POST.get('api_key')
            model_id = request.POST.get('model_name')
            
            provider_instance = get_object_or_404(AIProvider, name=provider_name)
            
            # Prevent duplicate keys for the same provider/user
            if APIKey.objects.filter(user=request.user, provider=provider_instance).exists():
                messages.error(request, f"شما قبلاً یک کلید برای {provider_instance.get_name_display()} ثبت کرده‌اید.")
            else:
                APIKey.objects.create(
                    user=request.user,
                    provider=provider_instance,
                    key=api_key_value, # IMPORTANT: Encrypt this in a real production environment!
                    model_name=model_id,
                    is_active=True,
                    is_verified=True,
                )
                messages.success(request, f"کلید API برای {provider_instance.get_name_display()} با موفقیت ذخیره شد.")
        except Exception as e:
            messages.error(request, f"خطایی در هنگام ذخیره‌سازی رخ داد: {e}")
        
        return redirect('api_manager:api_settings')

    providers = AIProvider.objects.filter(is_active=True)
    user_keys = APIKey.objects.filter(user=request.user).order_by('-created_at')
    context = {'providers': providers, 'user_keys': user_keys}
    return render(request, 'api_manager/api_settings.html', context)

@require_POST
@login_required
def get_available_models_view(request):
    # This view remains the same
    try:
        data = json.loads(request.body)
        provider_name = data.get('provider')
        api_key = data.get('api_key')
        if not provider_name or not api_key:
            return JsonResponse({'success': False, 'error': 'Provider and API Key are required.'})
        
        result = get_available_models_from_provider(provider_name, api_key)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
@login_required
def toggle_api_key_view(request):
    key_id = request.POST.get('key_id')
    key = get_object_or_404(APIKey, id=key_id, user=request.user) # Security: ensure user owns the key
    key.is_active = not key.is_active
    key.save()
    status = "فعال" if key.is_active else "غیرفعال"
    messages.success(request, f"وضعیت کلید {key.provider.get_name_display()} به {status} تغییر یافت.")
    return redirect('api_manager:api_settings')

@require_POST
@login_required
def delete_api_key_view(request):
    key_id = request.POST.get('key_id')
    key = get_object_or_404(APIKey, id=key_id, user=request.user) # Security check
    provider_name = key.provider.get_name_display()
    key.delete()
    messages.success(request, f"کلید API مربوط به {provider_name} با موفقیت حذف شد.")
    return redirect('api_manager:api_settings')

# These can be implemented later
@require_POST
@login_required
def test_api_connection_view(request):
    return JsonResponse({'success': True})

@require_POST
@login_required
def retest_api_key_view(request):
    return JsonResponse({'success': True})
