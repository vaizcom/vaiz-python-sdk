"""
Module demonstrating board group editing functionality.
"""

from .config import get_client, BOARD_ID
from vaiz.models import CreateBoardGroupRequest, EditBoardGroupRequest

def edit_board_group():
    """Create and then edit a board group using the Vaiz SDK."""
    client = get_client()
    
    # First, create a group to edit
    create_request = CreateBoardGroupRequest(
        name="Group to Edit",
        boardId=BOARD_ID,
        description="This group will be edited."
    )
    
    try:
        create_response = client.create_board_group(create_request)
        new_group = next((g for g in create_response.board_groups if g.name == "Group to Edit"), None)
        
        if not new_group:
            print("Failed to create the group for editing.")
            return

        print(f"Group created with ID: {new_group.id}")

        # Now, edit the created group
        edit_request = EditBoardGroupRequest(
            boardGroupId=new_group.id,
            boardId=BOARD_ID,
            name="Edited Group Name",
            description="This group has been successfully edited.",
            limit=15,
            hidden=False
        )

        edit_response = client.edit_board_group(edit_request)
        edited_group = next((g for g in edit_response.board_groups if g.id == new_group.id), None)
        
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