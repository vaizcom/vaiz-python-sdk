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

## Files and Images

### Image Block

Embed images in documents and task descriptions:

```python
from vaiz import image_block, heading, paragraph

# First, upload the image
uploaded = client.upload_file("screenshots/dashboard.png")

# Create image block - simple! Just pass the file
image = image_block(
    file=uploaded.file,
    caption="Main dashboard view"
)

content = [
    heading(1, "App Screenshots"),
    paragraph("Here's our main dashboard:"),
    image
]

client.replace_json_document(document_id, content)
```

### Image with Dimensions

Specify image dimensions and aspect ratio:

```python
from vaiz import image_block, paragraph
from PIL import Image

# Get image dimensions
img = Image.open("photo.jpg")
width, height = img.size

# Upload image
uploaded = client.upload_file("photo.jpg")

# Create image block with custom width
image = image_block(
    file=uploaded.file,
    caption="Product photo",
    width_percent=75  # Display at 75% width
)

content = [
    paragraph("Product image:"),
    image
]
```

### Multiple Images

Add multiple images to a document:

```python
from vaiz import image_block, heading, paragraph

# Upload images
screenshot1 = client.upload_file("screen1.png")
screenshot2 = client.upload_file("screen2.png")
screenshot3 = client.upload_file("screen3.png")

content = [
    heading(1, "Feature Gallery"),
    
    paragraph("Login screen:"),
    image_block(
        file=screenshot1.file,
        caption="User authentication"
    ),
    
    paragraph("Dashboard:"),
    image_block(
        file=screenshot2.file,
        caption="Main dashboard view"
    ),
    
    paragraph("Settings:"),
    image_block(
        file=screenshot3.file,
        caption="Configuration panel"
    )
]

client.replace_json_document(document_id, content)
```

### Files Block

Attach files (PDFs, documents, etc.) to documents:

```python
from vaiz import files_block, heading, paragraph

# Upload files
pdf = client.upload_file("report.pdf")
excel = client.upload_file("data.xlsx")

# Create file items
file1 = {
    "fileId": pdf.file.id,
    "url": pdf.file.url,
    "name": "Q4 Report.pdf",
    "size": pdf.file.size,
    "extension": "pdf",
    "type": "Pdf"
}

file2 = {
    "fileId": excel.file.id,
    "url": excel.file.url,
    "name": "Sales Data.xlsx",
    "size": excel.file.size,
    "extension": "xlsx",
    "type": "Excel"
}

content = [
    heading(1, "Quarterly Report"),
    paragraph("Attached documents:"),
    files_block(file1, file2)
]

client.replace_json_document(document_id, content)
```

### Single File Attachment

Attach a single file:

```python
from vaiz import files_block, paragraph

# Upload document
uploaded = client.upload_file("presentation.pptx")

# Create file item
file_item = {
    "fileId": uploaded.file.id,
    "url": uploaded.file.url,
    "name": "Product Presentation.pptx",
    "size": uploaded.file.size,
    "extension": "pptx",
    "type": "PowerPoint"
}

content = [
    paragraph("Download the presentation:"),
    files_block(file_item)
]
```

### Mixed File Types

Attach various file types together:

```python
from vaiz import files_block, heading, paragraph

# Upload different file types
pdf = client.upload_file("manual.pdf")
video = client.upload_file("demo.mp4")
zip_file = client.upload_file("source.zip")

files = [
    {
        "fileId": pdf.file.id,
        "url": pdf.file.url,
        "name": "User Manual.pdf",
        "size": pdf.file.size,
        "extension": "pdf",
        "type": "Pdf"
    },
    {
        "fileId": video.file.id,
        "url": video.file.url,
        "name": "Product Demo.mp4",
        "size": video.file.size,
        "extension": "mp4",
        "type": "Video"
    },
    {
        "fileId": zip_file.file.id,
        "url": zip_file.file.url,
        "name": "Source Code.zip",
        "size": zip_file.file.size,
        "extension": "zip",
        "type": "Archive"
    }
]

content = [
    heading(1, "Release Package"),
    paragraph("Download all release materials:"),
    files_block(*files)  # Unpack list
]

client.replace_json_document(document_id, content)
```

### Supported File Types

The `type` field in file items can be:

| Type | Extension Examples | Description |
|------|-------------------|-------------|
| `Pdf` | `.pdf` | PDF documents |
| `Image` | `.png`, `.jpg`, `.gif`, `.webp` | Images (use `image_block` instead) |
| `Video` | `.mp4`, `.mov`, `.avi` | Video files |
| `Excel` | `.xlsx`, `.xls`, `.csv` | Spreadsheets |
| `PowerPoint` | `.pptx`, `.ppt` | Presentations |
| `Word` | `.docx`, `.doc` | Word documents |
| `Archive` | `.zip`, `.rar`, `.tar.gz` | Compressed archives |
| `Text` | `.txt`, `.md` | Text files |
| `Code` | `.py`, `.js`, `.java`, etc. | Source code files |
| `Other` | Any other extension | Generic files |

