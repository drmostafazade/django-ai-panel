from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GitHubToken, Repository

@login_required
def git_settings(request):
    try:
        token = GitHubToken.objects.get(user=request.user)
    except GitHubToken.DoesNotExist:
        token = None
    
    if request.method == 'POST':
        github_token = request.POST.get('github_token')
        if github_token:
            if token:
                token.token = github_token
                token.save()
            else:
                token = GitHubToken.objects.create(
                    user=request.user,
                    token=github_token
                )
            messages.success(request, 'توکن GitHub با موفقیت ذخیره شد')
            return redirect('git_settings')
    
    return render(request, 'git_manager/settings.html', {'token': token})

@login_required
def repositories_list(request):
    repos = Repository.objects.filter(user=request.user)
    return render(request, 'git_manager/repositories.html', {'repos': repos})
