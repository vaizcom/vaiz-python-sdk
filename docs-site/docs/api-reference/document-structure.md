---
sidebar_position: 3
sidebar_label: Document Structure
title: Document Structure — JSON Format & Block Types | Vaiz Python SDK
description: Technical reference for the Vaiz document structure JSON format. Learn about blocks, marks, paragraphs, headings, lists, tables, and rich-text formatting.
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

### Task List Node (Checklist)

Interactive checklist with checkable items.

```json
{
  "type": "taskList",
  "attrs": {
    "uid": "uniqueId123"
  },
  "content": [
    {
      "type": "taskItem",
      "attrs": {
        "checked": true
      },
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Completed task"}]
        }
      ]
    },
    {
      "type": "taskItem",
      "attrs": {
        "checked": false
      },
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Todo task"}]
        }
      ]
    }
  ]
}
```

**Attributes:**
- `uid` - Unique identifier (optional, auto-generated)

**Features:**
- Interactive checkboxes
- Can be nested for multi-level checklists
- Supports checked/unchecked states
- Can contain paragraphs and nested task lists

### Task Item Node

Individual item in a task list (checklist).

```json
{
  "type": "taskItem",
  "attrs": {
    "checked": false
  },
  "content": [
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Task description"}]
    },
    {
      "type": "taskList",
      "content": [...]  // Nested checklist
    }
  ]
}
```

**Attributes:**
- `checked` - Whether the task is completed (required, boolean)

**Content:**
- Can contain paragraphs
- Can contain nested `taskList` nodes for sub-tasks
- Supports multi-level nesting

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

### Blockquote Node

Blockquote for quoted text or callouts.

