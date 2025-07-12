from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('', include('users.urls')),
    path('ai-chat/', include('ai_chat.urls')),
    # The URL for the API manager starts with 'api-manager/'
    path('api-manager/', include('api_manager.urls')),
]
