---
sidebar_position: 3
---

# Document Structure

Technical reference for the document structure JSON format.

## Content Methods

These methods work with document content for both task descriptions and standalone documents.

### `get_json_document`

```python
get_json_document(document_id: str) -> Dict[str, Any]
```

Get the JSON content of a specific document or task description.

**Parameters:**
- `document_id` - Document ID (from task or standalone document)

**Returns:** `Dict[str, Any]` - Parsed JSON structure

**Example:**
```python
# Get standalone document content
content = client.get_json_document("document_id")
print(content)

# Get task description
task_response = client.get_task("PRJ-123")
description = client.get_json_document(task_response.task.document)
```

---

### `replace_document`

```python
replace_document(
    document_id: str,
    description: str
) -> ReplaceDocumentResponse
```

Replace document content with plain text.

**Parameters:**
- `document_id` - Document ID
- `description` - New content (plain text or markdown-style)

**Returns:** `ReplaceDocumentResponse`

**Example:**
```python
# Replace with plain text
client.replace_document(
    document_id="doc_id",
    description="""
# Updated Content

New document content here.
"""
)
```

---

### `replace_json_document`

```python
replace_json_document(
    document_id: str,
    content: List[Dict[str, Any]]
) -> ReplaceJSONDocumentResponse
```

Replace document content with structured JSON content.

**Works for:**
- Task descriptions
- Standalone documents (Project, Space, Member)
- Any document type

**Parameters:**
- `document_id` - Document ID
- `content` - JSONContent array (see format below)

**Returns:** `ReplaceJSONDocumentResponse`

**Example with raw JSON:**
```python
json_content = [
    {
        "type": "heading",
        "attrs": {"level": 1},
        "content": [{"type": "text", "text": "Title"}]
    },
    {
        "type": "paragraph",
        "content": [
            {"type": "text", "text": "This is "},
            {"type": "text", "marks": [{"type": "bold"}], "text": "bold"}
        ]
    }
]

client.replace_json_document("doc_id", json_content)
```

**Example with helpers (recommended):**
```python
from vaiz import heading, paragraph, text

content = [
    heading(1, "Title"),
    paragraph("This is ", text("bold", bold=True))
]

client.replace_json_document("doc_id", content)
```

See [Document Structure Helpers Guide](../guides/document-structure-helpers) for all helper functions.

---

### `append_document`

```python
append_document(
    document_id: str,
    description: str = None,
    files: List[Any] = None
) -> AppendDocumentResponse
```

Append plain text content to an existing document without removing existing content.

**Parameters:**
- `document_id` - Document ID
- `description` - Plain text to append (optional)
- `files` - Files to attach (optional)

**Returns:** `AppendDocumentResponse`

**Example:**
```python
# Append text to existing document
client.append_document(
    document_id="doc_id",
    description="\n\nUpdate: Task completed successfully"
)
```

---

### `append_json_document`

```python
append_json_document(
    document_id: str,
    content: List[Dict[str, Any]]
) -> AppendJSONDocumentResponse
```

Append structured JSON content to an existing document without removing existing content.

**Parameters:**
- `document_id` - Document ID
- `content` - JSONContent array (see format below)

**Returns:** `AppendJSONDocumentResponse`

**Example with raw JSON:**
```python
new_section = [
    {
        "type": "heading",
        "attrs": {"level": 2},
        "content": [{"type": "text", "text": "Update"}]
    },
    {
        "type": "paragraph",
        "content": [{"type": "text", "text": "Additional notes"}]
    }
]

client.append_json_document("doc_id", new_section)
```

**Example with helpers:**
```python
from vaiz import heading, paragraph, text

updates = [
    heading(2, "Update"),
    paragraph("Additional ", text("notes", bold=True))
]

client.append_json_document("doc_id", updates)
```

---

## Method Comparison

| Method | Clears Existing? | Format | Use Case |
|--------|------------------|--------|----------|
| `replace_document` | ✅ Yes | Plain text | Complete replacement with plain text |
| `replace_json_document` | ✅ Yes | JSON structure | Complete replacement with rich content |
| `append_document` | ❌ No | Plain text | Add to existing plain text |
| `append_json_document` | ❌ No | JSON structure | Add to existing rich content |

---

## Format Overview

Documents consist of an array of **nodes**. Each node has a `type` and optional `content` or `attrs`:

```json
[
  {
    "type": "heading",
    "attrs": {"level": 1},
    "content": [...]
  },
  {
    "type": "paragraph",
    "content": [...]
  }
]
```

## Node Types

### Text Node

The most basic node type containing text content.

```json
{
  "type": "text",
  "text": "Hello World"
}
```

**With formatting marks:**

