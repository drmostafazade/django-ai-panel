from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'خوش آمدید!')
            return redirect('dashboard')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'با موفقیت خارج شدید')
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard/home.html')
