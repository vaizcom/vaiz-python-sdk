import re
import uuid
from vaiz.models import ProfileResponse, Profile, EditProfileRequest
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
    assert isinstance(profile.avatar_mode, int)
    assert isinstance(profile.member_id, str)
    assert isinstance(profile.user_id, str)
    assert profile.member_id != profile.user_id
    if profile.color.color is not None:
        assert isinstance(profile.color.color, str)
        assert is_valid_color_name(profile.color.color)
    if profile.color.is_dark is not None:
        assert isinstance(profile.color.is_dark, bool)


def test_profile_member_id_matches_space_member():
    """Profile member_id must be usable wherever a space member ID is expected."""
    client = get_test_client()
    profile = client.get_profile().profile
    member_ids = {m.id for m in client.get_space_members().members}
    assert profile.member_id in member_ids


def test_edit_profile_request_serialization():
    request = EditProfileRequest(full_name="John Doe", phone_number="+100", bio="")
    assert request.model_dump() == {"fullName": "John Doe", "phoneNumber": "+100", "bio": ""}
    assert EditProfileRequest().model_dump() == {}


def test_edit_profile():
    client = get_test_client()
    original = client.get_profile().profile
    marker = uuid.uuid4().hex[:8]

    try:
        response = client.edit_profile(EditProfileRequest(
            position=f"SDK position {marker}",
            bio=f"SDK bio {marker}",
            phone_number="+10000000000",
        ))
        assert isinstance(response, ProfileResponse)
        assert response.type == "EditProfile"
        profile = response.profile
        assert profile.member_id == original.member_id
        assert profile.position == f"SDK position {marker}"
        assert profile.bio == f"SDK bio {marker}"
        assert profile.phone_number == "+10000000000"
        assert profile.full_name == original.full_name

        reloaded = client.get_profile().profile
        assert reloaded.position == f"SDK position {marker}"

        member = client.get_members([original.member_id]).members[0]
        assert member.position == f"SDK position {marker}"
    finally:
        client.edit_profile(EditProfileRequest(
            position=original.position or "",
            bio=original.bio or "",
            phone_number=original.phone_number or "",
        ))

    restored = client.get_profile().profile
    assert (restored.position or "") == (original.position or "")
    assert (restored.bio or "") == (original.bio or "")


def test_profile_parses_new_member_shape():
    profile = Profile(**{
        "_id": "member1",
        "user": "user1",
        "space": "space1",
        "status": "Active",
        "fullName": "John Doe",
        "nickName": "johndoe",
        "email": "john@example.com",
        "avatarMode": 0,
        "color": {"color": "#f8e8e8", "isDark": False},
        "joinedDate": "2026-10-01T10:42:11.891Z",
        "updatedAt": "2026-10-01T10:42:12.354Z",
    })
    assert profile.id == "member1"
    assert profile.member_id == "member1"
    assert profile.user_id == "user1"
    assert profile.space == "space1"


def test_profile_parses_legacy_user_shape():
    profile = Profile(**{
        "_id": "user1",
        "memberId": "member1",
        "fullName": "John Doe",
        "nickName": "johndoe",
        "email": "john@example.com",
        "emails": [{"email": "john@example.com", "confirmed": True, "primary": True}],
        "avatarMode": 0,
        "registeredDate": "2025-01-01T00:00:00.000Z",
        "updatedAt": "2025-01-01T00:00:00.000Z",
    })
    assert profile.member_id == "member1"
    assert profile.user_id == "user1"
    assert len(profile.emails) == 1
