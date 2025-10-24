---
sidebar_position: 16
sidebar_label: Document Structure Helpers
title: Document Structure Helpers — Type-Safe Content Building | Vaiz Python SDK
description: Learn how to use type-safe helper functions to build valid document content with the Vaiz Python SDK. Includes paragraphs, headings, lists, tables, and more.
---

# Document Structure Helpers

Type-safe helper functions for building valid document content.

## Overview

The document structure format is used for creating and editing rich content in Vaiz. This includes:

- **Task descriptions** - Add rich formatted content to task descriptions
- **Standalone documents** - Project, Space, and Member documents
- **Any document content** - Universal format for all document types

When working with `replace_json_document`, you can use document structure helper functions to build content in a type-safe, readable way instead of manually constructing JSON structures.

### Why Use Helpers?

Instead of manually writing JSON structures, helpers provide:
- **Type safety** - Correct structure guaranteed
- **Readability** - Clean, Pythonic syntax
- **Validation** - Only allows supported elements
- **Productivity** - Write less, accomplish more

## Basic Helpers

### Text

Create text nodes with optional formatting:

```python
from vaiz import text

# Plain text
text("Hello World")

# Bold text
text("Important", bold=True)

# Italic text
text("Emphasis", italic=True)

# Inline code
text("client.get_task()", code=True)

# Combined formatting
text("Bold and Italic", bold=True, italic=True)

# Link
text("Click here", link="https://vaiz.app")
```

### Paragraph

Create paragraph nodes:

```python
from vaiz import paragraph, text

# Simple paragraph
paragraph("Hello World")

# Paragraph with mixed formatting
paragraph(
    "This is ",
    text("bold text", bold=True),
    " and this is ",
    text("italic", italic=True),
    "."
)
```

### Heading

Create heading nodes (levels 1-6):

```python
from vaiz import heading, text

# H1
heading(1, "Main Title")

# H2
heading(2, "Section Title")

# With formatting
heading(1, text("Important Title", bold=True))
```

### Links

Create hyperlink text:

```python
from vaiz import link_text, paragraph

# Basic link
link_text("Visit Vaiz", "https://vaiz.app")

# Bold link
link_text("Documentation", "https://docs.vaiz.app", bold=True)

# In a paragraph
paragraph(
    "Check out our ",
    link_text("documentation", "https://docs.vaiz.app"),
    " for more info."
)
```

## Lists

### Bullet Lists

Create unordered lists:

```python
from vaiz import bullet_list, list_item, paragraph, text

# Simple list from strings
bullet_list(
    "First item",
    "Second item",
    "Third item"
)

# Complex list items
bullet_list(
    list_item(paragraph(text("Bold item", bold=True))),
    list_item(paragraph("Regular item")),
    "Simple string item"
)
```

### Ordered Lists

Create numbered lists:

```python
from vaiz import ordered_list, list_item, paragraph

# Simple numbered list
ordered_list(
    "First step",
    "Second step",
    "Third step"
)

# Start from specific number
ordered_list(
    "Item 5",
    "Item 6",
    "Item 7",
    start=5
)

# Complex items
ordered_list(
    list_item(paragraph("Step 1: ", text("Install SDK", bold=True))),
    list_item(paragraph("Step 2: ", text("Configure", bold=True)))
)
```

### Nested Lists

Create multi-level list structures:

```python
from vaiz import bullet_list, list_item, paragraph

bullet_list(
    "Top level item",
    list_item(
        paragraph("Parent item"),
        bullet_list(
            "Nested item 1",
            "Nested item 2",
            list_item(
                paragraph("Sub-nested item"),
                bullet_list("Level 3 item")
            )
        )
    ),
    "Another top item"
)
```

## Tables

### Simple Table

Create tables with headers and data rows:

```python
from vaiz import table, table_row

# Simple status table
# Note: First row is typically displayed as headers in UI
status_table = table(
    table_row("Task", "Status", "Priority"),  # Header row
    table_row("Design mockups", "Done", "High"),
    table_row("API development", "In Progress", "High"),
    table_row("Documentation", "Todo", "Medium")
)
```

