from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from userman.taxonomies import UserRole
from utils.managers import AppUserManagerQuerySet
from utils.models import BaseModel

# Create your models here.


class User(PermissionsMixin, AbstractBaseUser, BaseModel):
    """Custom User model"""

    # config fields
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # custom manager
    objects = AppUserManagerQuerySet.as_manager()

    # Fields
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    role = models.PositiveSmallIntegerField(
        choices=UserRole.choices, default=UserRole.customer
    )
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def can_access_admin_panel(self):
        """Check if user can access admin panel."""

        return self.role == UserRole.admin
