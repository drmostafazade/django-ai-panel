from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required # <-- THIS IS THE FIX
from django.views.decorators.http import require_POST
import json

from .services import generate_specialized_prompt

@login_required
@require_POST
def generate_prompt_view(request):
    try:
        data = json.loads(request.body)
        technology = data.get('technology')
        version = data.get('version', 'latest')
        result = generate_specialized_prompt(request.user, technology, version)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# Note: The admin views don't need to be in this file.
# They are handled by the admin classes themselves.
