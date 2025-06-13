"""
Module demonstrating board custom field creation functionality.
"""

from .config import get_client, BOARD_ID
from vaiz.models import CreateBoardCustomFieldRequest, CustomFieldType

def create_board_custom_field():
    """Create a new custom field in a board using the Vaiz SDK."""
    client = get_client()
    
    try:
        request = CreateBoardCustomFieldRequest(
            name="Date",
            type=CustomFieldType.DATE,
            boardId=BOARD_ID,
            description="Date field for tracking deadlines",
            hidden=False
        )
        
        response = client.create_board_custom_field(request)
        custom_field = response.custom_field
        
        print("Custom field created successfully!")
        print(f"Field name: {custom_field.name}")
        print(f"Field type: {custom_field.type}")
        print(f"Field ID: {custom_field.id}")
        print(f"Description: {custom_field.description}")
        print(f"Hidden: {custom_field.hidden}")
        
        return custom_field.id
    except Exception as e:
        print(f"Error creating custom field: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    create_board_custom_field() 