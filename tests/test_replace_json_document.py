"""
Tests for replaceJSONDocument API endpoint.
"""

import pytest
from tests.test_config import get_test_client


def test_replace_json_document():
    """Test replacing document content with JSON content."""
    client = get_test_client()
    
    # Create a simple JSON content structure
    json_content = [
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Test content from replace_json_document"}
            ]
        }
    ]
    
    # Use a known document ID from your test environment
    # or create a task first to get a document ID
    from vaiz.models import CreateTaskRequest, TaskPriority, Kind
    
    # Get first board to use
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create a test task
    task_request = CreateTaskRequest(
        name="Test Task for JSON Document Replacement",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Initial description"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    assert document_id, "Task should have a document ID"
    
    # Replace document content with JSON
    response = client.replace_json_document(
        document_id=document_id,
        content=json_content
    )
    
    # Response should be successful (empty response object)
    assert response is not None
    
    # Verify content was updated by fetching it
    updated_content = client.get_json_document(document_id)
    assert updated_content is not None
    
    print(f"✅ Successfully replaced document {document_id} with JSON content")


def test_replace_json_document_with_rich_content():
    """Test replacing document with rich formatted JSON content."""
    client = get_test_client()
    
    # Create rich JSON content with various formatting
    rich_content = [
        {
            "type": "heading",
            "attrs": {"level": 1},
            "content": [
                {"type": "text", "text": "Rich Content Test"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "This is "},
                {
                    "type": "text",
                    "marks": [{"type": "bold"}],
                    "text": "bold text"
                },
                {"type": "text", "text": " and this is "},
                {
                    "type": "text",
                    "marks": [{"type": "italic"}],
                    "text": "italic text"
                },
                {"type": "text", "text": "."}
            ]
        },
        {
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": "First item"}
                            ]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "text": "Second item"}
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Link: "},
                {
                    "type": "text",
                    "marks": [
                        {
                            "type": "link",
                            "attrs": {
                                "href": "https://vaiz.app",
                                "target": "_blank"
                            }
                        }
                    ],
                    "text": "Vaiz"
                }
            ]
        }
    ]
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create a test task
    from vaiz.models import CreateTaskRequest, TaskPriority
    
    task_request = CreateTaskRequest(
        name="Test Task for Rich JSON Content",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Will be replaced"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Replace with rich content
    response = client.replace_json_document(
        document_id=document_id,
        content=rich_content
    )
    
    assert response is not None
    
    # Verify content was updated
    updated_content = client.get_json_document(document_id)
    assert updated_content is not None
    
    print(f"✅ Successfully replaced document {document_id} with rich JSON content")


def test_replace_json_document_empty_content():
    """Test replacing document with empty JSON content."""
    client = get_test_client()
    
    # Empty content array
    empty_content = []
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create a test task
    from vaiz.models import CreateTaskRequest, TaskPriority
    
    task_request = CreateTaskRequest(
        name="Test Task for Empty JSON Content",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Original content"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Replace with empty content
    response = client.replace_json_document(
        document_id=document_id,
        content=empty_content
    )
    
    assert response is not None
    
    print(f"✅ Successfully cleared document {document_id} content")


def test_replace_json_document_complex_structure():
    """Test replacing document with complex multi-level structure using only supported document elements."""
    client = get_test_client()
    
    # Complex document structure with ONLY validated working document elements:
    # - paragraph, heading, text, bulletList, orderedList, listItem
    # - marks: bold, italic, code, link
    complex_content = [
        # Title
        {
            "type": "heading",
            "attrs": {"level": 1},
            "content": [
                {"type": "text", "text": "📚 Comprehensive Project Documentation"}
            ]
        },
        # Subtitle with formatting
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "marks": [{"type": "italic"}], "text": "Last updated: 2025-10-22 | "},
                {"type": "text", "marks": [{"type": "bold"}], "text": "Status: Active"}
            ]
        },
        # Separator paragraph
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"}
            ]
        },
        # Overview section
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [
                {"type": "text", "text": "📋 Project Overview"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "This document provides a "},
                {"type": "text", "marks": [{"type": "bold"}], "text": "comprehensive overview"},
                {"type": "text", "text": " of the project architecture, implementation details, and "},
                {
                    "type": "text",
                    "marks": [
                        {"type": "link", "attrs": {"href": "https://vaiz.app/roadmap", "target": "_blank"}}
                    ],
                    "text": "roadmap"
                },
                {"type": "text", "text": "."}
            ]
        },
        # Key Features with bullet list
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [
                {"type": "text", "text": "✨ Key Features"}
            ]
        },
        {
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "marks": [{"type": "bold"}], "text": "Real-time collaboration: "},
                                {"type": "text", "text": "Multiple users can work simultaneously"}
                            ]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "marks": [{"type": "bold"}], "text": "Rich text editing: "},
                                {"type": "text", "text": "Support for "},
                                {"type": "text", "marks": [{"type": "italic"}], "text": "formatting"},
                                {"type": "text", "text": ", "},
                                {"type": "text", "marks": [{"type": "code"}], "text": "code"},
                                {"type": "text", "text": ", and more"}
                            ]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "marks": [{"type": "bold"}], "text": "API Integration: "},
                                {"type": "text", "text": "Comprehensive REST API with Python SDK"}
                            ]
                        },
                        # Nested list
                        {
                            "type": "bulletList",
                            "content": [
                                {
                                    "type": "listItem",
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "content": [
                                                {"type": "text", "text": "Task management"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "listItem",
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "content": [
                                                {"type": "text", "text": "Document collaboration"}
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "listItem",
                                    "content": [
                                        {
                                            "type": "paragraph",
                                            "content": [
                                                {"type": "text", "text": "Custom field management"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        # Technical Stack section
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [
                {"type": "text", "text": "🛠 Technical Stack"}
            ]
        },
        # Ordered list
        {
            "type": "orderedList",
            "attrs": {"start": 1},
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "marks": [{"type": "bold"}], "text": "Backend: "},
                                {"type": "text", "text": "Node.js, MongoDB, Redis"}
                            ]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "marks": [{"type": "bold"}], "text": "Frontend: "},
                                    {"type": "text", "text": "React, TypeScript, Rich Editor"}
                            ]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "marks": [{"type": "bold"}], "text": "SDK: "},
                                {"type": "text", "text": "Python 3.8+"}
                            ]
                        }
                    ]
                }
            ]
        },
        # Code example section (using inline code instead of codeBlock)
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [
                {"type": "text", "text": "💻 Quick Start"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Install the SDK: "},
                {"type": "text", "marks": [{"type": "code"}], "text": "pip install vaiz-sdk"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Initialize the client:"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "marks": [{"type": "code"}], "text": "from vaiz import VaizClient"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "marks": [{"type": "code"}], "text": "client = VaizClient(token=\"your_token\")"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "marks": [{"type": "code"}], "text": "task = client.get_task(\"PRJ-123\")"}
            ]
        },
        # Important notes section (using bold paragraph instead of blockquote)
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [
                {"type": "text", "text": "💡 Important Notes"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "marks": [{"type": "bold"}], "text": "Security Notice: "},
                {"type": "text", "text": "Always store your API token securely. Never commit tokens to version control. Use environment variables or secure vault solutions."}
            ]
        },
        # Implementation timeline (removed strikethrough mark)
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [
                {"type": "text", "text": "📅 Implementation Timeline"}
            ]
        },
        {
            "type": "orderedList",
            "attrs": {"start": 1},
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "marks": [{"type": "bold"}], "text": "Phase 1: "},
                                {"type": "text", "text": "Core API development "},
                                {"type": "text", "marks": [{"type": "code"}], "text": "✓ Completed"}
                            ]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "marks": [{"type": "bold"}], "text": "Phase 2: "},
                                {"type": "text", "text": "Python SDK implementation "},
                                {"type": "text", "marks": [{"type": "code"}], "text": "⏳ In Progress"}
                            ]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {"type": "text", "marks": [{"type": "bold"}], "text": "Phase 3: "},
                                {"type": "text", "text": "Advanced features (webhooks, real-time) "},
                                {"type": "text", "marks": [{"type": "code"}], "text": "📋 Planned"}
                            ]
                        }
                    ]
                }
            ]
        },
        # Resources section with mixed formatting
        {
            "type": "heading",
            "attrs": {"level": 2},
            "content": [
                {"type": "text", "text": "🔗 Resources"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Official links:"}
            ]
        },
        {
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "marks": [{"type": "link", "attrs": {"href": "https://docs.vaiz.app", "target": "_blank"}}],
                                    "text": "Documentation"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "marks": [{"type": "link", "attrs": {"href": "https://github.com/vaizcom/vaiz-python-sdk", "target": "_blank"}}],
                                    "text": "GitHub Repository"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "marks": [{"type": "link", "attrs": {"href": "https://vaiz.app/community", "target": "_blank"}}],
                                    "text": "Community Forum"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        # Footer (using separator paragraph instead of horizontalRule)
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"}
            ]
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "marks": [{"type": "italic"}], "text": "This document was generated programmatically using the "},
                {"type": "text", "marks": [{"type": "code"}], "text": "replace_json_document"},
                {"type": "text", "marks": [{"type": "italic"}], "text": " API method."}
            ]
        }
    ]
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create a test task
    from vaiz.models import CreateTaskRequest, TaskPriority
    
    task_request = CreateTaskRequest(
        name="Test Task with Complex Document Structure",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="Will be replaced with complex content"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Replace with complex structure
    response = client.replace_json_document(
        document_id=document_id,
        content=complex_content
    )
    
    assert response is not None
    
    # Verify content was updated
    updated_content = client.get_json_document(document_id)
    assert updated_content is not None
    
    print(f"✅ Successfully replaced document {document_id} with complex structure")
    print(f"   Structure includes: headings, lists (nested), inline code, links, and formatting")


def test_replace_json_document_complete_replacement():
    """Test that replace_json_document COMPLETELY replaces old content (strict test)."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create a test task with SPECIFIC initial content
    from vaiz.models import CreateTaskRequest, TaskPriority
    
    task_request = CreateTaskRequest(
        name="Test Complete JSON Replacement",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="OLD_CONTENT_MARKER - This text should be completely removed after replacement"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Verify initial content exists
    initial_content = client.get_json_document(document_id)
    initial_text = str(initial_content)
    assert "OLD_CONTENT_MARKER" in initial_text, "Initial content should contain marker"
    
    # Replace with completely NEW content
    new_content = [
        # Heading with NEW marker
        {
            "type": "heading",
            "attrs": {"level": 1},
            "content": [
                {"type": "text", "text": "NEW_CONTENT_MARKER - Verified Structure"}
            ]
        },
        # Paragraph with formatting
        {
            "type": "paragraph",
            "content": [
                {"type": "text", "text": "Text with "},
                {"type": "text", "marks": [{"type": "bold"}], "text": "bold"},
                {"type": "text", "text": ", "},
                {"type": "text", "marks": [{"type": "italic"}], "text": "italic"},
                {"type": "text", "text": ", and "},
                {"type": "text", "marks": [{"type": "code"}], "text": "code"}
            ]
        },
        # Link
        {
            "type": "paragraph",
            "content": [
                {
                    "type": "text",
                    "marks": [
                        {"type": "link", "attrs": {"href": "https://vaiz.app", "target": "_blank"}}
                    ],
                    "text": "Link to Vaiz"
                }
            ]
        },
        # Bullet list
        {
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "Bullet item 1"}]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "Bullet item 2"}]
                        }
                    ]
                }
            ]
        },
        # Ordered list
        {
            "type": "orderedList",
            "attrs": {"start": 1},
            "content": [
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "Ordered step 1"}]
                        }
                    ]
                },
                {
                    "type": "listItem",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": "Ordered step 2"}]
                        }
                    ]
                }
            ]
        }
    ]
    
    # Replace
    response = client.replace_json_document(
        document_id=document_id,
        content=new_content
    )
    
    assert response is not None
    
    # Retrieve and STRICTLY verify replacement
    saved_content = client.get_json_document(document_id)
    saved_text = str(saved_content)
    
    # CRITICAL: Old content MUST be completely gone
    assert "OLD_CONTENT_MARKER" not in saved_text, "OLD CONTENT STILL EXISTS! API did not replace, it appended!"
    
    # CRITICAL: New content MUST be present
    assert "NEW_CONTENT_MARKER" in saved_text, "New content not found"
    assert "Verified Structure" in saved_text, "New heading not found"
    
    # Verify structure elements are saved correctly
    saved_blocks = saved_content.get("default", {}).get("content", [])
    
    # Verify we have all expected block types
    block_types = [block.get("type") for block in saved_blocks]
    assert "heading" in block_types, "Heading not saved"
    assert "paragraph" in block_types, "Paragraph not saved"
    assert "bulletList" in block_types, "Bullet list not saved"
    assert "orderedList" in block_types, "Ordered list not saved"
    
    # Verify marks are preserved
    assert "bold" in saved_text, "Bold formatting not preserved"
    assert "italic" in saved_text, "Italic formatting not preserved"
    assert "code" in saved_text, "Code formatting not preserved"
    assert "vaiz.app" in saved_text, "Link not preserved"
    
    print(f"✅ STRICT TEST PASSED: Complete replacement verified")
    print(f"   ✓ Old content removed (OLD_CONTENT_MARKER not found)")
    print(f"   ✓ New content present (NEW_CONTENT_MARKER found)")
    print(f"   ✓ All structure elements preserved")
    print(f"   ✓ All formatting marks preserved")


def test_replace_document_complete_replacement():
    """Test that replace_document COMPLETELY replaces old content (strict test)."""
    client = get_test_client()
    
    # Get first board
    boards = client.get_boards()
    if not boards or not boards.boards:
        pytest.skip("No boards available for testing")
    
    board = boards.boards[0]
    
    # Create a test task with SPECIFIC initial content
    from vaiz.models import CreateTaskRequest, TaskPriority
    
    task_request = CreateTaskRequest(
        name="Test Complete Plain Text Replacement",
        group=client.space_id,
        board=board.id,
        priority=TaskPriority.General,
        description="PLAIN_OLD_MARKER - This plain text should be completely removed"
    )
    
    task_response = client.create_task(task_request)
    document_id = task_response.task.document
    
    # Verify initial content exists
    initial_content = client.get_json_document(document_id)
    initial_text = str(initial_content)
    assert "PLAIN_OLD_MARKER" in initial_text, "Initial content should contain marker"
    
    # Replace with completely NEW plain text
    new_description = "PLAIN_NEW_MARKER - This is the new content. The old content should be gone."
    
    response = client.replace_document(
        document_id=document_id,
        description=new_description
    )
    
    assert response is not None
    
    # Retrieve and STRICTLY verify replacement
    saved_content = client.get_json_document(document_id)
    saved_text = str(saved_content)
    
    # CRITICAL: Old content MUST be completely gone
    assert "PLAIN_OLD_MARKER" not in saved_text, "OLD CONTENT STILL EXISTS! API did not replace, it appended!"
    
    # CRITICAL: New content MUST be present
    assert "PLAIN_NEW_MARKER" in saved_text, "New content not found"
    assert "new content" in saved_text, "New description text not found"
    
    print(f"✅ STRICT TEST PASSED: Complete plain text replacement verified")
    print(f"   ✓ Old content removed (PLAIN_OLD_MARKER not found)")
    print(f"   ✓ New content present (PLAIN_NEW_MARKER found)")


if __name__ == "__main__":
    print("Running replace_json_document tests...")
    test_replace_json_document()
    test_replace_json_document_with_rich_content()
    test_replace_json_document_empty_content()
    test_replace_json_document_complex_structure()
    test_replace_json_document_complete_replacement()
    test_replace_document_complete_replacement()
    print("All tests passed! ✅")