```json
{
  "type": "text",
  "text": "Bold text",
  "marks": [{"type": "bold"}]
}
```

### Paragraph Node

Block-level node for paragraphs.

```json
{
  "type": "paragraph",
  "content": [
    {"type": "text", "text": "Regular text and "},
    {"type": "text", "text": "bold text", "marks": [{"type": "bold"}]}
  ]
}
```

### Heading Node

Heading with level 1-6.

```json
{
  "type": "heading",
  "attrs": {"level": 1},
  "content": [
    {"type": "text", "text": "Main Title"}
  ]
}
```

**Levels:**
- `level: 1` - H1 (largest)
- `level: 2` - H2
- `level: 3` - H3
- `level: 4` - H4
- `level: 5` - H5
- `level: 6` - H6 (smallest)

### Bullet List Node

Unordered list with bullet points.

```json
{
  "type": "bulletList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "First item"}]
        }
      ]
    },
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Second item"}]
        }
      ]
    }
  ]
}
```

### Ordered List Node

Numbered list.

```json
{
  "type": "orderedList",
  "attrs": {"start": 1},
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "First step"}]
        }
      ]
    }
  ]
}
```

**Attributes:**
- `start` - Starting number (optional, default: 1)

### List Item Node

Individual item in a list. Can contain paragraphs and nested lists.

```json
{
  "type": "listItem",
  "content": [
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Item content"}]
    },
    {
      "type": "bulletList",
      "content": [...]  // Nested list
    }
  ]
}
```

## Text Formatting Marks

Marks are applied to text nodes to add formatting:

### Bold

```json
{
  "type": "text",
  "text": "Bold text",
  "marks": [{"type": "bold"}]
}
```

### Italic

```json
{
  "type": "text",
  "text": "Italic text",
  "marks": [{"type": "italic"}]
}
```

### Code

Inline code formatting.

```json
{
  "type": "text",
  "text": "client.get_task()",
  "marks": [{"type": "code"}]
}
```

### Link

Hyperlink with URL.

```json
{
  "type": "text",
  "text": "Click here",
  "marks": [
    {
      "type": "link",
      "attrs": {
        "href": "https://vaiz.app",
        "target": "_blank"
      }
    }
  ]
}
```

**Attributes:**
- `href` - URL (required)
- `target` - Link target (optional, e.g., `"_blank"`)

### Combined Marks

Multiple marks can be combined:

```json
{
  "type": "text",
  "text": "Bold italic link",
  "marks": [
    {"type": "bold"},
    {"type": "italic"},
    {
      "type": "link",
      "attrs": {"href": "https://example.com"}
    }
  ]
}
```

## Tables

Tables use the `extension-table` type and consist of rows and cells.

### Extension Table

Table with rows and cells.

```json
{
  "type": "extension-table",
  "attrs": {
    "uid": "uniqueId123",
    "showRowNumbers": false
  },
  "content": [
    {
      "type": "tableRow",
      "attrs": {"showRowNumbers": false},
      "content": [
        {
          "type": "tableCell",
          "attrs": {"colspan": 1, "rowspan": 1},
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Name"}]
            }
          ]
        },
        {
          "type": "tableCell",
          "attrs": {"colspan": 1, "rowspan": 1},
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Status"}]
            }
          ]
        }
      ]
    },
    {
      "type": "tableRow",
      "attrs": {"showRowNumbers": false},
      "content": [
        {
          "type": "tableCell",
          "attrs": {"colspan": 1, "rowspan": 1},
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Task 1"}]
            }
          ]
        },
        {
          "type": "tableCell",
          "attrs": {"colspan": 1, "rowspan": 1},
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Done"}]
            }
          ]
        }
      ]
    }
  ]
}
```

### Table Row

Row in a table containing cells.

```json
{
  "type": "tableRow",
  "attrs": {"showRowNumbers": false},
  "content": [
    {"type": "tableCell", "attrs": {"colspan": 1, "rowspan": 1}, "content": [...]},
    {"type": "tableCell", "attrs": {"colspan": 1, "rowspan": 1}, "content": [...]}
  ]
}
```

**Attributes:**
- `showRowNumbers` - Display row numbers (optional, default: false)

### Table Cell

Table cell containing content (data cell).

```json
{
  "type": "tableCell",
  "attrs": {
    "colspan": 1,
    "rowspan": 1
  },
  "content": [
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Cell content"}]
    }
  ]
}
```

**Attributes:**
- `colspan` - Number of columns to span (default: 1)
- `rowspan` - Number of rows to span (default: 1)

### Table Header

Table header cell (`<th>` in HTML). Use for semantic table headers.

