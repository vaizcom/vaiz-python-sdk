import pytest
from tests.test_config import get_test_client

@pytest.fixture(scope="module")
def client():
    return get_test_client()

def test_upload_file(client, tmp_path):
    file_path = tmp_path / "test_upload.pdf"
    file_path.write_bytes(b"%PDF-1.4 test file content")
    try:
        response = client.upload_file(str(file_path), file_type="Pdf")
    except Exception as e:
        if hasattr(e, 'response') and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise
    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "test_upload.pdf"
    assert file.type == "Pdf"
    assert file.mime == "application/pdf"
    assert file.size > 0 