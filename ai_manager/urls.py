from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('settings/', views.api_settings, name='api_settings'),
    path('get-available-models/', views.get_available_models, name='get_available_models'),
    path('test-connection/', views.test_api_connection, name='test_api_connection'),
    path('toggle-api-key/', views.toggle_api_key, name='toggle_api_key'),
    path('delete-api-key/', views.delete_api_key, name='delete_api_key'),
    path('retest-api-key/', views.retest_api_key, name='retest_api_key'),
]
    # API endpoints
    path('api/token-balance/<int:key_id>/', views.get_token_balance, name='get_token_balance'),
    path('api/test-connection/<int:key_id>/', views.test_api_connection, name='test_api_connection'),
    path('api/personal-settings/<int:key_id>/', views.personal_settings_view, name='personal_settings'),
    path('api/prompt-manager/<int:key_id>/', views.prompt_manager_view, name='prompt_manager'),
    path('api/key-details/<int:key_id>/', views.key_details_view, name='key_details'),