```json
{
  "type": "tableHeader",
  "attrs": {
    "colspan": 1,
    "rowspan": 1
  },
  "content": [
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Header Name"}]
    }
  ]
}
```

**Attributes:**
- `colspan` - Number of columns to span (default: 1)
- `rowspan` - Number of rows to span (default: 1)

**Benefits:**
- Semantic HTML structure
- Better accessibility for screen readers
- Consistent styling
- Supports colspan/rowspan like table cells

## Nested Structures

Lists can be nested within list items:

```json
{
  "type": "bulletList",
  "content": [
    {
      "type": "listItem",
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Parent item"}]
        },
        {
          "type": "bulletList",
          "content": [
            {
              "type": "listItem",
              "content": [
                {
                  "type": "paragraph",
                  "content": [{"type": "text", "text": "Nested item"}]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## Complete Example

```json
[
  {
    "type": "heading",
    "attrs": {"level": 1},
    "content": [
      {"type": "text", "text": "Project Documentation"}
    ]
  },
  {
    "type": "paragraph",
    "content": [
      {"type": "text", "text": "This is "},
      {"type": "text", "text": "bold", "marks": [{"type": "bold"}]},
      {"type": "text", "text": " and "},
      {"type": "text", "text": "italic", "marks": [{"type": "italic"}]},
      {"type": "text", "text": " text."}
    ]
  },
  {
    "type": "heading",
    "attrs": {"level": 2},
    "content": [
      {"type": "text", "text": "Features"}
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
            "content": [{"type": "text", "text": "Easy to use"}]
          }
        ]
      },
      {
        "type": "listItem",
        "content": [
          {
            "type": "paragraph",
            "content": [{"type": "text", "text": "Type-safe"}]
          }
        ]
      }
    ]
  },
  {
    "type": "paragraph",
    "content": [
      {"type": "text", "text": "Learn more at "},
      {
        "type": "text",
        "text": "docs.vaiz.app",
        "marks": [
          {
            "type": "link",
            "attrs": {
              "href": "https://docs.vaiz.app",
              "target": "_blank"
            }
          }
        ]
      }
    ]
  }
]
```

## Helper Functions (Recommended)

Instead of manually constructing JSON, use the built-in helper functions:

```python
from vaiz import heading, paragraph, text, bullet_list, link_text, table, table_row, table_header

content = [
    heading(1, "Project Documentation"),
    paragraph(
        "This is ",
        text("bold", bold=True),
        " and ",
        text("italic", italic=True),
        " text."
    ),
    heading(2, "Features"),
    bullet_list(
        "Easy to use",
        "Type-safe"
    ),
    table(
        table_row(
            table_header("Feature"),
            table_header("Status")
        ),
        table_row("Document helpers", "✅"),
        table_row("Table headers", "✅")
    ),
    paragraph(
        "Learn more at ",
        link_text("docs.vaiz.app", "https://docs.vaiz.app")
    )
]
```

See [Document Structure Helpers Guide](../guides/document-structure-helpers) for complete documentation.

## Supported Elements

### Blocks

| Node Type | Description | Example |
|-----------|-------------|---------|
| `text` | Text content with optional marks | `{"type": "text", "text": "..."}` |
| `paragraph` | Paragraph block | `{"type": "paragraph", "content": [...]}` |
| `heading` | Heading (H1-H6) | `{"type": "heading", "attrs": {"level": 1}}` |
| `bulletList` | Unordered list | `{"type": "bulletList", "content": [...]}` |
| `orderedList` | Numbered list | `{"type": "orderedList", "content": [...]}` |
| `listItem` | List item | `{"type": "listItem", "content": [...]}` |
| `extension-table` | Table with rows | `{"type": "extension-table", "attrs": {"uid": "..."}, "content": [...]}` |
| `tableRow` | Table row with cells/headers | `{"type": "tableRow", "attrs": {"showRowNumbers": false}, "content": [...]}` |
| `tableCell` | Table data cell | `{"type": "tableCell", "attrs": {"colspan": 1, "rowspan": 1}, "content": [...]}` |
| `tableHeader` | Table header cell (th) | `{"type": "tableHeader", "attrs": {"colspan": 1, "rowspan": 1}, "content": [...]}` |
| `horizontalRule` | Horizontal divider line | `{"type": "horizontalRule"}` |

### Marks

| Mark Type | Description |
|-----------|-------------|
| `bold` | Bold text |
| `italic` | Italic text |
| `code` | Inline code |
| `link` | Hyperlink with href |

## See Also

- [Documents Guide](../guides/documents) - Document management
- [Document Structure Helpers](../guides/document-structure-helpers) - Helper functions
- [Tasks API](./tasks) - Task descriptions use the same format

