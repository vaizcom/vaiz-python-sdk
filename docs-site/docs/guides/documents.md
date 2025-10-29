---
sidebar_position: 9
sidebar_label: Documents
title: Working with Documents — Rich Content & Formatting | Vaiz Python SDK
description: Learn how to create and manage rich-text documents in Vaiz using the Python SDK. Includes JSON format, blocks, tables, mentions, and formatting.
---

# Documents

Manage task descriptions, rich content, and document lists in Vaiz.

## Document Scopes

Vaiz supports three document scopes:

- **Space** - Shared documents accessible to all space members
- **Member** - Personal documents accessible only to the member
- **Project** - Project documents accessible to project members

## Get Documents List

Retrieve a list of documents by kind and ID:

```python
from vaiz.models import GetDocumentsRequest, Kind

# Get Space documents
space_docs = client.get_documents(
    GetDocumentsRequest(
        kind=Kind.Space,
        kind_id="space_id"
    )
)

# Get Member (personal) documents
member_docs = client.get_documents(
    GetDocumentsRequest(
        kind=Kind.Member,
        kind_id="member_id"
    )
)

# Get Project documents
project_docs = client.get_documents(
    GetDocumentsRequest(
        kind=Kind.Project,
        kind_id="project_id"
    )
)

# Process documents
for doc in project_docs.payload.documents:
    print(f"Document: {doc.title}")
    print(f"  ID: {doc.id}")
    print(f"  Size: {doc.size} bytes")
    print(f"  Creator: {doc.creator}")
    print(f"  Created: {doc.created_at}")
    print(f"  Kind: {doc.kind}")
    print(f"  Followers: {doc.followers}")
```

See [API Reference](../api-reference/documents) for complete Document model definition.

## Creating Documents

You can create new documents in any scope (Space, Member, or Project):

```python
from vaiz.models import CreateDocumentRequest, Kind

# Create a Project document
new_doc = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id="project_id",
        title="Project Documentation",
        index=0,  # Position in document list
        parent_document_id=None  # Optional: for nested documents
    )
)

document = new_doc.payload.document
print(f"Created document: {document.id}")
print(f"Title: {document.title}")
```

### Creating Documents in Different Scopes

```python
# Space document (shared across organization)
space_doc = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Space,
        kind_id=space_id,
        title="Company Wiki",
        index=0
    )
)

# Member document (personal)
personal_doc = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Member,
        kind_id=member_id,
        title="My Notes",
        index=0
    )
)

# Project document
project_doc = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id=project_id,
        title="Project Plan",
        index=0
    )
)
```

### Create and Populate Document

```python
# 1. Create document
response = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id="project_id",
        title="Meeting Notes",
        index=0
    )
)

doc_id = response.payload.document.id

# 2. Add content
content = """
# Meeting Notes

**Date**: 2025-10-21

## Attendees
- John Doe
- Jane Smith

## Discussion
[Meeting content here]
"""

client.replace_document(doc_id, content)
print(f"✅ Document created and populated: {doc_id}")
```

### Creating Document Hierarchies

Create nested document structures for better organization:

```python
# 1. Create parent document
parent = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id=project_id,
        title="Product Documentation",
        index=0
    )
).payload.document

# 2. Create child documents
child1 = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id=project_id,
        title="Getting Started",
        index=0,
        parent_document_id=parent.id  # Link to parent
    )
).payload.document

child2 = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id=project_id,
        title="API Reference",
        index=1,
        parent_document_id=parent.id  # Same parent
    )
).payload.document

# 3. Create nested child (grandchild)
grandchild = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id=project_id,
        title="Quick Start Guide",
        index=0,
        parent_document_id=child1.id  # Nested under child1
    )
).payload.document

print(f"Created hierarchy: {parent.title} -> {child1.title} -> {grandchild.title}")
```

### Multi-Level Structure Example

```python
# Build a complete documentation tree
def create_doc_tree(client, project_id):
    """Create a hierarchical documentation structure."""
    
    # Root
    root = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Project,
            kind_id=project_id,
            title="User Manual",
            index=0
        )
    ).payload.document
    
    # Chapters
    chapters = [
        ("Chapter 1: Introduction", ["Overview", "Installation", "Quick Start"]),
        ("Chapter 2: Features", ["Core Features", "Advanced Features"]),
        ("Chapter 3: Configuration", ["Basic Setup", "Advanced Settings"])
    ]
    
    for chapter_idx, (chapter_title, sections) in enumerate(chapters):
        # Create chapter
        chapter = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Project,
                kind_id=project_id,
                title=chapter_title,
                index=chapter_idx,
                parent_document_id=root.id
            )
        ).payload.document
        
        print(f"📖 {chapter.title}")
        
        # Create sections
        for section_idx, section_title in enumerate(sections):
            section = client.create_document(
                CreateDocumentRequest(
                    kind=Kind.Project,
                    kind_id=project_id,
                    title=section_title,
                    index=section_idx,
                    parent_document_id=chapter.id
                )
            ).payload.document
            
            print(f"  📄 {section.title}")
    
    return root

# Create the tree
root_doc = create_doc_tree(client, project_id)
print(f"\n✅ Created documentation tree with root: {root_doc.id}")
```

## Editing Documents

Update document metadata such as title:

```python
from vaiz.models import EditDocumentRequest

# Edit document title
response = client.edit_document(
    EditDocumentRequest(
        document_id="document_id",
        title="Updated Document Title"
    )
)

edited_doc = response.payload.document
print(f"✅ Updated document: {edited_doc.title}")
```

