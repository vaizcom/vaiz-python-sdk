import pytest
from vaiz.models import BoardsResponse, Board, BoardResponse
from tests.test_config import get_test_client, TEST_BOARD_ID

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