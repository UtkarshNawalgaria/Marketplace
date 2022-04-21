from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from marketplace.core.models import BaseModel
from marketplace.users.manager import UserManager


class User(PermissionsMixin, AbstractBaseUser, BaseModel):
    """Default user for My Marketplace."""

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("User email"), max_length=255, unique=True)
    phone = models.CharField(
        _("User Phone Number"), max_length=10, unique=True, null=True
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"User - {self.email}"

    def get_absolute_url(self):
        """
        Get url for user's detail view.

        Returns:
        - str: URL for user detail.

        """
        return reverse("user:detail", kwargs={"id": self.id})


class Customer(BaseModel):
    """
    User proxy model for customer
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
