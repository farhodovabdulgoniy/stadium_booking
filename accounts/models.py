from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
    ('Admin', 'Admin'),
    ('Owner', 'Owner'),
    ('User', 'User'),
)

class CustomUser(AbstractUser):
    role = models.CharField(max_length=255, choices=ROLES, default='User')

    def __str__(self):
        return self.username
    