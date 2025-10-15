from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES=(
        ('admin','Admin'),
        ('teacher','Teacher'),
        ('student','Student'),
        ('parent','Parent')
    )
    role=models.CharField(max_length=10,choices=ROLE_CHOICES)

