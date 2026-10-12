from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def student_required(view_func):
    """
    Decorator that ensures the authenticated user has the 'STUDENT' role.
    If unauthenticated, redirects to student login.
    If authenticated as Teacher, redirects with a permission warning.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in as a student to access this page.")
            return redirect('student_login')
        if request.user.role != 'STUDENT':
            messages.error(request, "Access Denied: This area is restricted to students only.")
            return redirect('teacher_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def teacher_required(view_func):
    """
    Decorator that ensures the authenticated user has the 'TEACHER' role.
    If unauthenticated, redirects to teacher login.
    If authenticated as Student, raises PermissionDenied (403) or redirects
    with an unauthorized error to protect teacher endpoints.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in as a teacher to access this portal.")
            return redirect('teacher_login')
        if request.user.role != 'TEACHER':
            messages.error(request, "Access Denied: You do not have teacher privileges.")
            # Raising PermissionDenied renders standard 403 page or handles security
            raise PermissionDenied("Access Denied: Student accounts cannot access the Teacher Dashboard.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
