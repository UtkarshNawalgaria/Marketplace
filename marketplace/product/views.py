from django.contrib.auth import get_user_model
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render

from marketplace.product.forms import CategoryForm
from marketplace.product.models import Category

User = get_user_model()


def create_category(request):
    context = {}
    user = request.user

    if not (user.is_authenticated() and user.is_superuser):
        raise HttpResponseForbidden("You are not authorized to call this method.")

    if request.method == "POST":
        form = CategoryForm(request.POST or None)

        if form.is_valid():
            form.save()

    context["form"] = CategoryForm()
    return render(request, "", context)
