"""
Module demonstrating space information retrieval functionality.
"""

from .config import get_client
import os


def get_space():
    """Get space information using the Vaiz SDK."""
    client = get_client()
    
    # Get space ID from environment or use the one from config
    space_id = os.getenv("VAIZ_SPACE_ID")
    if not space_id:
        print("Error: VAIZ_SPACE_ID not set in environment")
        return None
    
    try:
        response = client.get_space(space_id)
        space = response.space
        
        print("=== Space Information ===")
        print(f"ID: {space.id}")
        print(f"Name: {space.name}")
        print(f"Color: {space.color.color}")
        print(f"Is Dark: {space.color.is_dark}")
        print(f"Avatar Mode: {space.avatar_mode}")
        if space.avatar:
            print(f"Avatar: {space.avatar}")
        print(f"Creator: {space.creator}")
        print(f"Plan: {space.plan}")
        print(f"Is Foreign: {space.is_foreign}")
        print(f"Created: {space.created_at}")
        print(f"Updated: {space.updated_at}")
        
        return space.id
    except Exception as e:
        print(f"Error retrieving space: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None


if __name__ == "__main__":
    get_space()

