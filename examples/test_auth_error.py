"""
Test script to demonstrate authentication error handling.
"""

from vaiz import VaizClient
from vaiz.models import CreateBoardTypeRequest
from vaiz.models.enums import Color

def main():
    # Create client with invalid token
    client = VaizClient(
        api_key="invalid_token",
        space_id="test_space",
        verify_ssl=False,
        base_url="https://api.vaiz.local:10000/v4",
        verbose=True  # Enable debug output
    )

    # Try to create a board type (this should fail with auth error)
    request = CreateBoardTypeRequest(
        boardId="test_board",
        label="Test Type",
        icon="Cursor",
        color=Color.Silver
    )

    try:
        client.create_board_type(request)
        print("Success! (This shouldn't happen)")
    except Exception as e:
        print(f"\nCaught error: {type(e).__name__}")
        print(f"Error message:\n{str(e)}")

if __name__ == "__main__":
    main() 