from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def ai_chat(request):
    """صفحه اصلی چت AI"""
    return render(request, 'ai_manager/chat.html', {
        'title': 'چت با هوش مصنوعی'
    })

@login_required
def api_settings(request):
    """مدیریت API Keys"""
    return render(request, 'ai_manager/api_settings.html', {
        'title': 'تنظیمات API'
    })
