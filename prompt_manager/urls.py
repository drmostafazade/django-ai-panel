from django.urls import path
from . import views
app_name = 'prompt_manager'
from django.contrib.admin.views.decorators import staff_member_required
urlpatterns = [
    path('generate-prompt/', staff_member_required(views.generate_prompt_view), name='generate_prompt'),
]