### Complete Files and Images Example

```python
from vaiz import (
    VaizClient, heading, paragraph, text,
    image_block, files_block, horizontal_rule
)

client = VaizClient(api_key="...", space_id="...")

# Upload all files
logo = client.upload_file("company_logo.png")
screenshot = client.upload_file("app_screen.png")
report_pdf = client.upload_file("annual_report.pdf")
data_csv = client.upload_file("data_export.csv")

# Build document with mixed content
content = [
    heading(1, "📊 Annual Report 2024"),
    
    # Logo image
    image_block(
        file=logo.file,
        width_percent=50,  # Display at 50% width
        caption="Company Logo"
    ),
    
    horizontal_rule(),
    
    # Report content
    heading(2, "Executive Summary"),
    paragraph("Our annual performance and achievements..."),
    
    # Screenshot
    heading(2, "New Features"),
    paragraph("We launched a redesigned application:"),
    image_block(
        file=screenshot.file,
        caption="New dashboard interface"
    ),
    
    horizontal_rule(),
    
    # Downloadable files
    heading(2, "📎 Attachments"),
    paragraph(text("Download the full report and data:", bold=True)),
    files_block(
        {
            "fileId": report_pdf.file.id,
            "url": report_pdf.file.url,
            "name": "Annual Report 2024.pdf",
            "size": report_pdf.file.size,
            "extension": "pdf",
            "type": "Pdf"
        },
        {
            "fileId": data_csv.file.id,
            "url": data_csv.file.url,
            "name": "Financial Data.csv",
            "size": data_csv.file.size,
            "extension": "csv",
            "type": "Excel"
        }
    )
]

# Update document
client.replace_json_document(document_id, content)
```

### Using with Task Descriptions

Images and files work great in task descriptions:

```python
from vaiz import CreateTaskRequest, image_block, files_block, heading, paragraph

# Upload files
screenshot = client.upload_file("bug_screenshot.png")
log_file = client.upload_file("error_log.txt")

# Build description with image and file
description_content = [
    heading(2, "Bug Report"),
    paragraph("Application crashes when clicking submit button."),
    
    heading(3, "Screenshot"),
    image_block(
        file=screenshot.file,
        caption="Error state"
    ),
    
    heading(3, "Logs"),
    files_block({
        "fileId": log_file.file.id,
        "url": log_file.file.url,
        "name": "error.log",
        "size": log_file.file.size,
        "extension": "txt",
        "type": "Text"
    })
]

# Create task with rich description
task = CreateTaskRequest(
    name="Fix submit button crash",
    description_json=description_content
)

client.create_task(task)
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

### Embed Block - External Content

Embed external content from various platforms:

```python
from vaiz import embed_block, heading, paragraph, horizontal_rule

content = [
    heading(1, "Project Resources"),
    
    # YouTube video
    heading(2, "Demo Video"),
    paragraph("Watch our product demo:"),
    embed_block(
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        size="large"
    ),
    
    horizontal_rule(),
    
    # Figma design
    heading(2, "Design Mockups"),
    paragraph("View the design files:"),
    embed_block(
        url="https://www.figma.com/file/example",
        size="large",
        is_content_hidden=True
    ),
    
    horizontal_rule(),
    
    # CodeSandbox
    heading(2, "Live Code Example"),
    paragraph("Try the code live:"),
    embed_block(url="https://codesandbox.io/s/example"),
    
    horizontal_rule(),
    
    # Generic iframe (default)
    heading(2, "External Tool"),
    embed_block(url="https://example.com/embed")
]

client.replace_json_document(document_id, content)
```

**Supported Embed Types:**
- YouTube - YouTube videos
- Figma - Figma design files
- Vimeo - Vimeo videos
- CodeSandbox - Interactive code sandboxes
- GitHub Gist - GitHub code snippets
- Miro - Miro whiteboards
- Iframe - Generic iframe embeds (default)

See [EmbedType enum](../api-reference/enums#embedtype) for type-safe values.

**Parameters:**
- `url` - URL of content to embed
- `embed_type` - Type of embed (optional, see [EmbedType](../api-reference/enums#embedtype))
- `size` - Display size: `"small"`, `"medium"`, `"large"` (default: `"medium"`)
- `is_content_hidden` - Hide content by default for Figma/Miro (default: `False`)

**Use Cases:**
- Video tutorials and demos
- Design system documentation
- Live code examples
- Interactive prototypes
- External tool integrations

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
- ✅ `code_block()` - Code with syntax highlighting
- ✅ `embed_block()` - Embed external content (YouTube, Figma, etc.)

### Navigation Blocks
- ✅ `toc_block()` - Automatic table of contents
- ✅ `anchors_block()` - Related documents and backlinks
- ✅ `siblings_block()` - Same-level documents navigation

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

