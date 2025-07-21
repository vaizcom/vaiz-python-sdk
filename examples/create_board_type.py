from vaiz import VaizClient
from vaiz.models import CreateBoardTypeRequest
from vaiz.api.base import VaizHTTPError, VaizSDKError
from .config import get_client


def main():
    # Get client from config with verbose mode enabled
    client = get_client()
    client.verbose = True  # Enable debug output

    # Create board type request with invalid board ID
    request = CreateBoardTypeRequest(
        board_id="invalid_board_id",  # This will cause an error
        label="New Type",
        icon="Cursor",
        color="silver"
    )

    try:
        # Create board type
        response = client.create_board_type(request)

        # Print response
        print(f"Created board type: {response.board_type.label}")
        print(f"Board type ID: {response.board_type.id}")
        print(f"Board type icon: {response.board_type.icon}")
        print(f"Board type color: {response.board_type.color}")

    except VaizHTTPError as e:
        print("\n=== HTTP Error ===")
        print(f"Status code: {e.status_code}")
        print(f"URL: {e.url}")
        print(f"Error message: {e.response_text}")
        print("================\n")

    except VaizSDKError as e:
        print("\n=== SDK Error ===")
        print(f"Error message: {str(e)}")
        print("================\n")

    except Exception as e:
        print("\n=== Unexpected Error ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("================\n")


if __name__ == "__main__":
    main() 