import re
from vaiz.models import GetSpaceMembersResponse, GetMembersRequest, GetMembersResponse, Member, ColorInfo, AvatarMode
from tests.test_config import get_test_client


def is_valid_hex_color(color: str) -> bool:
    """Check if the string is a valid hex color."""
    hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    return bool(re.match(hex_pattern, color))


def test_get_space_members():
    """Test getting space members."""
    client = get_test_client()
    
    # Get space members
    response = client.get_space_members()
    
    # Validate response structure
    assert isinstance(response, GetSpaceMembersResponse)
    assert response.type == "GetSpaceMembers"
    assert hasattr(response, 'payload')
    assert hasattr(response.payload, 'members')
    
    # Validate members list
    members = response.members
    assert isinstance(members, list)
    assert len(members) > 0, "Should have at least one member"
    
    # Validate first member
    member = members[0]
    assert isinstance(member, Member)
    
    # Validate required fields
    assert isinstance(member.id, str)
    assert len(member.id) > 0
    
    assert isinstance(member.email, str)
    assert len(member.email) > 0
    assert "@" in member.email
    
    # Validate optional string fields
    if member.nick_name:
        assert isinstance(member.nick_name, str)
    
    if member.full_name:
        assert isinstance(member.full_name, str)
    
    # Validate color
    assert isinstance(member.color, ColorInfo)
    assert isinstance(member.color.color, str)
    assert is_valid_hex_color(member.color.color)
    assert isinstance(member.color.is_dark, bool)
    
    # Validate avatar
    assert isinstance(member.avatar_mode, AvatarMode)
    assert member.avatar_mode in [AvatarMode.Uploaded, AvatarMode.Generated]
    
    if member.avatar:
        assert isinstance(member.avatar, str)
        assert len(member.avatar) > 0
    
    # Validate other fields
    assert isinstance(member.space, str)
    assert len(member.space) > 0
    
    assert isinstance(member.status, str)
    assert len(member.status) > 0
    
    assert isinstance(member.joined_date, str)
    assert len(member.joined_date) > 0
    
    assert isinstance(member.updated_at, str)
    assert len(member.updated_at) > 0
    
    print(f"✓ Members test passed: {len(members)} member(s) found")


def test_get_members_by_ids():
    client = get_test_client()
    space_members = client.get_space_members().members
    expected = {m.id: m for m in space_members[:3]}

    response = client.get_members(list(expected))

    assert isinstance(response, GetMembersResponse)
    assert response.type == "GetMembers"
    assert {m.id for m in response.members} == set(expected)
    for member in response.members:
        assert isinstance(member, Member)
        assert member.email == expected[member.id].email
        assert member.full_name == expected[member.id].full_name


def test_get_members_current_member():
    client = get_test_client()
    profile = client.get_profile().profile

    members = client.get_members([profile.member_id]).members

    assert len(members) == 1
    assert members[0].id == profile.member_id
    assert members[0].email == profile.email


def test_get_members_skips_unknown_ids():
    client = get_test_client()
    profile = client.get_profile().profile

    members = client.get_members([profile.member_id, "not-an-object-id", "000000000000000000000000"]).members

    assert [m.id for m in members] == [profile.member_id]


def test_get_members_empty_list():
    client = get_test_client()
    assert client.get_members([]).members == []


def test_get_members_request_serialization():
    assert GetMembersRequest(member_ids=["a", "b"]).model_dump() == {"memberIds": ["a", "b"]}


if __name__ == "__main__":
    test_get_space_members()

