import time
from django.shortcuts import redirect

def require_validation(view_func):
    def wrapper(request, *args, **kwargs):
        last_validated = request.session.get("last_validated")

        if not last_validated or (time.time() - last_validated > 1800):  # 30 minutes
            request.session.pop("last_validated", None)  # Remove expired validation
            return redirect("home")  # Redirect to home page for re-validation

        return view_func(request, *args, **kwargs)
    return wrapper
