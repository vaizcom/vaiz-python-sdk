"""
Module demonstrating board group editing functionality.
"""

from .config import get_client, BOARD_ID
from vaiz.models import CreateBoardGroupRequest, EditBoardGroupRequest

def edit_board_group():
    """Create and then edit a board group using the Vaiz SDK."""
    client = get_client()
    
    # Create a board group first
    create_request = CreateBoardGroupRequest(
        name="Test Group to Edit",
        board_id=BOARD_ID,
        description="This group will be edited."
    )

    create_response = client.create_board_group(create_request)
    created_group = create_response.board_groups[0]
    print(f"✅ Board group created: {created_group.name} (ID: {created_group.id})")

    # Now edit the created group
    edit_request = EditBoardGroupRequest(
        board_group_id=created_group.id,
        board_id=BOARD_ID,
        name="Updated Group Name",
        description="This is an updated description.",
        limit=20,
        hidden=False
    )

    try:
        edit_response = client.edit_board_group(edit_request)
        edited_group = next((g for g in edit_response.board_groups if g.id == created_group.id), None)
        
        if edited_group:
            print("\nBoard group edited successfully!")
            print(f"Edited group ID: {edited_group.id}")
            print(f"New name: {edited_group.name}")
            print(f"New description: {edited_group.description}")
            print(f"New limit: {edited_group.limit}")
            print(f"Is hidden: {edited_group.hidden}")
            return edited_group.id
        else:
            print("\nFailed to find the edited group in the response.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    edit_board_group() 