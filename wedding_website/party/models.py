from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, PermissionsMixin
from .choices import *
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class GuestUserManager(BaseUserManager):
    """
    Custom manager for GuestUser without passwords.
    """
    def create_user(self, email, first_name, last_name, phone_number=None, knows=None, code =None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            knows=knows,
            code=code
        )
        user.set_unusable_password()  # No password for guests
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, phone_number=None, knows=None, code=None):
        if not password:
            raise ValueError("Superusers must have a password.")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            knows=knows,
            code=code,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)

class GuestUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone_number = models.CharField(default='1234566789', blank=True, null=True)
    knows = models.CharField(max_length=1, choices=picks)
    is_validated = models.BooleanField(default=False)
    code = models.CharField(null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'knows', 'code']

    objects = GuestUserManager()

    def __str__(self):
        return self.email
    

class invitation_info(models.Model):
    email = models.ForeignKey(GuestUser, on_delete=models.CASCADE, related_name="invitation")

    name = models.CharField(null=True)
    attend = models.BooleanField(default=False)
    party = models.BooleanField(default=False, help_text="Please check if you plan on staying for after party")
    group_type = models.CharField(max_length=20, choices=group_picks, null=True, blank=True)
    number_of_guests = models.IntegerField(null=True, blank=True)  # Number of guests (always required)
    guest_names = models.CharField(null=True, blank = True, help_text= "Please provide all first and last names seperated by comma(s)", )
    invite = models.BooleanField(default=False, help_text="Do you want a physical invitation?")
    
    def __str__(self):
        return f"Invitation for {self.email}"

