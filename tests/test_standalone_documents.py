"""
Tests for creating standalone documents (Space docs and Personal docs).
These documents appear in document lists, not in tasks.
"""

import pytest
from tests.test_config import get_test_client
from tests.lexical_utils import root_children
from vaiz.models import CreateDocumentRequest, Kind


def test_create_space_document_with_content():
    """Create a standalone Space document (appears in Space docs section)."""
    client = get_test_client()
    
    # Create Space document
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
    
    # Add comprehensive content
    markdown = """# 📄 SDK Test - Space Document

This is a **standalone Space document** created by the Vaiz Python SDK test suite. It should appear in the *Space docs* section.

---

## ✨ Features Demonstrated

- Text formatting (bold, italic, code)
- Lists (bullet and ordered)
- Tables with headers
- Horizontal rules
- Links

## 📊 Sample Table

| Feature | Status | Version |
| --- | --- | --- |
| Document creation | ✅ Working | 0.9.0 |
| Markdown content | ✅ Working | 1.0.0 |
| Table headers | ✅ Working | 0.9.0 |

---

**Learn more:** [Vaiz Documentation](https://docs.vaiz.app)
"""

    # Add content to document
    response = client.replace_markdown_document(document_id, markdown)
    assert response is not None
    
    # Verify content was saved
    saved = client.get_json_document(document_id)
    saved_blocks = root_children(saved)
    
    assert len(saved_blocks) > 0, "Document should have content blocks"
    
    # Verify we have headings and tables
    headings = sum(1 for b in saved_blocks if b.get("type") == "heading")
    tables = sum(1 for b in saved_blocks if b.get("type") == "table")
    
    assert headings >= 2, "Should have at least 2 headings"
    assert tables >= 1, "Should have at least 1 table"
    
    print(f"✅ Space document created successfully")
    print(f"   Document ID: {document_id}")
    print(f"   Title: {doc_response.payload.document.title}")
    print(f"   Content blocks: {len(saved_blocks)}")
    print(f"   Location: Space docs section")


def test_create_personal_document_with_content():
    """Create a standalone Member (Personal) document."""
    client = get_test_client()
    
    # Get member ID for personal documents
    profile = client.get_profile()
    member_id = profile.profile.member_id
    
    # Create Personal document
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
    
    # Add comprehensive content
    markdown = """# 📝 Personal Notes - SDK Test

This is a **personal document** created by the SDK. It should appear in the *Personal docs* section.

---

## 🎯 My Tasks Today

1. Review SDK test results
2. Update documentation
3. Test markdown tables
4. Commit changes to repository

## 💡 Ideas

- **Document Structure**
    - Add more examples
    - Create video tutorials
- **SDK Improvements**
    - Better error messages
    - More examples

## 📈 Progress Tracking

| Week | Tasks Completed | Status |
| --- | --- | --- |
| Week 1 | 12 | ✅ Good |
| Week 2 | 15 | ✅ Excellent |
| Week 3 | 10 | ⚠️ Need improvement |
| **Total** | **37** | 📊 |

---

## 🔗 Useful Links

- [Vaiz Docs](https://docs.vaiz.app)
- [Python SDK](https://github.com/vaizcom/vaiz-python-sdk)

---

*Created with:* `Vaiz Python SDK`
"""

    # Add content to document
    response = client.replace_markdown_document(document_id, markdown)
    assert response is not None
    
    # Verify content was saved
    saved = client.get_json_document(document_id)
    saved_blocks = root_children(saved)
    
    assert len(saved_blocks) > 0, "Document should have content blocks"
    
    # Count elements
    headings = sum(1 for b in saved_blocks if b.get("type") == "heading")
    tables = sum(1 for b in saved_blocks if b.get("type") == "table")
    bullet_lists = sum(1 for b in saved_blocks if b.get("type") == "list" and b.get("listType") == "bullet")
    ordered_lists = sum(1 for b in saved_blocks if b.get("type") == "list" and b.get("listType") == "number")
    
    assert headings >= 4, "Should have at least 4 headings"
    assert tables >= 1, "Should have at least 1 table"
    assert bullet_lists >= 1, "Should have bullet lists"
    assert ordered_lists >= 1, "Should have ordered list"
    
    print(f"✅ Personal document created successfully")
    print(f"   Document ID: {document_id}")
    print(f"   Title: {doc_response.payload.document.title}")
    print(f"   Content blocks: {len(saved_blocks)}")
    print(f"   Headings: {headings}, Tables: {tables}")
    print(f"   Location: Personal docs section")


if __name__ == "__main__":
    print("Creating standalone documents...")
    print("\n" + "="*60)
    test_create_space_document_with_content()
    print("\n" + "="*60)
    test_create_personal_document_with_content()
    print("\n" + "="*60)
    print("\n✅ All standalone documents created!")
    print("Check your Vaiz interface:")
    print("  - Space docs: Should see 'SDK Test - Space Document'")
    print("  - Personal docs: Should see 'SDK Test Document - Member (Personal)'")

