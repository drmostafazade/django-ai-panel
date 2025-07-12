from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views
from dashboard.auth_views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('git/', views.git_view, name='git'),
    path('terminal/', views.terminal_view, name='terminal'),
    path('ai/', views.ai_view, name='ai'),
#    path('ai-chat/', include('ai_manager.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
