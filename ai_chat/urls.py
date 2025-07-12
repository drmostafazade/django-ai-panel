from django.urls import path
from .views import chat_view, ChatAPIView

app_name = 'ai_chat'

urlpatterns = [
    path('', chat_view, name='chat'),
    path('api/', ChatAPIView.as_view(), name='chat_api'),
]
