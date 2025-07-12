from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.cache import cache
import json

# Import the settings model from our core app
from core.models import AIProviderSetting

# Import AI libraries
import openai
import anthropic
import google.generativeai as genai

# --- Specific Functions for Each AI Provider ---

def _get_openai_response(api_key, system_prompt, user_message):
    try:
        client = openai.OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-4o",  # Or another model like "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return {
            "success": True,
            "content": completion.choices[0].message.content,
            "usage": {
                "input_tokens": completion.usage.prompt_tokens,
                "output_tokens": completion.usage.completion_tokens,
            }
        }
    except Exception as e:
        return {"success": False, "error": f"OpenAI API Error: {str(e)}"}

def _get_claude_response(api_key, system_prompt, user_message):
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return {
            "success": True,
            "content": message.content[0].text,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
            }
        }
    except Exception as e:
        return {"success": False, "error": f"Anthropic API Error: {str(e)}"}

def _get_gemini_response(api_key, system_prompt, user_message):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            system_instruction=system_prompt
        )
        response = model.generate_content(user_message)
        return {
            "success": True,
            "content": response.text,
            "usage": None  # Token usage is not as straightforward to get in this SDK version
        }
    except Exception as e:
        return {"success": False, "error": f"Google Gemini API Error: {str(e)}"}

# --- Main Dispatcher Function ---

def get_ai_response(provider, api_key, system_prompt, user_message):
    """Dispatcher function to call the correct AI provider."""
    if provider == 'openai':
        return _get_openai_response(api_key, system_prompt, user_message)
    elif provider == 'claude':
        return _get_claude_response(api_key, system_prompt, user_message)
    elif provider == 'gemini':
        return _get_gemini_response(api_key, system_prompt, user_message)
    else:
        return {"success": False, "error": f"Unknown provider: {provider}"}


# --- Django Views ---

def chat_view(request):
    """Renders the main chat page."""
    active_providers = AIProviderSetting.objects.filter(is_active=True)
    return render(request, 'ai_chat/chat.html', {'providers': active_providers})

class ChatAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            provider_name = data.get('provider')

            if not user_message or not provider_name:
                return JsonResponse({'error': 'Message and provider are required.'}, status=400)

            provider_setting = AIProviderSetting.objects.filter(provider=provider_name, is_active=True).first()
            if not provider_setting:
                return JsonResponse({'error': f"Provider '{provider_name}' is not configured or is inactive."}, status=400)
            
            api_key = provider_setting.api_key

            project_schema = cache.get('project_db_schema', {})
            schema_json = json.dumps(project_schema, indent=2)
            
            system_prompt = (
                "You are an expert Django developer assistant named 'PanelAI'. "
                "You are working inside a Django project. Use the following database schema for context:\n\n"
                f"```json\n{schema_json}\n```\n\n"
                "Provide accurate, helpful answers related to this project. Format code snippets correctly using markdown."
            )

            # This now calls our real AI dispatcher function
            response_data = get_ai_response(provider_name, api_key, system_prompt, user_message)

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)
