"""
Module demonstrating board group creation functionality.
"""

from .config import get_client, BOARD_ID
from vaiz.models import CreateBoardGroupRequest

def create_board_group():
    """Create a new board group using the Vaiz SDK."""
    client = get_client()
    
    request = CreateBoardGroupRequest(
        name="New Group",
        board_id=BOARD_ID,
        description="This is a new group."
    )
    
    try:
        response = client.create_board_group(request)
        board_groups = response.board_groups
        
        print("Board group created successfully!")
        print(f"Total groups in board: {len(board_groups)}")
        
        new_group = next((g for g in board_groups if g.name == "Test Group"), None)
        if new_group:
            print(f"New group name: {new_group.name}")
            print(f"New group ID: {new_group.id}")
            print(f"New group description: {new_group.description}")
        
        return new_group.id if new_group else None
    except Exception as e:
        print(f"Error creating board group: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    create_board_group() 