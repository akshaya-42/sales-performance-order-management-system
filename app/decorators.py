from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def staff_required(views_func):
    @wraps(views_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        try:
            profile = request.user.profile
            if profile.role in ['admin', 'staff'] or request.user.is_superuser:
                return views_func(request, *args, **kwargs)
        except Exception:
            if request.user.is_superuser:
                return views_func(request, *args, **kwargs)
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('/dashboard')
    return wrapper


def admin_required(views_func):
    @wraps(views_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login')
        try:
            profile = request.user.profile
            if profile.role == 'admin' or request.user.is_superuser:
                return views_func(request, *args, **kwargs)
        except Exception:
            if request.user.is_superuser:
                return views_func(request, *args, **kwargs)
        messages.error(request, "Admin access required.")
        return redirect('/dashboard')
    return wrapper