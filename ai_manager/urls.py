from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_chat, name='ai_chat'),
    path('settings/', views.api_settings, name='api_settings'),
    path('api/chat/', views.chat_api, name='chat_api'),
]
