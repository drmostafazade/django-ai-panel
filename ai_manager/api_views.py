from django.utils import timezone
from .models import AIProvider, APIKey
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import APIKey
from .services import get_ai_service

@login_required
@csrf_exempt
def chat_api(request):
    """API endpoint for AI chat"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        message = data.get('message')
        provider = data.get('provider', 'claude')
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # دریافت API key کاربر
        try:
            api_key = APIKey.objects.get(
                user=request.user,
                provider__name=provider,
                is_active=True
            )
        except APIKey.DoesNotExist:
            return JsonResponse({
                'error': f'No active API key found for {provider}'
            }, status=400)
        
        # ارسال پیام به AI
        service = get_ai_service(provider, api_key)
        result = service.send_message(message)
        
        # بروزرسانی last_used
        api_key.last_used = timezone.now()
        api_key.save()
        
        return JsonResponse(result)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
