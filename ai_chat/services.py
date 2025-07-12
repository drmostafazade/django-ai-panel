import openai
# Other imports will be added here later

def get_ai_response(key_instance, system_prompt, user_message):
    """
    Dispatcher function that calls the correct AI provider based on the APIKey instance.
    """
    provider_name = key_instance.provider.name
    api_key = key_instance.key
    model_name = key_instance.model_name
    
    try:
        if provider_name == 'openai':
            client = openai.OpenAI(api_key=api_key)
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            return {"success": True, "content": completion.choices[0].message.content}
        # Add other providers (claude, gemini) here later...
        else:
            return {"success": False, "error": f"Provider '{provider_name}' not implemented yet."}
    except Exception as e:
        return {"success": False, "error": f"API Error for {provider_name}: {str(e)}"}