### Table with Header Cells

Use `table_header()` to create proper header cells (`<th>` in HTML):

```python
from vaiz import table, table_row, table_header

# Table with semantic header cells
status_table = table(
    table_row(
        table_header("Task"),
        table_header("Status"),
        table_header("Priority")
    ),
    table_row("Design mockups", "Done", "High"),
    table_row("API development", "In Progress", "High"),
    table_row("Documentation", "Todo", "Medium")
)
```

**Benefits of `table_header()`:**
- Semantic HTML structure (`<th>` vs `<td>`)
- Better accessibility for screen readers
- Consistent header styling
- Support for colspan/rowspan on headers

### Table with Formatting

Add formatting to table content:

```python
from vaiz import table, table_row, table_cell, table_header, text, paragraph

formatted_table = table(
    table_row(
        table_header(paragraph(text("Name", bold=True))),
        table_header(paragraph(text("Status", bold=True)))
    ),
    table_row(
        table_cell(paragraph(text("Task 1", bold=True))),
        table_cell("✅ Done")
    ),
    table_row(
        "Task 2",
        table_cell(paragraph(text("In Progress", italic=True)))
    )
)
```

### Complex Table Example

```python
from vaiz import heading, paragraph, table, table_row, table_header, text

content = [
    heading(1, "📊 Project Metrics"),
    
    paragraph("Current sprint status:"),
    
    table(
        table_row(
            table_header("Metric"),
            table_header("Count"),
            table_header("Percentage")
        ),
        table_row("Completed", "28", "60%"),
        table_row("In Progress", "12", "26%"),
        table_row("Todo", "7", "14%")
    ),
    
    paragraph(text("Total: 47 tasks", bold=True))
]
```

### Table with Merged Headers (colspan/rowspan)

```python
from vaiz import table, table_row, table_header, table_cell, text, paragraph

# Quarterly report table with merged header
quarterly_table = table(
    # Main header spanning all columns
    table_row(
        table_header(paragraph(text("Q1-Q4 Performance", bold=True)), colspan=5)
    ),
    # Subheaders
    table_row(
        table_header("Metric"),
        table_header("Q1"),
        table_header("Q2"),
        table_header("Q3"),
        table_header("Q4")
    ),
    # Data rows
    table_row("Revenue", "$100K", "$120K", "$150K", "$180K"),
    table_row("Users", "1,000", "1,500", "2,200", "3,000")
)
```

## Visual Elements

### Horizontal Rule

Create a horizontal divider line:

```python
from vaiz import horizontal_rule

# Horizontal rule (native HTML <hr> style)
horizontal_rule()
```

### Blockquote

Create blockquotes for quoted text or callouts:

```python
from vaiz import blockquote, paragraph, text

# Blockquote with formatting
blockquote(
    paragraph(
        text("Important: ", bold=True),
        "This is a critical note that stands out."
    )
)
```

**Use cases for blockquotes:**
- Quotations from external sources
- Important callouts or warnings
- Key insights or takeaways
- API documentation notes
- User testimonials or feedback

## Mention Blocks

Create interactive mentions to reference users, documents, tasks, and milestones.

### Overview

Mention blocks create clickable references to entities in your workspace. When mentioned, users receive notifications and can click to navigate to the referenced item.

### User Mentions

Reference team members:

```python
from vaiz import mention_user, paragraph, text

# Get member ID from profile
profile = client.get_profile()
member_id = profile.profile.member_id

# Mention a user
paragraph(
    text("Assigned to "),
    mention_user(member_id)
)
```

### Document Mentions

Link to other documents:

```python
from vaiz import mention_document, paragraph, text

# Get document ID
from vaiz import GetDocumentsRequest, Kind

docs = client.get_documents(
    GetDocumentsRequest(kind=Kind.Space, kind_id=space_id)
)
doc_id = docs.payload.documents[0].id

# Mention a document
paragraph(
    text("See "),
    mention_document(doc_id),
    text(" for details")
)
```