```json
{
  "type": "blockquote",
  "content": [
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "This is a quote"}]
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

### Nested Lists

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

### Nested Checklists

Task lists support multi-level nesting:

```json
{
  "type": "taskList",
  "attrs": {"uid": "mainList"},
  "content": [
    {
      "type": "taskItem",
      "attrs": {"checked": false},
      "content": [
        {
          "type": "paragraph",
          "content": [{"type": "text", "text": "Main task"}]
        },
        {
          "type": "taskList",
          "attrs": {"uid": "nestedList"},
          "content": [
            {
              "type": "taskItem",
              "attrs": {"checked": true},
              "content": [
                {
                  "type": "paragraph",
                  "content": [{"type": "text", "text": "Subtask 1"}]
                }
              ]
            },
            {
              "type": "taskItem",
              "attrs": {"checked": false},
              "content": [
                {
                  "type": "paragraph",
                  "content": [{"type": "text", "text": "Subtask 2"}]
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

**Using helpers for nested checklists:**

```python
from vaiz import task_list, task_item, paragraph

content = [
    task_list(
        task_item(
            paragraph("Phase 1: Planning"),
            task_list(
                task_item("Define requirements", checked=True),
                task_item("Create wireframes", checked=True),
                task_item("Review with stakeholders", checked=False)
            ),
            checked=True
        ),
        task_item(
            paragraph("Phase 2: Development"),
            task_list(
                task_item("Setup project", checked=False),
                task_item("Implement features", checked=False)
            ),
            checked=False
        )
    )
]
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
from vaiz import heading, paragraph, text, bullet_list, task_list, task_item, blockquote, link_text, table, table_row, table_header

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
    heading(2, "Todo"),
    task_list(
        task_item("Review code", checked=True),
        task_item("Deploy to production", checked=False)
    ),
    blockquote(
        paragraph(
            text("Important: ", bold=True),
            "Always use type-safe helpers for better code quality."
        )
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

## Mention Blocks

Mention blocks create interactive references to users, documents, tasks, and milestones.

### Structure

```json
{
  "type": "custom-mention",
  "attrs": {
    "uid": "unique_id",
    "custom": 1,
    "inline": true,
    "data": {
      "item": {
        "id": "entity_id",
        "kind": "User"  // User | Document | Task | Milestone
      }
    }
  },
  "content": [
    {"type": "text", "text": " "}
  ]
}
```

### Using Helpers (Recommended)

```python
from vaiz import mention_user, mention_document, mention_task, mention_milestone

# Mention a user
mention_user("68fa7d4462f676bcd1c054b0")

# Mention a document
mention_document("68fa7d5762f676bcd1c055da")

# Mention a task
mention_task("68f2081feda35a3b34ac0318")

# Mention a milestone
mention_milestone("68fa739962f676bcd1beda2d")
```

### In Paragraphs

```python
from vaiz import paragraph, text, mention_user, mention_task

paragraph(
    text("Assigned to "),
    mention_user("member_id"),
    text(" - task "),
    mention_task("task_id")
)
```

### In Tables

```python
from vaiz import table, table_row, table_header, table_cell, paragraph
from vaiz import mention_user, mention_task

table(
    table_row(
        table_header("Assignee"),
        table_header("Task")
    ),
    table_row(
        table_cell(paragraph(mention_user("member_id"))),
        table_cell(paragraph(mention_task("task_id")))
    )
)
```

### Supported Mention Types

| Kind | Helper Function | Description |
|------|----------------|-------------|
| `User` | `mention_user(member_id)` | Mention a team member |
| `Document` | `mention_document(id)` | Reference a document |
| `Task` | `mention_task(id)` | Reference a task |
| `Milestone` | `mention_milestone(id)` | Reference a milestone |

### Getting Entity IDs

```python
# Get member ID
profile = client.get_profile()
member_id = profile.profile.member_id

# Or get from space members
members = client.get_space_members(space_id)
member_id = members.members[0].id

# Get document ID
from vaiz import GetDocumentsRequest, Kind
docs = client.get_documents(
    GetDocumentsRequest(kind=Kind.Space, kind_id=space_id)
)
doc_id = docs.payload.documents[0].id

# Get task ID
from vaiz import GetTasksRequest
tasks = client.get_tasks(GetTasksRequest())
task_id = tasks.payload.tasks[0].id

# Get milestone ID
milestones = client.get_milestones()
milestone_id = milestones.milestones[0].id
```

## Navigation Blocks

### TOC Block

Table of Contents block that automatically generates an interactive document outline.

**Structure:**
```json
{
  "type": "doc-siblings",
  "attrs": {
    "uid": "uniqueId123",
    "custom": 1,
    "contenteditable": "false"
  },
  "content": [
    {
      "type": "text",
      "text": "{\"type\":\"toc\"}"
    }
  ]
}
```

**Using Helper:**
```python
from vaiz import toc_block, heading, paragraph

content = [
    toc_block(),
    
    heading(1, "Introduction"),
    paragraph("Content here..."),
    
    heading(2, "Getting Started"),
    paragraph("More content...")
]

client.replace_json_document(document_id, content)
```

**Features:**
- Automatically indexes all headings (h1-h6)
- Creates clickable navigation links
- Shows hierarchical structure
- Updates automatically on changes

**Note:** Headings must have `uid` attribute for TOC navigation to work (automatically added by `heading()` helper).

---

### Anchors Block

Displays related documents and backlinks.

**Structure:**
```json
{
  "type": "doc-siblings",
  "attrs": {
    "uid": "uniqueId456",
    "custom": 1,
    "contenteditable": "false"
  },
  "content": [
    {
      "type": "text",
      "text": "{\"type\":\"anchors\"}"
    }
  ]
}
```

**Using Helper:**
```python
from vaiz import anchors_block, heading, paragraph

content = [
    anchors_block(),
    
    heading(1, "Documentation"),
    paragraph("Related documents shown above...")
]

client.replace_json_document(document_id, content)
```

**Shows:**
- Documents that this document links to
- Documents that link to this one (backlinks)
- Related documents from the space
- Knowledge graph connections

---

### Siblings Block

Previous/Next navigation between documents in a sequence.

**Structure:**
```json
{
  "type": "doc-siblings",
  "attrs": {
    "uid": "uniqueId789",
    "custom": 1,
    "contenteditable": "false"
  },
  "content": [
    {
      "type": "text",
      "text": "{\"type\":\"siblings\"}"
    }
  ]
}
```

**Using Helper:**
```python
from vaiz import siblings_block, heading, paragraph, horizontal_rule

content = [
    heading(1, "Tutorial Part 2: Advanced Features"),
    paragraph("Main content here..."),
    
    horizontal_rule(),
    
    # Navigation at the bottom
    siblings_block()  # Shows "← Part 1" and "Part 3 →"
]

client.replace_json_document(document_id, content)
```

**Features:**
- Shows Previous and Next documents in sequence
- Creates navigation buttons (Back/Forward)
- Typically placed at page bottom
- Maintains document order in branch

**Best for:**
- Tutorial series (Part 1 → Part 2 → Part 3)
- Multi-chapter guides  
- Sequential documentation
- Step-by-step workflows

---

### Code Block

Code block with syntax highlighting.

**Structure:**
```json
{
  "type": "codeBlock",
  "attrs": {
    "uid": "uniqueIdABC",
    "language": "python"
  },
  "content": [
    {
      "type": "text",
      "text": "def hello():\n    print(\"Hello, World!\")"
    }
  ]
}
```

**Using Helper:**
```python
from vaiz import code_block, heading, paragraph

python_code = '''def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)'''

content = [
    heading(1, "Code Example"),
    paragraph("Here's a Fibonacci function:"),
    
    code_block(
        code=python_code,
        language="python"
    )
]

client.replace_json_document(document_id, content)
```

**Supported Languages:**
- Python, JavaScript, TypeScript, Java, C++, Go, Rust
- SQL, JSON, YAML, XML, HTML, CSS, SCSS
- Bash, Shell, PowerShell
- Markdown, LaTeX
- And 50+ more languages

**Features:**
- Syntax highlighting based on language
- Multiline code support
- Optional language parameter
- Empty blocks supported

---

## Image Block

Embedded images in documents and task descriptions.

**Structure:**
```json
{
  "type": "image-block",
  "attrs": {
    "uid": "uniqueIdXYZ",
    "custom": 1,
    "contenteditable": "false",
    "widthPercent": 100
  },
  "content": [
    {
      "type": "text",
      "text": "{\"id\":\"img123\",\"src\":\"https://...\",\"fileName\":\"screenshot.png\",\"fileType\":\"image/png\",\"extension\":\"png\",\"title\":\"screenshot.png\",\"fileSize\":123456,\"fileId\":\"file_id\",\"dimensions\":[800,600],\"aspectRatio\":1.33,\"caption\":\"Screenshot\"}"
    }
  ]
}
```

**Image Data Fields:**
- `id` - Unique image ID (generated)
- `src` - Image URL (from upload_file)
- `fileName` - File name
- `fileType` - MIME type (e.g., "image/png", "image/jpeg")
- `extension` - File extension (e.g., "png", "jpg")
- `title` - Image title (usually same as fileName)
- `fileSize` - File size in bytes
- `fileId` - File ID from upload_file response
- `dimensions` - Optional [width, height] array
- `aspectRatio` - Optional aspect ratio (width/height)
- `caption` - Optional caption text
- `dominantColor` - Optional color object

**Attributes:**
- `uid` - Unique block identifier
- `custom` - Always 1 for custom blocks
- `contenteditable` - Should be "false"
- `widthPercent` - Display width percentage (1-100)

**Using Helper (Recommended):**
```python
from vaiz import image_block, heading, paragraph

# Upload image first
uploaded = client.upload_file("photo.jpg")

# Create image block
image = image_block(
    file_id=uploaded.file.id,
    src=uploaded.file.url,
    file_name="photo.jpg",
    file_size=uploaded.file.size,
    extension="jpg",
    file_type="image/jpeg",
    dimensions=[1920, 1080],
    caption="Product photo",
    width_percent=75
)

content = [
    heading(1, "Gallery"),
    paragraph("Check out our latest product:"),
    image
]

client.replace_json_document(document_id, content)
```

**Common Use Cases:**
- Screenshots in bug reports
- Product images in documentation
- Diagrams and flowcharts
- Photo galleries
- Visual examples in guides

---

## Files Block

File attachments (PDFs, documents, archives, etc.) in documents.

**Structure:**
```json
{
  "type": "files",
  "attrs": {
    "uid": "uniqueIdDEF",
    "custom": 1,
    "contenteditable": "false"
  },
  "content": [
    {
      "type": "text",
      "text": "{\"files\":[{\"id\":\"fileItem1\",\"fileId\":\"uploaded_file_id\",\"createAt\":1234567890000,\"url\":\"https://...\",\"extension\":\"pdf\",\"name\":\"Report.pdf\",\"size\":245678,\"type\":\"Pdf\"}]}"
    }
  ]
}
```

**Files Data Structure:**
- `files` - Array of file items

**File Item Fields:**
- `id` - Unique file item ID (generated)
- `fileId` - File ID from upload_file response
- `createAt` - Timestamp in milliseconds
- `url` - File download URL
- `extension` - File extension
- `name` - Display name
- `size` - File size in bytes
- `type` - File type category (see below)
- `dominantColor` - Optional color object

**File Type Categories:**
- `Pdf` - PDF documents
- `Image` - Images (prefer image_block instead)
- `Video` - Video files
- `Excel` - Spreadsheets (.xlsx, .xls, .csv)
- `PowerPoint` - Presentations (.pptx, .ppt)
- `Word` - Word documents (.docx, .doc)
- `Archive` - Compressed files (.zip, .rar, .tar.gz)
- `Text` - Text files (.txt, .md)
- `Code` - Source code files
- `Other` - Generic files

**Using Helper (Recommended):**
```python
from vaiz import files_block, heading, paragraph

# Upload files
pdf = client.upload_file("report.pdf")
excel = client.upload_file("data.xlsx")

# Create file items
files = [
    {
        "fileId": pdf.file.id,
        "url": pdf.file.url,
        "name": "Q4 Report.pdf",
        "size": pdf.file.size,
        "extension": "pdf",
        "type": "Pdf"
    },
    {
        "fileId": excel.file.id,
        "url": excel.file.url,
        "name": "Sales Data.xlsx",
        "size": excel.file.size,
        "extension": "xlsx",
        "type": "Excel"
    }
]

content = [
    heading(1, "Quarterly Report"),
    paragraph("Attached documents:"),
    files_block(*files)
]

client.replace_json_document(document_id, content)
```

**Common Use Cases:**
- Report attachments
- Source code archives
- Documentation PDFs
- Data exports (CSV, Excel)
- Log files
- Configuration files

**Combining Images and Files:**
```python
from vaiz import heading, paragraph, image_block, files_block, horizontal_rule

# Upload files
screenshot = client.upload_file("app.png")
manual = client.upload_file("manual.pdf")
source = client.upload_file("source.zip")

content = [
    heading(1, "Release v2.0"),
    
    # Image
    paragraph("New interface:"),
    image_block(
        file_id=screenshot.file.id,
        src=screenshot.file.url,
        file_name="app.png",
        file_size=screenshot.file.size,
        caption="Main screen"
    ),
    
    horizontal_rule(),
    
    # Files
    paragraph("Download resources:"),
    files_block(
        {
            "fileId": manual.file.id,
            "url": manual.file.url,
            "name": "User Manual.pdf",
            "size": manual.file.size,
            "extension": "pdf",
            "type": "Pdf"
        },
        {
            "fileId": source.file.id,
            "url": source.file.url,
            "name": "Source Code.zip",
            "size": source.file.size,
            "extension": "zip",
            "type": "Archive"
        }
    )
]

client.replace_json_document(document_id, content)
```

---

## Supported Elements

### Blocks

| Node Type | Description | Example |
|-----------|-------------|---------|
| `text` | Text content with optional marks | `{"type": "text", "text": "..."}` |
| `paragraph` | Paragraph block | `{"type": "paragraph", "content": [...]}` |
| `heading` | Heading (H1-H6) with UID | `{"type": "heading", "attrs": {"level": 1, "uid": "..."}}` |
| `bulletList` | Unordered list | `{"type": "bulletList", "content": [...]}` |
| `orderedList` | Numbered list | `{"type": "orderedList", "content": [...]}` |
| `listItem` | List item | `{"type": "listItem", "content": [...]}` |
| `taskList` | Checklist with checkable items | `{"type": "taskList", "attrs": {"uid": "..."}, "content": [...]}` |
| `taskItem` | Checklist item with checkbox | `{"type": "taskItem", "attrs": {"checked": false}, "content": [...]}` |
| `blockquote` | Blockquote for quotes/callouts | `{"type": "blockquote", "content": [...]}` |
| `details` | Collapsible section | `{"type": "details", "content": [...]}` |
| `extension-table` | Table with rows | `{"type": "extension-table", "attrs": {"uid": "..."}, "content": [...]}` |
| `tableRow` | Table row with cells/headers | `{"type": "tableRow", "attrs": {"showRowNumbers": false}, "content": [...]}` |
| `tableCell` | Table data cell | `{"type": "tableCell", "attrs": {"colspan": 1, "rowspan": 1}, "content": [...]}` |
| `tableHeader` | Table header cell (th) | `{"type": "tableHeader", "attrs": {"colspan": 1, "rowspan": 1}, "content": [...]}` |
| `horizontalRule` | Horizontal divider line | `{"type": "horizontalRule"}` |
| `custom-mention` | Mention user/doc/task/milestone | `{"type": "custom-mention", "attrs": {"uid": "...", "custom": 1, "inline": true, "data": {"item": {"id": "...", "kind": "User"}}}}` |
| `image-block` | Embedded image | `{"type": "image-block", "attrs": {"uid": "...", "custom": 1}, "content": [...]}` |
| `files` | File attachments | `{"type": "files", "attrs": {"uid": "...", "custom": 1}, "content": [...]}` |
| `doc-siblings` | Navigation blocks (TOC/Anchors/Siblings) | `{"type": "doc-siblings", "attrs": {"uid": "...", "custom": 1}, "content": [...]}` |
| `codeBlock` | Code with syntax highlighting | `{"type": "codeBlock", "attrs": {"uid": "...", "language": "python"}, "content": [...]}` |

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

