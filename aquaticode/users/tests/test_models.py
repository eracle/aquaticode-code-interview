import pytest

from aquaticode.users.models import User


@pytest.mark.skip
def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"
