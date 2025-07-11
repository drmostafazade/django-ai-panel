from django.urls import path
from . import views
from . import api_views
from . import api_views

urlpatterns = [
    path('', views.ai_chat, name='ai_chat'),
    path('settings/', views.api_settings, name='api_settings'),
]
    path('api/chat/', api_views.chat_api, name='chat_api'),
    path('api/chat/', api_views.chat_api, name='chat_api'),
