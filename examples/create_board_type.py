from vaiz import VaizClient
from vaiz.models import CreateBoardTypeRequest
from config import get_client


def main():
    # Get client from config
    client = get_client()

    # Create board type request
    request = CreateBoardTypeRequest(
        boardId="67f8d680db3b257778cfcf83",  # Replace with your board ID
        label="New Type",
        icon="Cursor",
        color="silver"
    )

    # Create board type
    response = client.create_board_type(request)

    # Print response
    print(f"Created board type: {response.board_type.label}")
    print(f"Board type ID: {response.board_type.id}")
    print(f"Board type icon: {response.board_type.icon}")
    print(f"Board type color: {response.board_type.color}")


if __name__ == "__main__":
    main() 