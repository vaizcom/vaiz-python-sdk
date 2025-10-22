"""
Example: Replace document with complex structure using replaceJSONDocument API.

This example demonstrates creating a comprehensive document with various document structure elements:
- Multiple heading levels
- Rich text formatting (bold, italic, strikethrough, code)
- Bullet lists with nesting
- Ordered lists
- Code blocks with syntax highlighting
- Links with attributes
- Blockquotes
- Horizontal rules
"""

import json
from examples.config import get_client
from vaiz.models import CreateTaskRequest, TaskPriority


def main():
    client = get_client()
    client.verbose = True

    # Create a task to get a document ID
    task = CreateTaskRequest(
        name="Complex Document Structure Demo",
        group=client.space_id,
        board="your_board_id",
        priority=TaskPriority.General,
        description="Initial description"
    )
    
    try:
        task_response = client.create_task(task)
        document_id = task_response.task.document
        print(f"Created task with document ID: {document_id}\n")
        
        # Create comprehensive complex structure
        complex_content = [
            # Main title
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
            
            # Horizontal separator
            {
                "type": "horizontalRule"
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
            
            # Key Features with nested lists
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
            
            # Technical Stack
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [
                    {"type": "text", "text": "🛠 Technical Stack"}
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
            
            # Code examples
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
                    {"type": "text", "text": "Install the SDK:"}
                ]
            },
            {
                "type": "codeBlock",
                "attrs": {"language": "bash"},
                "content": [
                    {"type": "text", "text": "pip install vaiz-sdk"}
                ]
            },
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Initialize the client:"}
                ]
            },
            {
                "type": "codeBlock",
                "attrs": {"language": "python"},
                "content": [
                    {"type": "text", "text": "from vaiz import VaizClient\n\nclient = VaizClient(token=\"your_token\")\ntask = client.get_task(\"PRJ-123\")"}
                ]
            },
            
            # Important notice
            {
                "type": "heading",
                "attrs": {"level": 2},
                "content": [
                    {"type": "text", "text": "💡 Important Notes"}
                ]
            },
            {
                "type": "blockquote",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "marks": [{"type": "bold"}], "text": "Security Notice: "},
                            {"type": "text", "text": "Always store your API token securely. Never commit tokens to version control. Use environment variables or secure vault solutions."}
                        ]
                    }
                ]
            },
            
            # Timeline
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
                                    {"type": "text", "marks": [{"type": "strikethrough"}], "text": "Core API development"},
                                    {"type": "text", "text": " "},
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
            
            # Resources
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
            
            # Footer
            {
                "type": "horizontalRule"
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
        
        # Replace document with complex structure
        print("=== Replacing Document with Complex Structure ===")
        replace_response = client.replace_json_document(
            document_id=document_id,
            content=complex_content
        )
        print("✅ Document content replaced with complex structure!\n")
        
        # Print summary
        print("📊 Document Structure Summary:")
        print("   ✓ Multiple heading levels (H1, H2)")
        print("   ✓ Rich text formatting (bold, italic, strikethrough, code)")
        print("   ✓ Bullet lists with nested sublists")
        print("   ✓ Ordered/numbered lists")
        print("   ✓ Code blocks with syntax highlighting (bash, python)")
        print("   ✓ Hyperlinks with custom attributes")
        print("   ✓ Blockquotes for important notices")
        print("   ✓ Horizontal rules for visual separation")
        print("   ✓ Emoji icons for visual appeal\n")
        
        # Verify the change
        updated_content = client.get_document_body(document_id)
        print(f"🎉 Document {document_id} now contains comprehensive structured content!")
        print(f"📏 Total content blocks: {len(complex_content)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

