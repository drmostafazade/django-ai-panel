import anthropic
from api_manager.models import APIKey

def generate_specialized_prompt(user, technology, version="latest"):
    try:
        claude_key = APIKey.objects.get(user=user, provider__name='claude', is_active=True)
        client = anthropic.Anthropic(api_key=claude_key.key)
        
        meta_prompt = f"""
        You are a world-class prompt engineer. Your task is to generate a comprehensive system prompt for another AI assistant.
        This assistant must become a super-specialist in: **{technology} (version: {version})**.
        Generate ONLY the system prompt text, without any introductory or concluding remarks.
        """
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620", max_tokens=1024,
            messages=[{"role": "user", "content": meta_prompt}]
        )
        return {"success": True, "prompt": message.content[0].text}
    except APIKey.DoesNotExist:
        return {"success": False, "error": "A valid, active Claude API key is required to use this feature."}
    except Exception as e:
        return {"success": False, "error": str(e)}
