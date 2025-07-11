from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'خوش آمدید {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
    
    return render(request, 'auth/login.html')

@login_required
def dashboard_view(request):
    context = {
        'repo_count': Repository.objects.filter(user=request.user).count(),
        'has_token': GitHubToken.objects.filter(user=request.user).exists(),
    }
    return render(request, 'dashboard/home.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, 'با موفقیت خارج شدید.')
    return redirect('login')
