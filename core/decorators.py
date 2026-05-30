from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

# Role-based decorators — each checks login status then role before allowing access

def homeowner_required(view_func):
    @wraps(view_func)  # preserves the original function name for debugging
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_homeowner():
            messages.error(request, 'Access denied. This area is for homeowners only.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_admin_user():
            messages.error(request, 'Access denied. This area is for admins only.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def technician_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_technician():
            messages.error(request, 'Access denied. This area is for technicians only.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
