from django.contrib import admin
from django.urls import path, include
from core.auth_views import login_view, logout_view, dashboard_view
from django.urls import path, include
urlpatterns = [
path('admin/', admin.site.urls),
path('', dashboard_view, name='home'),
path('dashboard/', dashboard_view, name='dashboard'),
path('auth/login/', login_view, name='login'),
path('auth/logout/', logout_view, name='logout'),
    path('git/', include('git_manager.urls', namespace='git_manager')),
]
