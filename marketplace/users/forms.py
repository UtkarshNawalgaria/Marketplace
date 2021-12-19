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
        fields = ("profile_type", "email", "password")

    def clean_email(self):
        # check if user exists with the email address
        user_email = self.cleaned_data["email"]

        try:
            user = User.objects.get(email=user_email)
            if user:
                self.add_error("email", "An account with this email already exists")
        except Exception:
            pass

        return user_email