### Task Mentions

Reference tasks:

```python
from vaiz import mention_task, paragraph, text, GetTasksRequest

# Get task ID
tasks = client.get_tasks(GetTasksRequest())
task_id = tasks.payload.tasks[0].id

# Mention a task
paragraph(
    text("Related to "),
    mention_task(task_id)
)
```

### Milestone Mentions

Link to milestones:

```python
from vaiz import mention_milestone, paragraph, text

# Get milestone ID
milestones = client.get_milestones()
milestone_id = milestones.milestones[0].id

# Mention a milestone
paragraph(
    text("Part of "),
    mention_milestone(milestone_id)
)
```

### Multiple Mentions

Combine multiple mentions in one paragraph:

```python
from vaiz import paragraph, text, mention_user, mention_task, mention_milestone

paragraph(
    text("User "),
    mention_user(member_id),
    text(" is assigned to "),
    mention_task(task_id),
    text(" in milestone "),
    mention_milestone(milestone_id)
)
```

### Mentions in Lists

Use mentions in bullet or ordered lists:

```python
from vaiz import bullet_list, list_item, paragraph, text, mention_user, mention_task

bullet_list(
    list_item(paragraph(
        text("Assignee: "),
        mention_user(member_id)
    )),
    list_item(paragraph(
        text("Related task: "),
        mention_task(task_id)
    ))
)
```

### Mentions in Tables

Create tables with mention references:

```python
from vaiz import table, table_row, table_header, table_cell, paragraph
from vaiz import mention_user, mention_task

table(
    table_row(
        table_header("Assignee"),
        table_header("Task"),
        table_header("Status")
    ),
    table_row(
        table_cell(paragraph(mention_user(member_id))),
        table_cell(paragraph(mention_task(task_id))),
        table_cell("In Progress")
    )
)
```

### Generic Mention Function

Use the generic `mention()` function for any entity type:

```python
from vaiz import mention

# Explicitly specify the kind
user_mention = mention(member_id, "User")
doc_mention = mention(doc_id, "Document")
task_mention = mention(task_id, "Task")
milestone_mention = mention(milestone_id, "Milestone")
```

### Supported Mention Types

| Function | Entity Type | Description |
|----------|-------------|-------------|
| `mention_user(member_id)` | User | Mention a team member |
| `mention_document(id)` | Document | Reference a document |
| `mention_task(id)` | Task | Reference a task |
| `mention_milestone(id)` | Milestone | Reference a milestone |
| `mention(id, kind)` | Any | Generic mention with explicit kind |

### Complete Example with Mentions

```python
from vaiz import VaizClient, GetDocumentsRequest, GetTasksRequest, Kind
from vaiz import (
    heading, paragraph, text, bullet_list, list_item,
    table, table_row, table_header, table_cell,
    mention_user, mention_task, mention_document
)

client = VaizClient(api_key="...", space_id="...")

# Get entity IDs
profile = client.get_profile()
member_id = profile.profile.member_id

tasks = client.get_tasks(GetTasksRequest())
task_id = tasks.payload.tasks[0].id

docs = client.get_documents(
    GetDocumentsRequest(kind=Kind.Space, kind_id=client.space_id)
)
doc_id = docs.payload.documents[0].id

# Create document with mentions
content = [
    heading(1, "Meeting Notes"),
    
    paragraph(
        text("Attendees: "),
        mention_user(member_id)
    ),
    
    heading(2, "Action Items"),
    
    bullet_list(
        list_item(paragraph(
            mention_user(member_id),
            text(" will complete "),
            mention_task(task_id)
        )),
        list_item(paragraph(
            text("Update "),
            mention_document(doc_id)
        ))
    ),
    
    heading(2, "Task Assignments"),
    
    table(
        table_row(
            table_header("Assignee"),
            table_header("Task")
        ),
        table_row(
            table_cell(paragraph(mention_user(member_id))),
            table_cell(paragraph(mention_task(task_id)))
        )
    )
]

# Update document
client.replace_json_document(document_id, content)
```

