import pytest
from tests.test_config import get_test_client

@pytest.fixture(scope="module")
def client():
    return get_test_client()