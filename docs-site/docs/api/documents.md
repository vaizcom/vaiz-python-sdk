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

### Document Model

Each document in the list contains:

```python
class Document:
    id: str                      # Unique document ID
    title: str                   # Document title
    size: int                    # Document size in bytes
    contributor_ids: List[str]   # List of contributor IDs
    archiver: Optional[str]      # User who archived (if archived)
    followers: Dict[str, str]    # Document followers
    archived_at: Optional[datetime]  # Archive timestamp
    kind_id: str                 # ID of parent (space/member/project)
    kind: Kind                   # Document scope (Space/Member/Project)
    creator: str                 # Creator user ID
    map: List[Any]               # Document structure map
    created_at: datetime         # Creation timestamp
    updated_at: datetime         # Last update timestamp
    bucket: str                  # Storage bucket ID
```

### Filtering Documents

```python
# Get all project documents
all_docs = client.get_documents(
    GetDocumentsRequest(
        kind=Kind.Project,
        kind_id=project_id
    )
)

# Filter by criteria
active_docs = [
    doc for doc in all_docs.payload.documents
    if doc.archived_at is None
]

recent_docs = sorted(
    all_docs.payload.documents,
    key=lambda d: d.created_at,
    reverse=True
)[:10]

print(f"Total: {len(all_docs.payload.documents)}")
print(f"Active: {len(active_docs)}")
print(f"Recent 10: {len(recent_docs)}")
```

## Working with Document Content

In addition to listing documents, you can work with their content using document API methods.

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

### Example: Update Project Document

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

