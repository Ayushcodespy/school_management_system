from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class UserBase(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('school', 'School'),
    )

    user_id = models.CharField(max_length=20, unique=True, primary_key=True)  # e.g. STU2025001
    user_type = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    dob = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=128)  # hashed password
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=20, null=True, blank=True)  # ID of admin or school
    is_first_login = models.BooleanField(default=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(UserBase, self).save(*args, **kwargs)