from django.urls import path
from . import views

app_name = 'git_integration'

urlpatterns = [
    path('settings/', views.git_settings_view, name='git_settings'),
    path('repositories/', views.repositories_view, name='repositories'),
]
