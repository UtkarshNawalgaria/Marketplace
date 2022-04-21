from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

        error_messages = {"email": {"unique": _("This email has already been taken.")}}


class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password")

    def clean_email(self):
        user_email = self.cleaned_data["email"]
        user = User.objects.filter(email=user_email)

        if user.exists():
            self.add_error("email", "Account with this email already exists")

        return user_email