## Complete Example

Build a full document with helpers:

```python
from vaiz import (
    VaizClient, text, paragraph, heading, 
    bullet_list, ordered_list, list_item, 
    link_text, horizontal_rule, blockquote
)

client = VaizClient(token="your_token")

# Build content using helpers
content = [
    # Title
    heading(1, "📚 Project Documentation"),
    
    # Subtitle
    paragraph(
        text("Status: ", italic=True),
        text("Active", bold=True)
    ),
    
    horizontal_rule(),
    
    # Overview
    heading(2, "Overview"),
    paragraph(
        "This project uses ",
        text("Vaiz SDK", bold=True),
        " for task management. Visit ",
        link_text("docs", "https://docs.vaiz.app"),
        " to learn more."
    ),
    
    # Important note
    blockquote(
        paragraph(
            text("Note: ", bold=True),
            "This SDK provides type-safe helpers for building document content."
        )
    ),
    
    # Features
    heading(2, "✨ Features"),
    bullet_list(
        "Real-time collaboration",
        "Rich text editing",
        list_item(
            paragraph(text("API Integration", bold=True)),
            bullet_list(
                "Python SDK",
                "REST API",
                "WebSocket support"
            )
        )
    ),
    
    # Quick Start
    heading(2, "Quick Start"),
    ordered_list(
        list_item(paragraph("Install: ", text("pip install vaiz-sdk", code=True))),
        list_item(paragraph("Import: ", text("from vaiz import VaizClient", code=True))),
        list_item(paragraph("Use: ", text("client = VaizClient(token='...')", code=True)))
    ),
    
    # Footer
    horizontal_rule(),
    paragraph(
        text("Built with ", italic=True),
        text("document structure helpers", code=True)
    )
]

# Replace document
client.replace_json_document("document_id", content)
```

## Navigation Blocks

### TOC Block - Table of Contents

Automatically generate a table of contents from all headings in the document:

```python
from vaiz import toc_block, heading, paragraph

content = [
    # Add TOC at the beginning
    toc_block(),
    
    heading(1, "Introduction"),
    paragraph("Welcome to our documentation"),
    
    heading(2, "Getting Started"),
    paragraph("First steps..."),
    
    heading(2, "Advanced Topics"),
    paragraph("Deep dive into features...")
]

client.replace_json_document(document_id, content)
```

**Features:**
- Automatically indexes all headings (h1-h6)
- Creates clickable navigation links
- Shows hierarchical document structure
- Updates automatically when content changes

**Note:** Headings created with `heading()` automatically get unique IDs required for TOC navigation.

### Anchors Block - Related Documents

Display related documents and backlinks:

```python
from vaiz import anchors_block, heading, paragraph

content = [
    anchors_block(),  # Shows related documents
    
    heading(1, "Main Content"),
    paragraph("Content here...")
]

client.replace_json_document(document_id, content)
```

**Shows:**
- Documents that this document links to
- Documents that link to this one (backlinks)
- Related documents from the space
- Knowledge graph connections

### Siblings Block - Previous/Next Navigation

Display Previous/Next navigation between documents in a sequence:

```python
from vaiz import siblings_block, heading, paragraph, horizontal_rule

content = [
    heading(1, "Tutorial Part 2: Advanced Features"),
    paragraph("Main tutorial content here..."),
    
    horizontal_rule(),
    
    # Navigation at the bottom
    siblings_block()  # Shows "← Previous" and "Next →" buttons
]

client.replace_json_document(document_id, content)
```

**Features:**
- Shows Previous and Next documents in sequence
- Creates navigation buttons (Back/Forward)
- Typically placed at page bottom
- Perfect for linear document flows

**Useful for:**
- Tutorial series (Part 1 → Part 2 → Part 3)
- Multi-chapter guides
- Documentation sequences
- Step-by-step workflows

### Code Block - Syntax Highlighting

Display code with syntax highlighting:

