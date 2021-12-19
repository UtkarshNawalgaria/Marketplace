from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, RedirectView, UpdateView

from marketplace.users.forms import UserSignupForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):

        user = self.request.user
        if user.profile_type == User.UserType.CUSTOMER:
            return reverse("core:customer-dashboard")

        return reverse("core:seller-dashboard")


user_redirect_view = UserRedirectView.as_view()


class UserSignupView(CreateView):
    template_name = "users/signup.html"
    form_class = UserSignupForm

    def post(self, request, *args, **kwargs):

        form = UserSignupForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

            login(request, user)

            return redirect("user:redirect")

        form = UserSignupForm()
        return render(request, "users/signup.html", {"form": form})


user_signup_view = UserSignupView.as_view()


def user_logout_view(request):
    logout(request)
    return redirect("user:signup")
