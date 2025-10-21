---
sidebar_position: 9
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

See [API Reference](./methods#document-models) for complete Document model definition.

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

## Working with Document Content

In addition to listing and creating documents, you can work with their content using document API methods.

### Get Document Content

Retrieve the JSON content of any document:

```python
# Get document content by ID
content = client.get_document_body("document_id")
print(content)  # Returns parsed JSON structure
```

This method is universal and works for:
- Task descriptions
- Standalone documents
- Any document by its ID

### Replace Document Content

Replace the entire content of a document:

```python
# Replace document content
client.replace_document(
    document_id="document_id",
    description="New content here"
)
```

**Use cases:**
- Updating task descriptions programmatically
- Bulk content updates
- Template-based content generation

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
    current_content = client.get_document_body(target_doc.id)
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

# Markdown-style formatting
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
```

## See Also

- [Tasks](./tasks) - Task operations and descriptions
- [Comments](./comments) - Add comments to tasks and documents
- [Projects](./projects) - Project management

