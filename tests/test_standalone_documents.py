"""
Tests for creating standalone documents (Space docs and Personal docs).
These documents appear in document lists, not in tasks.
"""

import pytest
from tests.test_config import get_test_client
from vaiz.models import CreateDocumentRequest, Kind
from vaiz import (
    heading, paragraph, text, 
    bullet_list, ordered_list, list_item,
    table, table_row, table_cell, table_header,
    horizontal_rule, link_text
)


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
    content = [
        heading(1, "📄 SDK Test - Space Document"),
        
        paragraph(
            "This is a ",
            text("standalone Space document", bold=True),
            " created by the Vaiz Python SDK test suite. ",
            "It should appear in the ",
            text("Space docs", italic=True),
            " section."
        ),
        
        horizontal_rule(),
        
        heading(2, "✨ Features Demonstrated"),
        
        bullet_list(
            "Text formatting (bold, italic, code)",
            "Lists (bullet and ordered)",
            "Tables with headers",
            "Horizontal rules",
            "Links"
        ),
        
        heading(2, "📊 Sample Table"),
        
        table(
            table_row(
                table_header("Feature"),
                table_header("Status"),
                table_header("Version")
            ),
            table_row("Document creation", "✅ Working", "0.9.0"),
            table_row("Content helpers", "✅ Working", "0.8.0"),
            table_row("Table headers", "✅ Working", "0.9.0")
        ),
        
        horizontal_rule(),
        
        paragraph(
            text("Learn more: ", bold=True),
            link_text("Vaiz Documentation", "https://docs.vaiz.app")
        )
    ]
    
    # Add content to document
    response = client.replace_json_document(document_id, content)
    assert response is not None
    
    # Verify content was saved via markdown round-trip
    saved = client.get_json_document(document_id)
    assert "root" in saved, "Document should have content"

    markdown = client.get_markdown_document(document_id)
    lines = markdown.splitlines()

    headings = sum(1 for l in lines if l.lstrip().startswith("#"))
    table_separators = sum(1 for l in lines if l.strip().startswith("|") and "---" in l)

    assert headings >= 2, "Should have at least 2 headings"
    assert table_separators >= 1, "Should have at least 1 table"

    print(f"✅ Space document created successfully")
    print(f"   Document ID: {document_id}")
    print(f"   Title: {doc_response.payload.document.title}")
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
    content = [
        heading(1, "📝 Personal Notes - SDK Test"),
        
        paragraph(
            "This is a ",
            text("personal document", bold=True),
            " created by the SDK. ",
            "It should appear in the ",
            text("Personal docs", italic=True),
            " section."
        ),
        
        horizontal_rule(),
        
        heading(2, "🎯 My Tasks Today"),
        
        ordered_list(
            "Review SDK test results",
            "Update documentation",
            "Test new table_header feature",
            "Commit changes to repository"
        ),
        
        heading(2, "💡 Ideas"),
        
        bullet_list(
            list_item(
                paragraph(text("Document Structure", bold=True)),
                bullet_list(
                    "Add more examples",
                    "Create video tutorials"
                )
            ),
            list_item(
                paragraph(text("SDK Improvements", bold=True)),
                bullet_list(
                    "Better error messages",
                    "More helper functions"
                )
            )
        ),
        
        heading(2, "📈 Progress Tracking"),
        
        table(
            table_row(
                table_header("Week"),
                table_header("Tasks Completed"),
                table_header("Status")
            ),
            table_row("Week 1", "12", "✅ Good"),
            table_row("Week 2", "15", "✅ Excellent"),
            table_row("Week 3", "10", "⚠️ Need improvement"),
            table_row(
                table_cell(text("Total", bold=True)),
                table_cell(text("37", bold=True)),
                table_cell("📊")
            )
        ),
        
        horizontal_rule(),
        
        heading(2, "🔗 Useful Links"),
        
        paragraph(
            "• ", link_text("Vaiz Docs", "https://docs.vaiz.app"), "\n",
            "• ", link_text("Python SDK", "https://github.com/vaiz/vaiz-python-sdk"), "\n",
            "• ", link_text("API Reference", "https://api.vaiz.app")
        ),
        
        horizontal_rule(),
        
        paragraph(
            text("Created with: ", italic=True),
            text("Vaiz Python SDK", code=True)
        )
    ]
    
    # Add content to document
    response = client.replace_json_document(document_id, content)
    assert response is not None
    
    # Verify content was saved via markdown round-trip
    saved = client.get_json_document(document_id)
    assert "root" in saved, "Document should have content"

    markdown = client.get_markdown_document(document_id)
    lines = markdown.splitlines()

    headings = sum(1 for l in lines if l.lstrip().startswith("#"))
    table_separators = sum(1 for l in lines if l.strip().startswith("|") and "---" in l)
    bullet_items = sum(1 for l in lines if l.lstrip().startswith("- "))
    ordered_items = sum(1 for l in lines if l.lstrip()[:3] in ("1. ", "2. ", "3. ", "4. "))

    assert headings >= 4, "Should have at least 4 headings"
    assert table_separators >= 1, "Should have at least 1 table"
    assert bullet_items >= 2, "Should have bullet lists"
    assert ordered_items >= 3, "Should have ordered list"

    print(f"✅ Personal document created successfully")
    print(f"   Document ID: {document_id}")
    print(f"   Title: {doc_response.payload.document.title}")
    print(f"   Headings: {headings}, Tables: {table_separators}")
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

