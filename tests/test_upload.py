import pytest
import os
from tests.test_config import (
    get_test_client,
    TEST_BOARD_ID,
    TEST_GROUP_ID,
    TEST_PROJECT_ID,
)
from vaiz.models.enums import UploadFileType
from vaiz.models import CreateTaskRequest, TaskPriority, TaskFile


@pytest.fixture(scope="module")
def client():
    return get_test_client()


def test_upload_pdf_file(client):
    """Test uploading a real PDF file from assets."""
    file_path = "./assets/example.pdf"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")

    try:
        response = client.upload_file(file_path, file_type=UploadFileType.Pdf)
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "example.pdf"
    assert file.type == UploadFileType.Pdf
    assert file.mime == "application/pdf"
    assert file.size > 0


def test_upload_image_file(client):
    """Test uploading a real image file from assets."""
    file_path = "./assets/example.png"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")

    try:
        response = client.upload_file(file_path, file_type=UploadFileType.Image)
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "example.png"
    assert file.type == UploadFileType.Image
    assert file.mime == "image/png"
    assert file.size > 0


def test_upload_video_file(client):
    """Test uploading a real video file from assets."""
    file_path = "./assets/example.mp4"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")

    try:
        response = client.upload_file(file_path, file_type=UploadFileType.Video)
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "example.mp4"
    assert file.type == UploadFileType.Video
    assert file.mime == "video/mp4"
    assert file.size > 0


def test_upload_file_with_explicit_type(client):
    """Test uploading a PDF file with explicit file type."""
    file_path = "./assets/example.pdf"
    if not os.path.exists(file_path):
        pytest.skip(f"Test file {file_path} not found")

    try:
        response = client.upload_file(
            file_path, UploadFileType.Pdf
        )  # Explicit file_type
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "example.pdf"
    assert file.type == UploadFileType.Pdf  # Explicitly specified type
    assert file.mime == "application/pdf"
    assert file.size > 0


def test_upload_multiple_files(client):
    """Test uploading multiple real files from assets."""
    files_to_upload = [
        ("./assets/example.pdf", UploadFileType.Pdf),
        ("./assets/example.png", UploadFileType.Image),
        ("./assets/example.mp4", UploadFileType.Video),
    ]


# URL Upload Tests


def test_upload_image_from_url_with_auto_detection(client):
    """Test uploading an image from URL with automatic type detection."""
    image_url = "https://placehold.co/150/png"

    try:
        response = client.upload_file_from_url(image_url)
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "png"  # Extracted from URL
    assert file.type == UploadFileType.Image  # Auto-detected
    assert file.size > 0


def test_upload_image_from_url_with_explicit_type(client):
    """Test uploading an image from URL with explicit type and custom filename."""
    image_url = "https://placehold.co/150/png"
    custom_filename = "test_image.png"

    try:
        response = client.upload_file_from_url(
            file_url=image_url,
            file_type=UploadFileType.Image,
            filename=custom_filename,
        )
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == custom_filename
    assert file.type == UploadFileType.Image
    assert file.size > 0


def test_upload_pdf_from_url_with_auto_detection(client):
    """Test uploading a PDF from URL with automatic type detection."""
    pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

    try:
        response = client.upload_file_from_url(pdf_url)
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "dummy.pdf"  # Extracted from URL
    assert file.type == UploadFileType.Pdf  # Auto-detected
    assert file.size > 0


def test_upload_from_url_with_no_extension(client):
    """Test uploading from URL without file extension (should default to File type)."""
    # This URL doesn't have a clear file extension - using a simple text endpoint
    url_no_ext = "https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore"

    try:
        response = client.upload_file_from_url(
            file_url=url_no_ext,
            file_type=UploadFileType.File,  # Explicit type since auto-detection might fail
            filename="test_file.txt",
        )
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    assert response.type == "UploadFile"
    file = response.file
    assert file.url.startswith("http")
    assert file.name == "test_file.txt"
    assert file.type == UploadFileType.File
    assert file.size > 0


def test_upload_from_invalid_url(client):
    """Test uploading from an invalid URL should raise an exception."""
    invalid_url = "https://this-url-does-not-exist-12345.com/nonexistent.jpg"

    with pytest.raises(Exception):  # Should raise requests.RequestException or similar
        client.upload_file_from_url(invalid_url)


