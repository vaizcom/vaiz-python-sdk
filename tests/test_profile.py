import pytest
from vaiz.models import ProfileResponse, Profile
from tests.test_config import get_test_client


def test_get_profile():
    client = get_test_client()
    response = client.get_profile()
    assert isinstance(response, ProfileResponse)
    assert isinstance(response.payload["profile"], Profile)
    profile = response.payload["profile"]
    assert isinstance(profile.id, str)
    assert isinstance(profile.fullName, str)
    assert isinstance(profile.nickName, str)
    assert isinstance(profile.email, str)
    assert isinstance(profile.emails, list)
    assert len(profile.emails) > 0
    assert isinstance(profile.emails[0].email, str)
    assert isinstance(profile.emails[0].confirmed, bool)
    assert isinstance(profile.emails[0].primary, bool)
    assert isinstance(profile.avatarMode, int)
    assert isinstance(profile.incompleteSteps, list)
    assert isinstance(profile.memberId, str) 