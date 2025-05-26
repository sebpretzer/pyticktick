import pytest

from pyticktick.models.v2 import UserProfileV2, UserStatisticsV2, UserStatusV2


@pytest.mark.order(1)
def test_get_profile(client):
    profile = client.get_profile_v2()
    assert isinstance(profile, UserProfileV2)
    assert profile.username == client.v2_username


@pytest.mark.order(1)
@pytest.mark.dependency(name="helper_get_status_v2", scope="session")
def test_get_status_v2(client):
    status = client.get_status_v2()
    assert isinstance(status, UserStatusV2)
    assert status.username == client.v2_username
    assert status.inbox_id == f"inbox{status.user_id}"


@pytest.mark.order(1)
def test_get_statistics_v2(client):
    statistics = client.get_statistics_v2()
    assert isinstance(statistics, UserStatisticsV2)