### Complete Edit Workflow

Create, edit, and verify document changes:

```python
from vaiz import CreateDocumentRequest, EditDocumentRequest, GetDocumentsRequest, Kind

# 1. Create document
create_response = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id=project_id,
        title="Initial Title",
        index=0
    )
)

doc_id = create_response.payload.document.id
print(f"Created: {create_response.payload.document.title}")

# 2. Edit document title
edit_response = client.edit_document(
    EditDocumentRequest(
        document_id=doc_id,
        title="Updated Title"
    )
)

print(f"Updated: {edit_response.payload.document.title}")

# 3. Verify change in document list
docs = client.get_documents(
    GetDocumentsRequest(kind=Kind.Project, kind_id=project_id)
)

updated_doc = next((d for d in docs.payload.documents if d.id == doc_id), None)
if updated_doc:
    print(f"✅ Verified: {updated_doc.title}")
```

## Working with Document Content

In addition to listing and creating documents, you can work with their content using document API methods.

### Get Document Content

Retrieve the JSON content of any document:

```python
# Get document content by ID
content = client.get_json_document("document_id")
print(content)  # Returns parsed JSON structure
```

This method is universal and works for:
- Task descriptions
- Standalone documents
- Any document by its ID

### Replace Document Content (Plain Text)

Replace the entire content of a document with plain text:

```python
# Replace document content with plain text
client.replace_document(
    document_id="document_id",
    description="New content here"
)
```

**Use cases:**
- Updating task descriptions programmatically
- Bulk content updates
- Template-based content generation

### Replace Document Content (Rich JSON)

Replace document content with structured rich content.

**💡 Tip:** Use [Document Structure helper functions](./document-structure-helpers) for type-safe, readable content creation!

```python
# Replace with rich formatted content
json_content = [
    {
        "type": "heading",
        "attrs": {"level": 1},
        "content": [
            {"type": "text", "text": "Project Overview"}
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
            }
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
    }
]

client.replace_json_document(
    document_id="document_id",
    content=json_content
)
```

**Document Structure Format features:**
- **Rich text formatting**: Bold, italic, underline, strikethrough, code
- **Headings**: Multiple levels (h1-h6)
- **Lists**: Bullet lists, numbered lists, task lists
- **Links**: Hyperlinks with custom attributes
- **Code blocks**: Syntax highlighted code
- **Tables**: Structured tabular data
- **And more**: Blockquotes, horizontal rules, mentions, etc.

**Use cases:**
- Creating structured documentation programmatically
- Importing content from other systems with formatting
- Generating reports with rich formatting
- Building document templates with complex layouts

**With helper functions (recommended):**
```python
from vaiz import heading, paragraph, text, bullet_list, link_text, horizontal_rule

content = [
    heading(1, "📚 Documentation"),
    paragraph(
        "Welcome to our ",
        text("project docs", bold=True),
        "!"
    ),
    horizontal_rule(),
    heading(2, "Features"),
    bullet_list(
        "Easy to use",
        "Type-safe",
        "Well documented"
    ),
    paragraph(
        "Learn more at ",
        link_text("our docs", "https://docs.vaiz.app")
    )
]

client.replace_json_document(document_id, content)
```

See [Document Structure Helpers Guide](./document-structure-helpers) for complete documentation.

### Update Project Document

```python
from vaiz.models import GetDocumentsRequest, Kind

# 1. Get all project documents
docs = client.get_documents(
    GetDocumentsRequest(
        kind=Kind.Project,
        kind_id="project_id"
    )
)

# 2. Find specific document
target_doc = next(
    (doc for doc in docs.payload.documents if doc.title == "Meeting Notes"),
    None
)

if target_doc:
    # 3. Get current content
    current_content = client.get_json_document(target_doc.id)
    print(f"Current size: {target_doc.size} bytes")
    
    # 4. Update content
    new_content = """
# Meeting Notes - Updated

## Attendees
- John Doe
- Jane Smith

## Action Items
- Review design mockups
- Update documentation
"""
    
    client.replace_document(target_doc.id, new_content)
    print(f"✅ Updated: {target_doc.title}")
```

### Document Content Format

Documents are stored as structured JSON. When you use `replace_document`, the content is converted to the appropriate format:

```python
# Plain text
client.replace_document(doc_id, "Simple text")

# Markdown-style formatting (as plain text)
client.replace_document(
    doc_id,
    """
# Header
## Subheader

- List item 1
- List item 2

**Bold** and *italic* text
"""
)

# Rich JSON format (with actual formatting)
json_content = [
    {
        "type": "heading",
        "attrs": {"level": 1},
        "content": [{"type": "text", "text": "Header"}]
    },
    {
        "type": "heading",
        "attrs": {"level": 2},
        "content": [{"type": "text", "text": "Subheader"}]
    },
    {
        "type": "bulletList",
        "content": [
            {
                "type": "listItem",
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "List item 1"}]
                }]
            },
            {
                "type": "listItem",
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "List item 2"}]
                }]
            }
        ]
    },
    {
        "type": "paragraph",
        "content": [
            {"type": "text", "marks": [{"type": "bold"}], "text": "Bold"},
            {"type": "text", "text": " and "},
            {"type": "text", "marks": [{"type": "italic"}], "text": "italic"},
            {"type": "text", "text": " text"}
        ]
    }
]

client.replace_json_document(doc_id, json_content)
```

## See Also

- [Tasks](./tasks) - Task operations and descriptions
- [Comments](./comments) - Add comments to tasks and documents
- [Projects](./projects) - Project management

