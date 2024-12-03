
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils.crypto import get_random_string
from django.utils import timezone
from student.models import Student
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_authorized = models.BooleanField(default=False)
    login_token = models.CharField(max_length=6, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
       # Fields for user roles
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False) 

    # Set related_name to None to prevent reverse relationship creation
    groups = models.ManyToManyField(
        'auth.Group',
        related_name=None,
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name=None,
        blank=True
    )

    def __str__(self):
        return self.username



class PasswordUpdate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=64, unique=True, null=True, blank=True)  # Optional token
    new_password = models.CharField(max_length=255)  # Field to store the new password
    updated_at = models.DateTimeField(auto_now=True)  # Track when the password was updated

    def __str__(self):
        return f"Password update for {self.user.username}"

    def set_new_password(self):
        """Method to set the new password directly for the user."""
        if self.user and self.new_password:
            self.user.set_password(self.new_password)
            self.user.save()
            self.save()

    @staticmethod
    def generate_reset_token():
        """Generate a unique reset token."""
        return get_random_string(length=64)



        