from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GitHubToken, Repository
import requests

@login_required
def git_settings(request):
    token = None
    try:
        token = GitHubToken.objects.filter(user=request.user).first()
    except:
        pass
    
    if request.method == 'POST':
        github_token = request.POST.get('token', '')
        if github_token and not github_token.startswith('•'):
            if token:
                token.token = github_token
                token.save()
            else:
                GitHubToken.objects.create(
                    user=request.user,
                    token=github_token
                )
            messages.success(request, 'توکن با موفقیت ذخیره شد!')
            return redirect('git_integration:settings')
    
    return render(request, 'git_integration/settings.html', {
        'token': token,
        'title': 'تنظیمات GitHub'
    })

@login_required
def repositories_list(request):
    if request.method == 'POST' and 'sync' in request.POST:
        try:
            token = GitHubToken.objects.filter(user=request.user).first()
            if token:
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
                            }
                        )
                        count += 1
                    messages.success(request, f'{count} مخزن همگام‌سازی شد!')
                else:
                    messages.error(request, 'خطا در دریافت مخازن')
            else:
                messages.error(request, 'ابتدا توکن GitHub را تنظیم کنید')
                return redirect('git_integration:settings')
        except Exception as e:
            messages.error(request, f'خطا: {str(e)}')
    
    repos = Repository.objects.filter(user=request.user).order_by('name')
    return render(request, 'git_integration/repositories.html', {
        'repos': repos,
        'title': 'مخازن من'
    })
