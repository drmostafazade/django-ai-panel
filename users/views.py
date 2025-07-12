from django.shortcuts import render, redirect; from django.contrib.auth import authenticate, login, logout; from django.contrib.auth.forms import AuthenticationForm; from django.contrib import messages
def login_view(request):
    if request.user.is_authenticated: return redirect('dashboard:home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user(); login(request, user); return redirect('dashboard:home')
        else: messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else: form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})
def logout_view(request): logout(request); return redirect('users:login')
