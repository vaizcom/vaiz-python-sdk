import pytest
from vaiz.models import BoardsResponse, Board
from tests.test_config import get_test_client

def test_get_boards_real():
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