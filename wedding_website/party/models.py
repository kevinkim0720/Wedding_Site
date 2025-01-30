from django.db import models
from django.contrib.auth.models import AbstractUser, User
from .choices import *
from phonenumber_field.formfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    password = None
    is_staff = None
    is_superuser = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone_number = PhoneNumberField()
    knows = models.CharField(max_length=1, choices=picks)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'knows']
