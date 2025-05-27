from time import time
from typing import Callable
from uuid import uuid4

import pytest

from pyticktick.models.v2 import UserSignOnV2


@pytest.fixture()
def test_v1_token_expiration_days() -> Callable[[int], int]:
    def _test_v1_token_expiration_days(days: int) -> int:
        return int(time()) + days * 24 * 60 * 60

    return _test_v1_token_expiration_days


@pytest.fixture()
def test_v1_client_id() -> str:
    return "test_client_id"


@pytest.fixture()
def test_v1_client_secret() -> str:
    return "test_client_secret"


@pytest.fixture()
def test_v1_token_value() -> str:
    return str(uuid4())


@pytest.fixture()
def test_v1_token_expiration(test_v1_token_expiration_days) -> str:
    return test_v1_token_expiration_days(30)


@pytest.fixture()
def test_v2_username() -> str:
    return "test@username.com"


@pytest.fixture()
def test_v2_password() -> str:
    return "test_password"


@pytest.fixture()
def test_v2_token() -> str:
    return "test_token_value"


@pytest.fixture()
def test_v2_usersignonv2(test_v2_username, test_v2_token) -> UserSignOnV2:
    return UserSignOnV2(
        token=test_v2_token,
        user_id="test_user_id",
        user_code=uuid4(),
        username=test_v2_username,
        team_pro=False,
        pro_start_date="test_pro_start_date",
        pro_end_date="test_pro_end_date",
        subscribe_type="test_subscribe_type",
        subscribe_freq="test_subscribe_freq",
        need_subscribe=False,
        freq="test_freq",
        inbox_id="test_inbox_id",
        team_user=False,
        active_team_user=False,
        free_trial=False,
        grace_period=False,
        pro=False,
        ds=False,
    )
