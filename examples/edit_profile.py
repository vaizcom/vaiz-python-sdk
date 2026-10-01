"""
Module demonstrating profile editing functionality.
"""

from vaiz import EditProfileRequest

from .config import get_client


def edit_profile():
    """Update the current member's position and bio in the current space."""
    client = get_client()
    
    try:
        original = client.get_profile().profile
        print(f"Current position: {original.position or 'N/A'}")
        
        response = client.edit_profile(EditProfileRequest(
            position="Developer Advocate",
            bio="Updated via Vaiz Python SDK",
        ))
        profile = response.profile
        print(f"New position: {profile.position}")
        print(f"New bio: {profile.bio}")
        
        client.edit_profile(EditProfileRequest(
            position=original.position or "",
            bio=original.bio or "",
        ))
        print("Profile restored")
        
        return profile.member_id
    except Exception as e:
        print(f"Error editing profile: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None


if __name__ == "__main__":
    edit_profile()
