from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    context = {
        'stats': {
            'projects': 12,
            'commits': 347,
            'issues': 23,
            'users': 5
        }
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def git_view(request):
    return render(request, 'dashboard/git.html')

@login_required
def terminal_view(request):
    return render(request, 'dashboard/terminal.html')

@login_required
def ai_view(request):
    return render(request, 'dashboard/ai.html')
