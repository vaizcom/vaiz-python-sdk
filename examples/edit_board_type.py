from vaiz import VaizClient
from vaiz.models import EditBoardTypeRequest
from config import get_client


def main():
    # Get client from config
    client = get_client()

    # Edit board type request
    request = EditBoardTypeRequest(
        boardTypeId="684ad3b021b100837be1a521",  # Replace with your board type ID
        boardId="67f8d680db3b257778cfcf83",  # Replace with your board ID
        label="Updated Type",
        icon="Cursor",
        color="silver",
        description="Updated description",
        hidden=True
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