"""
Module demonstrating space members retrieval functionality.
"""

from .config import get_client


def get_space_members():
    """Get all members in the space using the Vaiz SDK."""
    client = get_client()
    
    try:
        response = client.get_space_members()
        
        print("=== Space Members ===")
        print(f"Total members: {len(response.members)}\n")
        
        for member in response.members:
            print(f"👤 {member.full_name or member.nick_name}")
            print(f"   ID: {member.id}")
            print(f"   Email: {member.email}")
            print(f"   Nick: {member.nick_name}")
            print(f"   Status: {member.status}")
            print(f"   Color: {member.color.color} (Dark: {member.color.is_dark})")
            print(f"   Avatar Mode: {member.avatar_mode}")
            if member.avatar:
                print(f"   Avatar: {member.avatar}")
            print(f"   Joined: {member.joined_date}")
            print(f"   Updated: {member.updated_at}")
            print()
        
        return len(response.members)
    except Exception as e:
        print(f"Error retrieving space members: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None


if __name__ == "__main__":
    get_space_members()

