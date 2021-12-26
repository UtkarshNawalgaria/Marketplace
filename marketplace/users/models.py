from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from marketplace.core.models import BaseModel
from marketplace.users.manager import UserManager


class User(PermissionsMixin, AbstractBaseUser, BaseModel):
    """Default user for My Marketplace."""

    class UserType(models.TextChoices):
        SELLER = ("Seller", "SELLER")
        CUSTOMER = ("Customer", "CUSTOMER")

    default_type = UserType.CUSTOMER

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("User email"), max_length=255, unique=True)
    phone = models.CharField(
        _("User Phone Number"), max_length=10, unique=True, null=True
    )
    profile_type = models.CharField(
        max_length=255, choices=UserType.choices, default=default_type
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"User - {self.email}"

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("user:detail", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        created = not self.pk

        if created and not self.profile_type:
            self.profile_type = self.default_type

        return super().save(*args, **kwargs)


class SellerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(profile_type=User.UserType.SELLER)
        )


class CustomerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(profile_type=User.UserType.CUSTOMER)
        )


class Seller(User):
    """
    User proxy model for sellers
    """

    default_type = User.UserType.SELLER
    objects = SellerManager()

    class Meta:
        proxy = True


class Customer(User):
    """
    User proxy model for customer
    """

    default_type = User.UserType.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True
