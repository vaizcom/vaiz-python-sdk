import pytest
import re
from vaiz.models import ProfileResponse, Profile
from tests.test_config import get_test_client


def is_valid_hex_color(color: str) -> bool:
    """Check if the string is a valid hex color."""
    hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    return bool(re.match(hex_pattern, color))


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
    if profile.color.color is not None:
        assert isinstance(profile.color.color, str)
        assert is_valid_hex_color(profile.color.color)
    if profile.color.isDark is not None:
        assert isinstance(profile.color.isDark, bool) 