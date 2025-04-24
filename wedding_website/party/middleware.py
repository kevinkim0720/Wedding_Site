from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve
from django.contrib import messages

GUEST_ALLOWED_PREFIXES = (
    '/', '/home', '/faq', '/info_form', '/validation', '/check-session', '/favicon.ico', '/static', '/media'
)

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_path = request.path
        # print(f"🔍 Middleware hit: {current_path} | Authenticated: {request.user.is_authenticated}")

        if not request.user.is_authenticated and not current_path.startswith(GUEST_ALLOWED_PREFIXES):
            # print(f"⛔ Redirecting {current_path} to {settings.LOGIN_URL}")
            messages.warning(request, "Session expired. Please validate again.")
            return redirect('/validation/')

        return self.get_response(request)