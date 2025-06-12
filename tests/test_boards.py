import pytest
from vaiz.models import BoardsResponse, Board, BoardResponse
from tests.test_config import get_test_client, TEST_BOARD_ID
from vaiz.models import CreateBoardTypeRequest, EditBoardTypeRequest

def test_get_boards():
    client = get_test_client()
    response = client.get_boards()
    assert isinstance(response, BoardsResponse)
    assert hasattr(response.payload, 'boards')
    boards = response.payload.boards
    assert isinstance(boards, list)
    # Проверим хотя бы одну доску, если есть
    if boards:
        board = boards[0]
        assert isinstance(board, Board)
        assert isinstance(board.id, str)
        assert isinstance(board.name, str)

def test_get_board():
    client = get_test_client()
    response = client.get_board(TEST_BOARD_ID)
    assert isinstance(response, BoardResponse)
    assert isinstance(response.payload["board"], Board)
    board = response.payload["board"]
    assert board.id == TEST_BOARD_ID
    assert isinstance(board.name, str)

def test_create_board_type():
    client = get_test_client()
    request = CreateBoardTypeRequest(
        boardId=TEST_BOARD_ID,
        label="Test Type",
        icon="Cursor",
        color="silver"
    )
    response = client.create_board_type(request)
    assert response.type == "CreateBoardType"
    assert response.board_type.label == "Test Type"
    assert response.board_type.icon == "Cursor"
    assert response.board_type.color == "silver"
    assert isinstance(response.board_type.id, str)

def test_edit_board_type():
    client = get_test_client()
    request = EditBoardTypeRequest(
        boardTypeId="684ad3b021b100837be1a521",  # Using the ID from your example
        boardId=TEST_BOARD_ID,
        label="Updated Test Type",
        icon="Cursor",
        color="silver",
        description="Updated test description",
        hidden=True
    )
    response = client.edit_board_type(request)
    assert response.type == "EditBoardType"
    assert response.board_type.label == "Updated Test Type"
    assert response.board_type.icon == "Cursor"
    assert response.board_type.color == "silver"
    assert response.board_type.description == "Updated test description"
    assert response.board_type.hidden is True
    assert response.board_type.id == "684ad3b021b100837be1a521" 