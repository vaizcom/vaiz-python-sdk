from vaiz.client import VaizClient

def test_instantiation():
    client = VaizClient(api_key="test")
    assert client.api_key == "test"