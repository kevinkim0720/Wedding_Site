# party/backends.py

from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist
from .models import GuestUser

class EmailAuthBackend(BaseBackend):
    """
    Custom authentication backend to authenticate users by their email.
    """
    def authenticate(self, request, email=None):
        try:
            # Try to find the user by email
            user = GuestUser.objects.get(email=email)
            # You can add other logic for validation if needed
            if user.is_validated:
                return user
            else:
                return None  # Or raise an error if user is not validated
        except ObjectDoesNotExist:
            return None  # No user found with this email

    def get_user(self, user_id):
        try:
            return GuestUser.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None
