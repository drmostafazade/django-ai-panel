from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GitHubTokenForm
from .models import GitHubToken, Repository
import requests

@login_required
def git_settings(request):
    try:
        token = GitHubToken.objects.get(user=request.user)
    except GitHubToken.DoesNotExist:
        token = None
    
    if request.method == 'POST':
        form = GitHubTokenForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'توکن با موفقیت ذخیره شد!')
            return redirect('git_integration:settings')
    else:
        form = GitHubTokenForm()
    
    return render(request, 'git_integration/settings.html', {
        'form': form,
        'token': token,
        'title': 'تنظیمات GitHub'
    })

@login_required
def repositories_list(request):
    if request.method == 'POST' and 'sync' in request.POST:
        try:
            token = GitHubToken.objects.get(user=request.user)
            headers = {'Authorization': f'token {token.token}'}
            response = requests.get('https://api.github.com/user/repos', headers=headers)
            
            if response.status_code == 200:
                repos = response.json()
                count = 0
                for repo in repos:
                    Repository.objects.update_or_create(
                        user=request.user,
                        name=repo['name'],
                        defaults={
                            'full_name': repo['full_name'],
                            'description': repo.get('description', ''),
                            'html_url': repo['html_url'],
                        }
                    )
                    count += 1
                messages.success(request, f'{count} مخزن همگام‌سازی شد!')
            else:
                messages.error(request, 'خطا در دریافت مخازن')
        except GitHubToken.DoesNotExist:
            messages.error(request, 'ابتدا توکن GitHub را تنظیم کنید')
            return redirect('git_integration:settings')
    
    repos = Repository.objects.filter(user=request.user).order_by('-is_active', 'name')
    return render(request, 'git_integration/repositories.html', {
        'repos': repos,
        'title': 'مخازن من'
    })
