"""
Module demonstrating profile retrieval functionality.
"""

from .config import get_client

def get_profile():
    """Get user profile using the Vaiz SDK."""
    client = get_client()
    
    try:
        response = client.get_profile()
        profile = response.payload["profile"]
        
        print("Profile retrieved successfully!")
        print(f"ID: {profile.id}")
        print(f"Full Name: {profile.full_name}")
        print(f"Nickname: {profile.nick_name}")
        print(f"Email: {profile.email}")
        print("\nEmail Addresses:")
        for email in profile.emails:
            print(f"  - {email.email} (Primary: {email.primary}, Confirmed: {email.confirmed})")
        print(f"\nAvatar Mode: {profile.avatar_mode}")
        print(f"Incomplete Steps: {profile.incomplete_steps}")
        print(f"Member ID: {profile.member_id}")
        print(f"Created: {profile.created_at}")
        print(f"Updated: {profile.updated_at}")
        
        return profile.id
    except Exception as e:
        print(f"Error retrieving profile: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    get_profile() 