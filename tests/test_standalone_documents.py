"""
Tests for creating standalone documents (Space docs and Personal docs).
These documents appear in document lists, not in tasks.
"""

import pytest
from tests.test_config import get_test_client
from vaiz.models import CreateDocumentRequest, Kind


def test_create_space_document_with_content():
    """Create a standalone Space document (appears in Space docs section)."""
    client = get_test_client()

    doc_response = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Space,
            kind_id=client.space_id,
            title="SDK Test - Space Document",
            index=0
        )
    )

    document_id = doc_response.payload.document.id
    assert document_id is not None

    markdown = (
        "# SDK Test - Space Document\n\n"
        "This is a **standalone Space document** created by the Vaiz Python SDK "
        "test suite. It should appear in the *Space docs* section.\n\n"
        "---\n\n"
        "## Features Demonstrated\n\n"
        "- Text formatting (bold, italic, code)\n"
        "- Lists (bullet and ordered)\n"
        "- Tables with headers\n"
        "- Horizontal rules\n"
        "- Links\n\n"
        "## Sample Table\n\n"
        "| Feature | Status | Version |\n"
        "| --- | --- | --- |\n"
        "| Document creation | Working | 1.0.0 |\n"
        "| Markdown content | Working | 1.0.0 |\n\n"
        "---\n\n"
        "**Learn more:** [Vaiz Documentation](https://docs.vaiz.app)"
    )

    response = client.replace_markdown_document(document_id, markdown)
    assert response is not None

    # Verify content was saved via markdown round-trip
    saved = client.get_markdown_document(document_id)
    lines = saved.splitlines()

    headings = sum(1 for l in lines if l.lstrip().startswith("#"))
    table_separators = sum(1 for l in lines if l.strip().startswith("|") and "---" in l)

    assert headings >= 2, "Should have at least 2 headings"
    assert table_separators >= 1, "Should have at least 1 table"

    print(f"✅ Space document created successfully")
    print(f"   Document ID: {document_id}")
    print(f"   Title: {doc_response.payload.document.title}")


def test_create_personal_document_with_content():
    """Create a standalone Member (Personal) document."""
    client = get_test_client()

    profile = client.get_profile()
    member_id = profile.profile.member_id

    doc_response = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Member,
            kind_id=member_id,
            title="SDK Test Document - Member (Personal)",
            index=0
        )
    )

    document_id = doc_response.payload.document.id
    assert document_id is not None

    markdown = (
        "# Personal Notes - SDK Test\n\n"
        "This is a **personal document** created by the SDK. "
        "It should appear in the *Personal docs* section.\n\n"
        "---\n\n"
        "## My Tasks Today\n\n"
        "1. Review SDK test results\n"
        "2. Update documentation\n"
        "3. Commit changes to repository\n\n"
        "## Ideas\n\n"
        "- **Documentation**\n"
        "  - Add more examples\n"
        "  - Create video tutorials\n"
        "- **SDK Improvements**\n"
        "  - Better error messages\n"
        "  - More helper functions\n\n"
        "## Progress Tracking\n\n"
        "| Week | Tasks Completed | Status |\n"
        "| --- | --- | --- |\n"
        "| Week 1 | 12 | Good |\n"
        "| Week 2 | 15 | Excellent |\n"
        "| Week 3 | 10 | Needs improvement |\n\n"
        "---\n\n"
        "## Useful Links\n\n"
        "- [Vaiz Docs](https://docs.vaiz.app)\n"
        "- [Python SDK](https://github.com/vaizcom/vaiz-python-sdk)\n\n"
        "*Created with* `Vaiz Python SDK`"
    )

    response = client.replace_markdown_document(document_id, markdown)
    assert response is not None

    saved = client.get_markdown_document(document_id)
    lines = saved.splitlines()

    headings = sum(1 for l in lines if l.lstrip().startswith("#"))
    table_separators = sum(1 for l in lines if l.strip().startswith("|") and "---" in l)
    bullet_items = sum(1 for l in lines if l.lstrip().startswith("- "))
    ordered_items = sum(1 for l in lines if l.lstrip()[:3] in ("1. ", "2. ", "3. "))

    assert headings >= 4, "Should have at least 4 headings"
    assert table_separators >= 1, "Should have at least 1 table"
    assert bullet_items >= 2, "Should have bullet lists"
    assert ordered_items >= 3, "Should have ordered list"

    print(f"✅ Personal document created successfully")
    print(f"   Document ID: {document_id}")
    print(f"   Title: {doc_response.payload.document.title}")
    print(f"   Headings: {headings}, Tables: {table_separators}")
