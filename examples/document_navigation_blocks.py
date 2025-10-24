"""
Example demonstrating all document navigation blocks: TOC, Anchors, and Siblings.

This example shows how to create a document with automatic navigation features:
- Table of Contents (TOC) for internal document navigation
- Anchors for displaying related documents and backlinks
- Siblings for showing documents at the same hierarchical level
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
    # Automatic table of contents
    toc_block(),
    
    # Related documents and backlinks
    anchors_block(),
    
    # Sibling documents navigation
    siblings_block(),
    
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
    
    heading(2, "Siblings Block - Same Level Documents"),
    
    paragraph(
        "The ",
        text("siblings_block()", code=True),
        " shows documents at the same hierarchical level:"
    ),
    
    bullet_list(
        "Documents in the same folder/collection",
        "Documents at the same level in structure",
        "Useful for series of related pages (guides, tutorials)"
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
        '''from vaiz import toc_block, anchors_block, siblings_block

content = [
    toc_block(),        # Table of contents
    anchors_block(),    # Related documents
    siblings_block(),   # Sibling documents
    
    heading(1, "Main Content"),
    paragraph("Your content here...")
]

client.replace_json_document(document_id, content)''',
        code=True
    )),
    
    horizontal_rule(),
    
    heading(1, "Best Practices"),
    
    bullet_list(
        "Place TOC block at the document start for better accessibility",
        "Use Anchors block for documentation with cross-references",
        "Use Siblings block for series of related pages",
        "For short documents (< 3 sections), TOC may be redundant"
    ),
    
    paragraph(
        text("Tip: ", bold=True),
        "Combine these blocks with ",
        text("mention_document()", code=True),
        " to create links between documents and populate the Anchors block!"
    ),
]

try:
    response = client.replace_json_document(DOCUMENT_ID, content)
    print("✅ Document created successfully!")
    print()
    print("What was added:")
    print("  • TOC block - automatic table of contents")
    print("  • Anchors block - related documents and backlinks")
    print("  • Siblings block - same-level documents")
    print("  • Headings with UIDs for navigation")
    print()
    print(f"Open document in Vaiz: {DOCUMENT_ID}")
    print()
except Exception as e:
    print(f"❌ Error: {e}")

