from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GitHubToken, Repository
import requests

@login_required
def git_settings(request):
    token = GitHubToken.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        github_token = request.POST.get('token', '')
        if github_token and not github_token.startswith('توکن'):
            if token:
                token.token = github_token
                token.save()
            else:
                GitHubToken.objects.create(user=request.user, token=github_token)
            messages.success(request, 'توکن با موفقیت ذخیره شد!')
            return redirect('git_integration:settings')
    
    return render(request, 'git_integration/settings.html', {
        'token': token,
        'title': 'تنظیمات GitHub'
    })

@login_required
def repositories_list(request):
    if request.method == 'POST' and 'sync' in request.POST:
        token = GitHubToken.objects.filter(user=request.user).first()
        if not token:
            messages.error(request, 'ابتدا توکن GitHub را تنظیم کنید')
            return redirect('git_integration:settings')
        
        try:
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
                            'html_url': repo.get('html_url', ''),
                        }
                    )
                    count += 1
                messages.success(request, f'{count} مخزن همگام‌سازی شد!')
            else:
                messages.error(request, f'خطا در دریافت مخازن: {response.status_code}')
        except Exception as e:
            messages.error(request, f'خطا: {str(e)}')
    
    # تغییر وضعیت فعال/غیرفعال
    if request.method == 'POST' and 'toggle' in request.POST:
        repo_id = request.POST.get('repo_id')
        try:
            repo = Repository.objects.get(id=repo_id, user=request.user)
            repo.is_active = not repo.is_active
            repo.save()
            status = "فعال" if repo.is_active else "غیرفعال"
            messages.success(request, f'مخزن {repo.name} {status} شد')
        except Repository.DoesNotExist:
            messages.error(request, 'مخزن یافت نشد')
    
    repos = Repository.objects.filter(user=request.user).order_by('-is_active', 'name')
    return render(request, 'git_integration/repositories.html', {
        'repos': repos,
        'title': 'مخازن من'
    })
