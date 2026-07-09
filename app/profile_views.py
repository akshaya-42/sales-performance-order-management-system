from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from app.models import UserProfile
from app.forms import UserUpdateForm, ProfileUpdateForm
from app.decorators import admin_required


@login_required
def profile_views(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


@login_required
def profile_edit(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=profile)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    return render(request, 'edit.html', {'u_form': u_form, 'p_form': p_form})


@admin_required
def user_list(request):
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    return render(request, 'user_list.html', {'users': users})


@admin_required
def change_user_role(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        role = request.POST.get('role')
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if role in ['admin', 'staff', 'user']:
            profile.role = role
            profile.save()
            messages.success(request, f"Role updated for {user.username}.")
    return redirect('user_list')