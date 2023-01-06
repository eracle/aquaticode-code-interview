import pytest
from django.urls import resolve, reverse

from aquaticode.users.models import User


@pytest.mark.skip
def test_detail(user: User):
    assert (
        reverse("users:detail", kwargs={"username": user.username})
        == f"/users/{user.username}/"
    )
    assert resolve(f"/users/{user.username}/").view_name == "users:detail"


@pytest.mark.skip
def test_update():
    assert reverse("users:update") == "/users/~update/"
    assert resolve("/users/~update/").view_name == "users:update"


@pytest.mark.skip
def test_redirect():
    assert reverse("users:redirect") == "/users/~redirect/"
    assert resolve("/users/~redirect/").view_name == "users:redirect"
