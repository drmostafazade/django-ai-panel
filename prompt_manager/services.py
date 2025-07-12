# This is the corrected and final version of the service file.
import openai
import anthropic
from api_manager.models import APIKey

def generate_specialized_prompt(user, technology, version, api_key_id):
    try:
        # Use the specific API key selected by the user
        generation_key = APIKey.objects.get(id=api_key_id, user=user, is_active=True)
        provider_name = generation_key.provider.name
        api_key_value = generation_key.key

        meta_prompt = f"Generate a comprehensive, expert-level system prompt for an AI assistant specializing in: **{technology} (version: {version or 'latest'})**. Output ONLY the prompt text, without any other text."
        
        response_text = ""

        if provider_name == 'openai':
            client = openai.OpenAI(api_key=api_key_value)
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo", # Using a faster model for this task
                messages=[{"role": "user", "content": meta_prompt}]
            )
            response_text = completion.choices[0].message.content
        
        elif provider_name == 'claude':
            client = anthropic.Anthropic(api_key=api_key_value)
            message = client.messages.create(
                model="claude-3-haiku-20240307", # Using a faster model
                max_tokens=1024,
                messages=[{"role": "user", "content": meta_prompt}]
            )
            response_text = message.content[0].text
        
        else:
             return {"success": False, "error": f"Provider '{provider_name}' is not supported for prompt generation yet."}

        return {"success": True, "prompt": response_text}

    except APIKey.DoesNotExist:
        return {"success": False, "error": "کلید API انتخاب شده برای تولید پرامپت معتبر یا فعال نیست."}
    except Exception asش e:
        # This will catch the 401 error from OpenAI and return it to the user
        return {"success": False, "error": str(e)}
