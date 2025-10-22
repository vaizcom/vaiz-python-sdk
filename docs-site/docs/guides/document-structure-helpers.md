---
sidebar_position: 16
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

### Table with Formatting

Add formatting to table content:

```python
from vaiz import table, table_row, table_cell, text, paragraph

formatted_table = table(
    table_row(
        table_cell(paragraph(text("Name", bold=True))),
        table_cell(paragraph(text("Status", bold=True)))
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
from vaiz import heading, paragraph, table, table_row, text

content = [
    heading(1, "📊 Project Metrics"),
    
    paragraph("Current sprint status:"),
    
    table(
        table_row("Metric", "Count", "Percentage"),  # Header row
        table_row("Completed", "28", "60%"),
        table_row("In Progress", "12", "26%"),
        table_row("Todo", "7", "14%")
    ),
    
    paragraph(text("Total: 47 tasks", bold=True))
]
```

## Visual Elements

### Separator

Create visual separator lines:

```python
from vaiz import separator

# Default separator (━━━━━━...)
separator()

# Custom character and length
separator("—", 50)
separator("*", 30)
```

## Complete Example

Build a full document with helpers:

```python
from vaiz import (
    VaizClient, text, paragraph, heading, 
    bullet_list, ordered_list, list_item, 
    link_text, separator
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
    
    separator(),
    
    # Overview
    heading(2, "Overview"),
    paragraph(
        "This project uses ",
        text("Vaiz SDK", bold=True),
        " for task management. Visit ",
        link_text("docs", "https://docs.vaiz.app"),
        " to learn more."
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
    separator(),
    paragraph(
        text("Built with ", italic=True),
        text("document structure helpers", code=True)
    )
]

# Replace document
client.replace_json_document("document_id", content)
```

## Supported Elements

All helper functions create nodes compatible with the document editor:

### Nodes
- ✅ `text()` - Text with formatting marks
- ✅ `paragraph()` - Paragraph blocks
- ✅ `heading(level)` - Headings (H1-H6)
- ✅ `bullet_list()` - Unordered lists
- ✅ `ordered_list()` - Numbered lists
- ✅ `list_item()` - List items with content
- ✅ `table()` - Tables with rows and cells
- ✅ `table_row()` - Table row
- ✅ `table_cell()` - Table cell (use for both data and headers)

### Marks (Formatting)
- ✅ `bold=True` - Bold text
- ✅ `italic=True` - Italic text
- ✅ `code=True` - Inline code
- ✅ `link="url"` - Hyperlinks

### Utilities
- ✅ `separator()` - Visual dividers
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

