import pytest
from vaiz.models import BoardsResponse, Board, BoardResponse
from tests.test_config import get_test_client, TEST_BOARD_ID
from vaiz.models import CreateBoardTypeRequest, EditBoardTypeRequest, CreateBoardCustomFieldRequest, CustomFieldType

@pytest.fixture
def board_type_id():
    client = get_test_client()
    request = CreateBoardTypeRequest(
        boardId=TEST_BOARD_ID,
        label="Test Type",
        icon="Cursor",
        color="silver"
    )
    response = client.create_board_type(request)
    return response.board_type.id

def test_get_boards():
    client = get_test_client()
    response = client.get_boards()
    assert isinstance(response, BoardsResponse)
    assert hasattr(response.payload, 'boards')
    boards = response.payload.boards
    assert isinstance(boards, list)
    # Check at least one board if exists
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

def test_create_board_type(board_type_id):
    assert isinstance(board_type_id, str)

def test_edit_board_type(board_type_id):
    client = get_test_client()
    request = EditBoardTypeRequest(
        boardTypeId=board_type_id,
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
    assert response.board_type.id == board_type_id

    # Additional check: label has been updated in the system
    board = client.get_board(TEST_BOARD_ID).payload["board"]
    found = False
    for t in (board.types_list or []):
        if t.id == board_type_id:
            assert t.label == "Updated Test Type"
            found = True
    assert found, "Updated board type not found in board"

def test_create_board_custom_field():
    client = get_test_client()
    request = CreateBoardCustomFieldRequest(
        name="Test Date Field",
        type=CustomFieldType.DATE,
        boardId=TEST_BOARD_ID,
        description="Test date field description",
        hidden=False
    )
    response = client.create_board_custom_field(request)
    assert response.type == "CreateBoardCustomField"
    assert response.custom_field.name == "Test Date Field"
    assert response.custom_field.type == CustomFieldType.DATE
    assert response.custom_field.description == "Test date field description"
    assert response.custom_field.hidden is False
    assert response.custom_field.id is not None

    # Additional check: custom field has been added to the board
    board = client.get_board(TEST_BOARD_ID).payload["board"]
    found = False
    for cf in (board.custom_fields or []):
        if cf.id == response.custom_field.id:
            assert cf.name == "Test Date Field"
            assert cf.type == CustomFieldType.DATE
            found = True
    assert found, "Created custom field not found in board" 