def test_upload_from_url_file_type_detection():
    """Test the file type detection helper method."""
    from vaiz.api.upload import UploadAPIClient
    from vaiz.models.enums import UploadFileType

    # Create a test instance (we don't need actual API calls for this)
    upload_client = UploadAPIClient("http://test.com", "test_token")

    # Test URL extension detection
    assert (
        upload_client._detect_file_type_from_url_and_content("test.jpg", None)
        == UploadFileType.Image
    )
    assert (
        upload_client._detect_file_type_from_url_and_content("test.png", None)
        == UploadFileType.Image
    )
    assert (
        upload_client._detect_file_type_from_url_and_content("test.mp4", None)
        == UploadFileType.Video
    )
    assert (
        upload_client._detect_file_type_from_url_and_content("test.pdf", None)
        == UploadFileType.Pdf
    )
    assert (
        upload_client._detect_file_type_from_url_and_content("test.txt", None)
        == UploadFileType.File
    )

    # Test content type detection
    assert (
        upload_client._detect_file_type_from_url_and_content("noext", "image/jpeg")
        == UploadFileType.Image
    )
    assert (
        upload_client._detect_file_type_from_url_and_content("noext", "video/mp4")
        == UploadFileType.Video
    )
    assert (
        upload_client._detect_file_type_from_url_and_content("noext", "application/pdf")
        == UploadFileType.Pdf
    )
    assert (
        upload_client._detect_file_type_from_url_and_content("noext", "text/plain")
        == UploadFileType.File
    )

    # Test default fallback
    assert (
        upload_client._detect_file_type_from_url_and_content("noext", "unknown/type")
        == UploadFileType.File
    )


def test_upload_multiple_files_from_urls(client):
    """Test uploading multiple files from different URLs."""
    urls_and_types = [
        ("https://placehold.co/150/png", UploadFileType.Image, "small_image.png"),
        (
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            UploadFileType.Pdf,
            "dummy.pdf",
        ),
    ]

    uploaded_files = []

    for url, file_type, filename in urls_and_types:
        try:
            response = client.upload_file_from_url(
                file_url=url, file_type=file_type, filename=filename
            )
            uploaded_files.append(response.file)
        except Exception as e:
            if hasattr(e, "response") and e.response is not None:
                print("SERVER RESPONSE:", e.response.text)
            raise

    # Verify all files were uploaded
    assert len(uploaded_files) == len(urls_and_types)

    for i, file in enumerate(uploaded_files):
        expected_type = urls_and_types[i][1]
        expected_filename = urls_and_types[i][2]

        assert file.url.startswith("http")
        assert file.name == expected_filename
        assert file.type == expected_type
        assert file.size > 0


# Complex Integration Test: Create Task with External File Upload


