from django.urls import path
from . import views

app_name = 'git_integration'

urlpatterns = [
    path('settings/', views.git_settings, name='settings'),
    path('repositories/', views.repositories_list, name='repositories'),
]
