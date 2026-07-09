from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.forms import RegisterForm, CustomPasswordChangeForm
from app.models import UserProfile


def login_views(request):
    if request.user.is_authenticated:
        return redirect('dashboard_views')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect(request.GET.get('next', 'dashboard'))
        messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def logout_views(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


def register_views(request):
    if request.user.is_authenticated:
        return redirect('dashboard_views')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='user')
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
    return render(request, 'register.html', {'form': form})


@login_required
def change_password_views(request):
    form = CustomPasswordChangeForm(request.user)
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('profile')
    return render(request, 'change_password.html', {'form': form})