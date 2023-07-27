from django.contrib.auth.models import AbstractUser
from django.db import models
from users.constants import UserRole


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        max_length=100,
    )
