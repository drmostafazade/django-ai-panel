import openai
import anthropic
import google.generativeai as genai
from .models import AIProvider

def get_available_models_from_provider(provider_name, api_key):
    """
    Connects to the actual AI provider and fetches a list of available models.
    """
    try:
        if provider_name == 'openai':
            client = openai.OpenAI(api_key=api_key)
            models = client.models.list()
            model_list = [{"id": model.id, "name": model.id} for model in models.data if "gpt" in model.id]
            account_info = {"api_key_valid": True}
            return {"success": True, "models": model_list, "account_info": account_info}

        elif provider_name == 'claude':
            # Anthropic SDK doesn't have a public models.list() equivalent.
            # We list the most common ones manually.
            model_list = [
                {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus"},
                {"id": "claude-3-5-sonnet-20240620", "name": "Claude 3.5 Sonnet"},
                {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku"},
            ]
            # We can do a small test call to validate the key
            client = anthropic.Anthropic(api_key=api_key)
            client.messages.create(model="claude-3-haiku-20240307", max_tokens=1, messages=[{"role": "user", "content": "test"}])
            return {"success": True, "models": model_list, "account_info": {"api_key_valid": True}}

        # Add other providers here later...
        else:
            return {"success": False, "error": "Provider not yet implemented in services."}

    except Exception as e:
        return {"success": False, "error": str(e)}

# This is a placeholder for now, can be implemented later
def test_api_connection_service(provider, api_key, model_name):
    return {"success": True, "model": model_name}
