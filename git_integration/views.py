from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def git_settings(request):
    return render(request, 'git_integration/settings.html', {})

@login_required
def repositories_list(request):
    return render(request, 'git_integration/repositories.html', {'repos': []})
