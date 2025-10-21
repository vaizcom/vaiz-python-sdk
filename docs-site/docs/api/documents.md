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

## See Also

- [Tasks](./tasks) - Task operations and descriptions
- [Comments](./comments) - Add comments to tasks and documents
- [Projects](./projects) - Project management

