from django.urls import path
from . import views

# This ensures the namespace is correctly set to 'api_manager'
app_name = 'api_manager'

urlpatterns = [
    path('settings/', views.api_settings_view, name='api_settings'),
    # --- The rest of your URLs ---
    path('get-models/', views.get_available_models_view, name='get_available_models'),
    path('test-connection/', views.test_api_connection_view, name='test_api_connection'),
    path('toggle-key/', views.toggle_api_key_view, name='toggle_api_key'),
    path('delete-key/', views.delete_api_key_view, name='delete_api_key'),
    path('retest-key/', views.retest_api_key_view, name='retest_api_key'),
]