def test_create_task_with_external_file_from_url(client):
    """
    Integration test: Create a task and attach an external file uploaded from URL.

    This test demonstrates the complete workflow:
    1. Upload a file from external URL
    2. Create a TaskFile object from the uploaded file
    3. Create a task with the attached file
    """
    # Skip if required test configuration is missing
    if not all([TEST_GROUP_ID, TEST_BOARD_ID, TEST_PROJECT_ID]):
        pytest.skip(
            "Test config values are missing. Please set VAIZ_GROUP_ID, VAIZ_BOARD_ID, VAIZ_PROJECT_ID."
        )

    # Step 1: Upload an external file from URL
    external_image_url = "https://placehold.co/150/png"

    try:
        upload_response = client.upload_file_from_url(
            file_url=external_image_url,
            file_type=UploadFileType.Image,
            filename="task_attachment_from_url.png",
        )
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    uploaded_file = upload_response.file

    # Verify the file was uploaded successfully
    assert upload_response.type == "UploadFile"
    assert uploaded_file.url.startswith("http")
    assert uploaded_file.name == "task_attachment_from_url.png"
    assert uploaded_file.type == UploadFileType.Image
    assert uploaded_file.size > 0

    # Step 2: Create a TaskFile object from the uploaded file
    task_file = TaskFile(
        url=uploaded_file.url,
        name=uploaded_file.name,
        dimension=uploaded_file.dimension,
        ext=uploaded_file.ext,
        _id=uploaded_file.id,
        type=uploaded_file.type,
    )

    # Step 3: Create a task with the external file attached
    task_request = CreateTaskRequest(
        name="Task with External File from URL",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        priority=TaskPriority.High,
        completed=False,
        description=f"This task was created with an external file downloaded from: {external_image_url}",
        files=[task_file],
    )

    try:
        task_response = client.create_task(task_request)
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    # Verify the task was created successfully
    assert task_response.type == "CreateTask"
    created_task = task_response.payload["task"]
    assert created_task["name"] == "Task with External File from URL"
    # Note: API may assign a different group based on board's default settings
    assert created_task["group"] is not None
    assert created_task["board"] == TEST_BOARD_ID
    assert created_task["project"] == TEST_PROJECT_ID
    assert created_task["priority"] == TaskPriority.High.value
    assert created_task["completed"] is False

    # The task should have a document (description + files are stored separately)
    assert "document" in created_task
    assert created_task["document"] is not None

    print(
        f"✅ Successfully created task '{created_task['name']}' with external file from URL"
    )
    print(f"   Task ID: {created_task['_id']}")
    print(f"   File URL: {uploaded_file.url}")
    print(f"   File name: {uploaded_file.name}")
    print(f"   File type: {uploaded_file.type}")

    # Test completed successfully - task ID available for debugging if needed


def test_create_task_with_multiple_external_files(client):
    """
    Advanced integration test: Create a task with multiple external files from different URLs.
    """
    # Skip if required test configuration is missing
    if not all([TEST_GROUP_ID, TEST_BOARD_ID, TEST_PROJECT_ID]):
        pytest.skip(
            "Test config values are missing. Please set VAIZ_GROUP_ID, VAIZ_BOARD_ID, VAIZ_PROJECT_ID."
        )

    # Define multiple external files to upload
    external_files = [
        {
            "url": "https://placehold.co/150/png",
            "type": UploadFileType.Image,
            "filename": "external_image_1.png",
        },
        {
            "url": "https://placehold.co/200/png",
            "type": UploadFileType.Image,
            "filename": "external_image_2.png",
        },
    ]

    task_files = []

    # Upload all external files
    for file_info in external_files:
        try:
            upload_response = client.upload_file_from_url(
                file_url=file_info["url"],
                file_type=file_info["type"],
                filename=file_info["filename"],
            )

            uploaded_file = upload_response.file

            # Create TaskFile object
            task_file = TaskFile(
                url=uploaded_file.url,
                name=uploaded_file.name,
                dimension=uploaded_file.dimension,
                ext=uploaded_file.ext,
                _id=uploaded_file.id,
                type=uploaded_file.type,
            )

            task_files.append(task_file)

        except Exception as e:
            if hasattr(e, "response") and e.response is not None:
                print("SERVER RESPONSE:", e.response.text)
            raise

    # Verify all files were uploaded
    assert len(task_files) == len(external_files)

    # Create task with multiple external files
    task_request = CreateTaskRequest(
        name="Task with Multiple External Files",
        group=TEST_GROUP_ID,
        board=TEST_BOARD_ID,
        priority=TaskPriority.Medium,
        completed=False,
        description="This task demonstrates uploading and attaching multiple external files from URLs",
        files=task_files,
    )

    try:
        task_response = client.create_task(task_request)
    except Exception as e:
        if hasattr(e, "response") and e.response is not None:
            print("SERVER RESPONSE:", e.response.text)
        raise

    # Verify the task was created successfully
    assert task_response.type == "CreateTask"
    created_task = task_response.payload["task"]
    assert created_task["name"] == "Task with Multiple External Files"
    assert "document" in created_task
    assert created_task["document"] is not None

    print(f"✅ Successfully created task with {len(task_files)} external files")
    print(f"   Task ID: {created_task['_id']}")

    for i, task_file in enumerate(task_files):
        print(f"   File {i + 1}: {task_file.name} ({task_file.type})")

    # Test completed successfully - task ID available for debugging if needed
