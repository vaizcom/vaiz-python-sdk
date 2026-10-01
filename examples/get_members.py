"""
Module demonstrating member retrieval by IDs.
"""

from .config import get_client


def get_members():
    """Resolve member IDs (e.g. task assignees or history authors) to member profiles."""
    client = get_client()
    
    try:
        member_ids = [client.get_profile().profile.member_id]
        response = client.get_members(member_ids)
        
        print("=== Members ===")
        for member in response.members:
            print(f"👤 {member.full_name or member.nick_name}")
            print(f"   ID: {member.id}")
            print(f"   Email: {member.email}")
            print(f"   Position: {member.position or 'N/A'}")
            print()
        
        return len(response.members)
    except Exception as e:
        print(f"Error retrieving members: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None


if __name__ == "__main__":
    get_members()
