from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.api_settings_test, name='api_settings_test'),
    path('', views.chat_view, name='chat'),
    path('settings/', views.api_settings, name='api_settings'),
    path('get-available-models/', views.get_available_models, name='get_available_models'),
    path('test-connection/', views.test_api_connection, name='test_api_connection'),
    path('toggle-api-key/', views.toggle_api_key, name='toggle_api_key'),
    path('delete-api-key/', views.delete_api_key, name='delete_api_key'),
    path('retest-api-key/', views.retest_api_key, name='retest_api_key'),
]
