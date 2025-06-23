import pytest
from vaiz.models import BoardsResponse, Board, BoardResponse
from tests.test_config import get_test_client, TEST_BOARD_ID
from vaiz.models import CreateBoardTypeRequest, EditBoardTypeRequest, CreateBoardCustomFieldRequest, EditBoardCustomFieldRequest, CustomFieldType, CreateBoardGroupRequest, CreateBoardGroupResponse, EditBoardGroupRequest, EditBoardGroupResponse

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

def test_edit_board_custom_field():
    client = get_test_client()
    
    # First create a custom field
    create_request = CreateBoardCustomFieldRequest(
        name="Test Field",
        type=CustomFieldType.TEXT,
        boardId=TEST_BOARD_ID,
        hidden=False,
        description="Test description"
    )
    create_response = client.create_board_custom_field(create_request)
    field_id = create_response.custom_field.id
    
    # Then edit it
    edit_request = EditBoardCustomFieldRequest(
        fieldId=field_id,
        boardId=TEST_BOARD_ID,
        hidden=True,
        description="Updated test description"
    )
    edit_response = client.edit_board_custom_field(edit_request)
    
    assert edit_response.type == "EditBoardCustomField"
    assert edit_response.custom_field.id == field_id
    assert edit_response.custom_field.name == "Test Field"
    assert edit_response.custom_field.type == CustomFieldType.TEXT
    assert edit_response.custom_field.hidden is True
    assert edit_response.custom_field.description == "Updated test description"
    
    # Additional check: field has been updated in the board
    board = client.get_board(TEST_BOARD_ID).payload["board"]
    found = False
    for cf in (board.custom_fields or []):
        if cf.id == field_id:
            assert cf.hidden is True
            assert cf.description == "Updated test description"
            found = True
    assert found, "Updated custom field not found in board"

def test_create_board_group():
    client = get_test_client()
    request = CreateBoardGroupRequest(
        name="Test Board Group",
        boardId=TEST_BOARD_ID,
        description="A group for testing"
    )
    response = client.create_board_group(request)
    assert isinstance(response, CreateBoardGroupResponse)
    assert response.type == "CreateBoardGroup"

    board_groups = response.board_groups
    assert isinstance(board_groups, list)

    # Check if the new group is in the list
    new_group = next((g for g in board_groups if g.name == "Test Board Group"), None)
    assert new_group is not None
    assert new_group.description == "A group for testing"

    # Also check if it's in the board's groups list
    board = client.get_board(TEST_BOARD_ID).payload["board"]
    found = False
    for group in (board.groups or []):
        if group.id == new_group.id:
            assert group.name == "Test Board Group"
            found = True
    assert found, "Created board group not found in board"

def test_edit_board_group():
    client = get_test_client()

    # First, create a group to get an ID
    create_request = CreateBoardGroupRequest(
        name="Group to be Edited",
        boardId=TEST_BOARD_ID
    )
    create_response = client.create_board_group(create_request)
    group_to_edit = next((g for g in create_response.board_groups if g.name == "Group to be Edited"), None)
    assert group_to_edit is not None, "Failed to create group for editing"
    
    # Now, edit the group
    edit_request = EditBoardGroupRequest(
        boardGroupId=group_to_edit.id,
        boardId=TEST_BOARD_ID,
        name="Edited Group",
        description="This group was edited",
        limit=50,
        hidden=False
    )
    edit_response = client.edit_board_group(edit_request)

    assert isinstance(edit_response, EditBoardGroupResponse)
    assert edit_response.type == "EditBoardGroup"
    
    edited_group = next((g for g in edit_response.board_groups if g.id == group_to_edit.id), None)
    assert edited_group is not None, "Edited group not found in response"
    assert edited_group.name == "Edited Group"
    assert edited_group.description == "This group was edited"
    assert edited_group.limit == 50
    assert edited_group.hidden is False 