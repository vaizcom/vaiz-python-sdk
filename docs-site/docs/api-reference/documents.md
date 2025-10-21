---
sidebar_position: 9
---

# Documents

Complete reference for document-related methods and models.

## Methods

### `create_document`

```python
create_document(request: CreateDocumentRequest) -> CreateDocumentResponse
```

Create a new document in specified scope (Space/Member/Project).

**Parameters:**
- `request` - CreateDocumentRequest with kind, kind_id, title, index, and optional parent_document_id

**Returns:** `CreateDocumentResponse` with created document

**Example:**
```python
from vaiz.models import CreateDocumentRequest, Kind

response = client.create_document(
    CreateDocumentRequest(
        kind=Kind.Project,
        kind_id="project_id",
        title="Project Plan",
        index=0
    )
)

document = response.payload.document
print(f"Created: {document.id}")
```

---

### `get_documents`

```python
get_documents(request: GetDocumentsRequest) -> GetDocumentsResponse
```

Get list of documents filtered by scope (Space/Member/Project) and scope ID.

**Parameters:**
- `request` - GetDocumentsRequest with kind and kind_id

**Returns:** `GetDocumentsResponse` with list of documents

**Example:**
```python
from vaiz.models import GetDocumentsRequest, Kind

docs = client.get_documents(
    GetDocumentsRequest(
        kind=Kind.Project,
        kind_id="project_id"
    )
)
```

---

### `get_document_body`

```python
get_document_body(document_id: str) -> Dict[str, Any]
```

Get the JSON content of a specific document.

**Parameters:**
- `document_id` - Document ID

**Returns:** `Dict[str, Any]` - Parsed JSON structure

**Example:**
```python
# Get document content
content = client.get_document_body("document_id")
print(content)

# Get task description
task = client.get_task("PRJ-123")
description = client.get_document_body(task.payload["task"]["document"])
```

---

### `replace_document`

```python
replace_document(
    document_id: str,
    description: str
) -> ReplaceDocumentResponse
```

Replace the entire content of a document.

**Parameters:**
- `document_id` - Document ID
- `description` - New content (plain text or markdown-style)

**Returns:** `ReplaceDocumentResponse`

**Example:**
```python
# Replace document content
client.replace_document(
    document_id="doc_id",
    description="""
# Updated Content

New document content here.
"""
)
```

---

## Models

### Document

```python
class Document:
    id: str                             # Document ID
    title: str                          # Document title
    size: int                           # Document size in bytes
    contributor_ids: List[str]          # List of contributor IDs
    archiver: Optional[str]             # User who archived (if archived)
    followers: Dict[str, str]           # Document followers
    archived_at: Optional[datetime]     # Archive timestamp
    kind_id: str                        # ID of document
    kind: Kind                          # Document scope (Space/Member/Project)
    creator: str                        # Creator user ID
    map: List[Any]                      # Document structure map
    created_at: datetime                # Creation timestamp
    updated_at: datetime                # Last update timestamp
    bucket: str                         # Storage bucket ID
```

---

### CreateDocumentRequest

```python
class CreateDocumentRequest:
    kind: Kind                          # Required - Document scope (Space/Member/Project)
    kind_id: str                        # Required - ID of space/member/project
    title: str                          # Required - Document title
    index: int                          # Required - Position in document list
    parent_document_id: Optional[str]   # Optional - Parent document ID for nesting
```

---

### CreateDocumentResponse

```python
class CreateDocumentResponse:
    payload: CreateDocumentPayload      # Response payload
    type: str                           # Response type ("CreateDocument")
```

---

### CreateDocumentPayload

```python
class CreateDocumentPayload:
    document: Document                  # Created document
```

---

### GetDocumentsRequest

```python
class GetDocumentsRequest:
    kind: Kind                          # Required - Document scope (Space/Member/Project)
    kind_id: str                        # Required - ID of space/member/project
```

---

### GetDocumentsResponse

```python
class GetDocumentsResponse:
    payload: GetDocumentsPayload        # Response payload
    type: str                           # Response type ("GetDocuments")
```

---

### GetDocumentsPayload

```python
class GetDocumentsPayload:
    documents: List[Document]           # List of documents
```

---

### GetDocumentRequest

```python
class GetDocumentRequest:
    document_id: str                    # Required - Document ID
```

---

### ReplaceDocumentRequest

```python
class ReplaceDocumentRequest:
    document_id: str                    # Required - Document ID
    description: str                    # Required - New document content
```

---

### ReplaceDocumentResponse

```python
class ReplaceDocumentResponse:
    # Empty response on success
    pass
```

---

## See Also

- [Documents Guide](../guides/documents) - Usage examples and patterns
- [Enums](./enums) - Kind enum for document scopes

