from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

EXCLUDED_PATHS = ['/home/', '/', '/faq/', '/info_form/', '/validation/']

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_path = request.path

        # If user is NOT authenticated and trying to access a PROTECTED page, redirect to validation
        if not request.user.is_authenticated and current_path not in EXCLUDED_PATHS:
            return redirect(settings.LOGIN_URL)  # Redirect to validation page

        return self.get_response(request)