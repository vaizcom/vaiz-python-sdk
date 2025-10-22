import re
from vaiz.models import ProfileResponse, Profile
from tests.test_config import get_test_client


def is_valid_color_name(color: str) -> bool:
    """Check if the string is a valid color name or hex color."""
    valid_colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'black', 'white']
    # Accept both color names and hex colors (since API may return hex)
    if color.lower() in valid_colors:
        return True
    # Check if it's a valid hex color
    hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    return bool(re.match(hex_pattern, color))


def test_get_profile():
    client = get_test_client()
    response = client.get_profile()
    assert isinstance(response, ProfileResponse)
    assert isinstance(response.profile, Profile)
    profile = response.profile
    assert isinstance(profile.id, str)
    assert isinstance(profile.full_name, str)
    assert isinstance(profile.nick_name, str)
    assert isinstance(profile.email, str)
    assert isinstance(profile.emails, list)
    assert len(profile.emails) > 0
    assert isinstance(profile.emails[0].email, str)
    assert isinstance(profile.emails[0].confirmed, bool)
    assert isinstance(profile.emails[0].primary, bool)
    assert isinstance(profile.avatar_mode, int)
    assert isinstance(profile.incomplete_steps, list)
    assert isinstance(profile.member_id, str)
    if profile.color.color is not None:
        assert isinstance(profile.color.color, str)
        assert is_valid_color_name(profile.color.color)
    if profile.color.is_dark is not None:
        assert isinstance(profile.color.is_dark, bool) 