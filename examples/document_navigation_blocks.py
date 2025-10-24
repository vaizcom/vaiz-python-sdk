"""
Example demonstrating all document navigation blocks: TOC, Anchors, and Siblings.

This example shows how to create a document with automatic navigation features:
- Table of Contents (TOC) for internal document navigation (top)
- Anchors for displaying related documents and backlinks (top)
- Siblings for Previous/Next navigation between documents (bottom)
"""

from config import get_client
from vaiz import (
    toc_block,
    anchors_block,
    siblings_block,
    heading,
    paragraph,
    bullet_list,
    horizontal_rule,
    text,
    link_text,
)

# Initialize client
client = get_client()

# Document ID (replace with your actual document ID)
DOCUMENT_ID = "68fb2452322665c43876937d"

print("Creating document with navigation blocks...")
print("=" * 80)

# Create document content with all navigation blocks
content = [
    # Top navigation: TOC and related documents
    toc_block(),
    anchors_block(),
    
    horizontal_rule(),
    
    # Main content
    heading(1, "Document Navigation Features"),
    
    paragraph(
        "This document demonstrates the three types of ",
        text("navigation blocks", bold=True),
        " available in Vaiz: TOC, Anchors, and Siblings."
    ),
    
    horizontal_rule(),
    
    heading(2, "TOC Block - Table of Contents"),
    
    paragraph(
        "The ",
        text("toc_block()", code=True),
        " automatically generates an interactive table of contents:"
    ),
    
    bullet_list(
        "Shows hierarchical document structure (h1-h6)",
        "Creates clickable links for quick navigation",
        "Updates automatically when document changes"
    ),
    
    heading(2, "Anchors Block - Related Documents"),
    
    paragraph(
        "The ",
        text("anchors_block()", code=True),
        " displays document relationships:"
    ),
    
    bullet_list(
        "Documents that this document links to",
        "Documents that link to this one (backlinks)",
        "Related documents from the same space"
    ),
    
    heading(2, "Siblings Block - Previous/Next Navigation"),
    
    paragraph(
        "The ",
        text("siblings_block()", code=True),
        " provides Previous/Next navigation between documents in a sequence:"
    ),
    
    bullet_list(
        "Shows Previous and Next documents in the sequence",
        "Creates navigation buttons (Back/Forward)",
        "Typically placed at the bottom of the page",
        "Perfect for tutorial series and sequential guides"
    ),
    
    horizontal_rule(),
    
    heading(1, "Usage Examples"),
    
    heading(2, "Basic TOC Usage"),
    
    paragraph(text(
        '''from vaiz import toc_block, heading, paragraph

content = [
    toc_block(),
    heading(1, "Introduction"),
    paragraph("Welcome to our document"),
    heading(2, "Getting Started"),
    paragraph("First steps...")
]

client.replace_json_document(document_id, content)''',
        code=True
    )),
    
    heading(2, "All Navigation Blocks Together"),
    
    paragraph(text(
        '''from vaiz import toc_block, anchors_block, siblings_block, horizontal_rule

content = [
    # Top navigation
    toc_block(),        # Table of contents
    anchors_block(),    # Related documents
    
    horizontal_rule(),
    
    # Your content
    heading(1, "Tutorial Part 2"),
    paragraph("Main content here..."),
    
    horizontal_rule(),
    
    # Bottom navigation
    siblings_block()    # Previous/Next buttons
]

client.replace_json_document(document_id, content)''',
        code=True
    )),
    
    horizontal_rule(),
    
    heading(1, "Best Practices"),
    
    bullet_list(
        "Place TOC and Anchors blocks at the document start for better accessibility",
        "Place Siblings block at the document end for Previous/Next navigation",
        "Use Anchors block for documentation with cross-references",
        "Use Siblings block for tutorial series and sequential guides",
        "For short documents (< 3 sections), TOC may be redundant"
    ),
    
    paragraph(
        text("Tip: ", bold=True),
        "Combine these blocks with ",
        text("mention_document()", code=True),
        " to create links between documents and populate the Anchors block!"
    ),
    
    horizontal_rule(),
    
    # Bottom navigation - demonstrate siblings placement
    siblings_block(),
]

try:
    response = client.replace_json_document(DOCUMENT_ID, content)
    print("✅ Document created successfully!")
    print()
    print("What was added:")
    print("  • TOC block (top) - automatic table of contents")
    print("  • Anchors block (top) - related documents and backlinks")
    print("  • Siblings block (bottom) - Previous/Next navigation")
    print("  • Headings with UIDs for TOC navigation")
    print()
    print("Navigation layout:")
    print("  ┌─────────────────────────┐")
    print("  │ TOC Block               │  ← Internal navigation")
    print("  │ Anchors Block           │  ← Related docs")
    print("  ├─────────────────────────┤")
    print("  │ Content...              │")
    print("  ├─────────────────────────┤")
    print("  │ Siblings Block          │  ← Previous/Next")
    print("  └─────────────────────────┘")
    print()
    print(f"Open document in Vaiz: {DOCUMENT_ID}")
    print()
except Exception as e:
    print(f"❌ Error: {e}")

