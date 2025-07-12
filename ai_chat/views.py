from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.core.cache import cache
import json

from api_manager.models import APIKey
from prompt_manager.models import PersonalizationProfile, PromptTemplate
from .services import get_ai_response

@login_required
def chat_view(request):
    active_keys = APIKey.objects.filter(user=request.user, is_active=True).select_related('provider')
    profiles = PersonalizationProfile.objects.filter(user=request.user, is_active=True)
    templates = PromptTemplate.objects.filter(user=request.user, is_active=True)
    
    context = {
        'api_keys': active_keys,
        'profiles': profiles,
        'templates': templates,
    }
    return render(request, 'ai_chat/chat.html', context)

class ChatAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            api_key_id = data.get('api_key_id')
            profile_id = data.get('profile_id')
            template_id = data.get('template_id')

            if not user_message or not api_key_id:
                return JsonResponse({'error': 'Message and API Key selection are required.'}, status=400)

            key_instance = APIKey.objects.get(id=api_key_id, user=request.user, is_active=True)
            
            # Use default schema if no profile is selected
            system_prompt = json.dumps(cache.get('project_db_schema', {}), indent=2)
            if profile_id:
                profile = PersonalizationProfile.objects.get(id=profile_id, user=request.user)
                system_prompt = profile.system_prompt
            
            final_user_message = user_message
            if template_id:
                template = PromptTemplate.objects.get(id=template_id, user=request.user)
                final_user_message = template.template_text.replace("{{user_message}}", user_message)

            response_data = get_ai_response(
                provider_name=key_instance.provider.name,
                api_key=key_instance.key,
                model_name=key_instance.model_name,
                system_prompt=system_prompt,
                user_message=final_user_message
            )
            return JsonResponse(response_data)

        except APIKey.DoesNotExist:
            return JsonResponse({'error': 'Invalid or inactive API Key selected.'}, status=403)
        except Exception as e:
            return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)
