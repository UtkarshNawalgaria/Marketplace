import pytest
from django.urls import resolve, reverse

from marketplace.users.models import User

pytestmark = pytest.mark.django_db


def test_detail(user: User):
    assert reverse("user:detail", kwargs={"id": user.id}) == f"/user/{user.id}/"
    assert resolve(f"/user/{user.id}/").view_name == "user:detail"


def test_update():
    assert reverse("user:update") == "/user/~update/"
    assert resolve("/user/~update/").view_name == "user:update"


def test_redirect():
    assert reverse("user:redirect") == "/user/~redirect/"
    assert resolve("/user/~redirect/").view_name == "user:redirect"
