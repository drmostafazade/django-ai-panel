from django.urls import path
from . import views

urlpatterns = [
    # صفحات اصلی
    path('', views.ai_chat, name='ai_chat'),
    path('settings/', views.api_settings, name='api_settings'),
    
    # API endpoints
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/active-keys/', views.get_active_keys_api, name='get_active_keys_api'),
    path('get-models/', views.get_available_models, name='get_available_models'),
    path('test-connection/', views.test_api_connection, name='test_api_connection'),
    path('retest-key/', views.retest_api_key, name='retest_api_key'),
    
    # مدیریت API Keys
    path('toggle-key/', views.toggle_api_key, name='toggle_api_key'),
    path('delete-key/', views.delete_api_key, name='delete_api_key'),
    path('balance/<int:key_id>/', views.get_balance, name='get_balance'),
    path('personal/<int:key_id>/', views.personal_settings, name='personal_settings'),
    path('add-prompt/<int:key_id>/', views.add_prompt, name='add_prompt'),
]

# Import test_buttons view if exists
try:
    from .test_buttons import test_buttons_view
    urlpatterns.append(path('test-buttons/', test_buttons_view, name='test_buttons'))
except ImportError:
    pass
