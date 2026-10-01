"""
Module demonstrating profile retrieval functionality.
"""

from .config import get_client

def get_profile():
    """Get the current member's profile using the Vaiz SDK."""
    client = get_client()
    
    try:
        response = client.get_profile()
        profile = response.profile
        
        print("Profile retrieved successfully!")
        print(f"Member ID: {profile.member_id}")
        print(f"User ID: {profile.user_id}")
        print(f"Space: {profile.space}")
        print(f"Full Name: {profile.full_name}")
        print(f"Nickname: {profile.nick_name}")
        print(f"Email: {profile.email}")
        print(f"Position: {profile.position}")
        print(f"\nAvatar Mode: {profile.avatar_mode}")
        print(f"Joined: {profile.joined_date}")
        print(f"Updated: {profile.updated_at}")
        
        return profile.member_id
    except Exception as e:
        print(f"Error retrieving profile: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    get_profile() 