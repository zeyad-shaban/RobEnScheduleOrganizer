from django.shortcuts import redirect
from functools import wraps

def anonymous_required(redirect_to=None):
    def decorator(view_function):
        @wraps(view_function)
        def _wrapped_view_function(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to or 'home')  # Redirect to the home page or any other page
            return view_function(request, *args, **kwargs)
        return _wrapped_view_function
    return decorator
