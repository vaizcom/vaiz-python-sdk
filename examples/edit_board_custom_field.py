"""
Module demonstrating board custom field editing functionality.
"""

from .config import get_client, BOARD_ID
from vaiz.models import EditBoardCustomFieldRequest

def edit_board_custom_field(field_id: str):
    """Edit a board custom field using the Vaiz SDK."""
    client = get_client()
    
    try:
        request = EditBoardCustomFieldRequest(
            fieldId=field_id,
            boardId=BOARD_ID,
            hidden=True,
            description="Updated field description"
        )
        
        response = client.edit_board_custom_field(request)
        custom_field = response.custom_field
        
        print("Custom field updated successfully!")
        print(f"Field name: {custom_field.name}")
        print(f"Field ID: {custom_field.id}")
        print(f"Field type: {custom_field.type}")
        print(f"Hidden: {custom_field.hidden}")
        print(f"Description: {custom_field.description}")
        
        return custom_field.id
    except Exception as e:
        print(f"Error updating custom field: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    # Replace with an actual field ID from your board
    FIELD_ID = "your_field_id_here"
    edit_board_custom_field(FIELD_ID) 