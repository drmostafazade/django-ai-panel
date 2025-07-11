from django.urls import path
from . import views

app_name = 'git_integration'

urlpatterns = [
    path('repositories/', views.repositories_view, name='repositories'),
]
