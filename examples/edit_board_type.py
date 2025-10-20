from vaiz import VaizClient
from vaiz.models import EditBoardTypeRequest
from .config import BOARD_ID,get_client


def main():
    # Get client from config
    client = get_client()

    board_response = client.get_board(BOARD_ID)
    board = board_response.payload["board"]

    # Edit an existing board type
    edit_request = EditBoardTypeRequest(
        board_type_id=BOARD_TYPE_ID,
        board_id=BOARD_ID,
        label="Updated Type",
        icon=Icon.Bookmark,
        color=Color.Green,
        description="Updated description for the board type",
        hidden=False
    )

    # Edit board type
    response = client.edit_board_type(request)

    # Print response
    print(f"Updated board type: {response.board_type.label}")
    print(f"Board type ID: {response.board_type.id}")
    print(f"Board type icon: {response.board_type.icon}")
    print(f"Board type color: {response.board_type.color}")
    print(f"Board type description: {response.board_type.description}")
    print(f"Board type hidden: {response.board_type.hidden}")


if __name__ == "__main__":
    main() 