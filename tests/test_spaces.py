import re
from vaiz.models import GetSpaceResponse, Space, ColorInfo, AvatarMode
from tests.test_config import get_test_client, TEST_SPACE_ID


def is_valid_hex_color(color: str) -> bool:
    """Check if the string is a valid hex color."""
    hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    return bool(re.match(hex_pattern, color))


def test_get_space():
    """Test getting space information."""
    client = get_test_client()
    
    # Get space information using the test space ID
    response = client.get_space(TEST_SPACE_ID)
    
    # Validate response structure
    assert isinstance(response, GetSpaceResponse)
    assert response.type == "GetSpace"
    assert hasattr(response, 'payload')
    assert hasattr(response.payload, 'space')
    
    # Validate space object
    space = response.space
    assert isinstance(space, Space)
    
    # Validate required fields
    assert isinstance(space.id, str)
    assert len(space.id) > 0
    assert space.id == TEST_SPACE_ID
    
    assert isinstance(space.name, str)
    assert len(space.name) > 0
    
    # Validate color
    assert isinstance(space.color, ColorInfo)
    assert isinstance(space.color.color, str)
    assert is_valid_hex_color(space.color.color)
    assert isinstance(space.color.is_dark, bool)
    
    # Validate other fields
    assert isinstance(space.avatar_mode, AvatarMode)
    assert space.avatar_mode in [AvatarMode.Uploaded, AvatarMode.Generated]
    
    if space.avatar:
        assert isinstance(space.avatar, str)
        assert len(space.avatar) > 0
    
    # Creator can be either string ID or user object
    assert space.creator is not None
    if isinstance(space.creator, str):
        assert len(space.creator) > 0
    elif isinstance(space.creator, dict):
        assert '_id' in space.creator
    
    assert isinstance(space.plan, str)
    assert len(space.plan) > 0
    
    assert isinstance(space.is_foreign, bool)
    
    # Validate timestamps
    assert space.created_at is not None
    assert space.updated_at is not None
    
    print(f"✓ Space test passed: {space.name} ({space.id})")


if __name__ == "__main__":
    test_get_space()

