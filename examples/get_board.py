"""
Module demonstrating board retrieval functionality.
"""

from .config import get_client, BOARD_ID

def get_board():
    """Get a single board using the Vaiz SDK."""
    client = get_client()
    
    try:
        response = client.get_board(BOARD_ID)
        board = response.payload["board"]
        
        print("Board retrieved successfully!")
        print(f"Board name: {board.name}")
        print(f"Board ID: {board.id}")
        print(f"Project: {board.project}")
        print(f"Groups: {[g.name for g in (board.groups or [])]}")
        print(f"Types: {[t.label for t in (board.types_list or [])]}")
        print(f"Custom Fields: {[cf.name for cf in (board.custom_fields or [])]}")
        
        return board.id
    except Exception as e:
        print(f"Error retrieving board: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    get_board() 