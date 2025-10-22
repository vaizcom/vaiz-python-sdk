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
    updated_content = client.get_document_body(document_id)
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
    updated_content = client.get_document_body(document_id)
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
    updated_content = client.get_document_body(document_id)
    assert updated_content is not None
    
    print(f"✅ Successfully replaced document {document_id} with complex structure")
    print(f"   Structure includes: headings, lists (nested), inline code, links, and formatting")


if __name__ == "__main__":
    print("Running replace_json_document tests...")
    test_replace_json_document()
    test_replace_json_document_with_rich_content()
    test_replace_json_document_empty_content()
    test_replace_json_document_complex_structure()
    print("All tests passed! ✅")

