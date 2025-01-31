from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from .choices import *
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class GuestUserManager(BaseUserManager):
    """
    Custom manager for GuestUser without passwords.
    """
    def create_user(self, email, first_name, last_name, phone_number=None, knows=None):
        """
        Create and return a regular user without a password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            knows=knows
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number=None, knows=None):
        """
        Create and return a superuser without a password.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            knows=knows
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class guestuser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone_number = PhoneNumberField(default='+1234567890', blank=True, null=True)
    knows = models.CharField(max_length=1, choices=picks)
    is_validated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'knows']

    def __str__(self):
        return self.email
    