```python
from vaiz import code_block, heading, paragraph

python_code = '''def hello():
    print("Hello, World!")
    return True'''

content = [
    heading(1, "Code Example"),
    paragraph("Here's a Python function:"),
    
    code_block(
        code=python_code,
        language="python"
    ),
    
    paragraph("This code demonstrates a simple function.")
]

client.replace_json_document(document_id, content)
```

**Supported Languages:**
- Python, JavaScript, TypeScript, Java, C++, Go, Rust
- SQL, JSON, YAML, XML, HTML, CSS
- Bash, Shell, PowerShell
- And 50+ more languages

**Features:**
- Syntax highlighting
- Multiline code support
- Optional language specification
- Automatic formatting

### Complete Navigation Example

Combine all navigation blocks for optimal user experience:

```python
from vaiz import (
    toc_block, anchors_block, siblings_block,
    heading, paragraph, code_block, bullet_list, horizontal_rule
)

content = [
    # Top navigation: TOC and related documents
    toc_block(),
    anchors_block(),
    
    horizontal_rule(),
    
    # Main content
    heading(1, "API Documentation - Part 2"),
    
    paragraph("This guide explains how to use our API."),
    
    heading(2, "Authentication"),
    bullet_list(
        "Get API key from settings",
        "Set environment variable",
        "Initialize client"
    ),
    
    heading(2, "Example"),
    code_block(
        code='client = VaizClient(api_key="...")',
        language="python"
    ),
    
    horizontal_rule(),
    
    # Bottom navigation: Previous/Next pages
    siblings_block()  # Shows "← Part 1" and "Part 3 →"
]

client.replace_json_document(document_id, content)
```

**Navigation Layout:**
- **Top**: TOC (internal navigation) + Anchors (related docs)
- **Content**: Your document content
- **Bottom**: Siblings (Previous/Next in sequence)

## Supported Elements

All helper functions create nodes compatible with the document editor:

### Nodes
- ✅ `text()` - Text with formatting marks
- ✅ `paragraph()` - Paragraph blocks
- ✅ `heading(level)` - Headings (H1-H6) with automatic UID
- ✅ `bullet_list()` - Unordered lists
- ✅ `ordered_list()` - Numbered lists
- ✅ `list_item()` - List items with content
- ✅ `blockquote()` - Blockquotes for quotes and callouts
- ✅ `details()` - Collapsible sections
- ✅ `table()` - Tables with rows and cells
- ✅ `table_row()` - Table row
- ✅ `table_cell()` - Table cell (use for both data and headers)
- ✅ `table_header()` - Table header cell (semantic th)
- ✅ `mention_user()` - Mention a user
- ✅ `mention_document()` - Reference a document
- ✅ `mention_task()` - Reference a task
- ✅ `mention_milestone()` - Reference a milestone
- ✅ `mention(id, kind)` - Generic mention
- ✅ `image_block()` - Embed images
- ✅ `files_block()` - Attach files

### Navigation & Special Blocks
- ✅ `toc_block()` - Automatic table of contents
- ✅ `anchors_block()` - Related documents and backlinks
- ✅ `siblings_block()` - Same-level documents navigation
- ✅ `code_block()` - Code with syntax highlighting

### Marks (Formatting)
- ✅ `bold=True` - Bold text
- ✅ `italic=True` - Italic text
- ✅ `code=True` - Inline code
- ✅ `link="url"` - Hyperlinks

### Utilities
- ✅ `horizontal_rule()` - Horizontal divider line
- ✅ `link_text()` - Formatted hyperlinks

## Benefits

**Type Safety:**
- Type hints for all parameters
- IDE autocomplete support
- Catch errors before runtime

**Readability:**
- Clean, Pythonic syntax
- Self-documenting code
- Easy to understand structure

**Validation:**
- Only allows supported document elements
- Prevents invalid structures
- Ensures API compatibility

## See Also

- [Documents Guide](./documents) - Document management
- [API Reference: Document Structure](../api-reference/document-structure) - Content methods and format reference
- [API Reference: Documents](../api-reference/documents) - Document management API
- [Ready-to-Run Examples](../patterns/ready-to-run) - Complete examples

