import json
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from .services import generate_specialized_prompt # We need to create/update this service

logger = logging.getLogger(__name__)

@staff_member_required
@require_POST
def generate_prompt_view(request):
    try:
        data = json.loads(request.body)
        technology = data.get('technology')
        version = data.get('version', '')
        custom_tech = data.get('custom_tech', '')
        api_key_id = data.get('api_key_id') # ID of the AI to use for generation

        final_tech = custom_tech if custom_tech else technology
        if not final_tech:
            return JsonResponse({'success': False, 'error': 'تکنولوژی انتخاب یا وارد نشده است.'}, status=400)
        
        if not api_key_id:
            return JsonResponse({'success': False, 'error': 'مدل هوش مصنوعی برای تولید پرامپت انتخاب نشده است.'}, status=400)

        # Pass all info to the service layer
        result = generate_specialized_prompt(request.user, final_tech, version, api_key_id)
        
        return JsonResponse(result)

    except Exception as e:
        logger.error(f"Error in generate_prompt_view: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': f'خطای داخلی سرور: {str(e)}'}, status=500)
