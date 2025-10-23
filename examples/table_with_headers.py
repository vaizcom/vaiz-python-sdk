#!/usr/bin/env python3
"""
Example: Using table_header() for semantic table headers

This example demonstrates the new table_header() function that creates
proper HTML <th> elements instead of <td> for better accessibility
and semantic structure.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import get_client
from vaiz import (
    heading, paragraph, text, table, table_row, 
    table_cell, table_header, horizontal_rule
)
from vaiz.models import CreateDocumentRequest, Kind


def main():
    print("=== Table Header Example ===\n")
    
    client = get_client()
    
    # Get current user's member ID for Personal document
    profile = client.get_profile()
    member_id = profile.profile.member_id
    
    # Create Personal document
    doc_response = client.create_document(
        CreateDocumentRequest(
            kind=Kind.Member,
            kind_id=member_id,
            title="Table Headers Demo",
            index=0
        )
    )
    document_id = doc_response.payload.document.id
    print(f"✅ Document created: {document_id}\n")
    
    # Build document with various table examples
    content = [
        heading(1, "📊 Table Headers Demo"),
        
        paragraph(
            "This document demonstrates the ",
            text("table_header()", code=True),
            " function for creating semantic table headers."
        ),
        
        horizontal_rule(),
        
        heading(2, "Example 1: Simple Table with Headers"),
        
        paragraph("Using table_header() for proper semantic HTML structure:"),
        
        table(
            table_row(
                table_header("Task"),
                table_header("Assignee"),
                table_header("Status"),
                table_header("Priority")
            ),
            table_row("Implement API", "John", "✅ Done", "High"),
            table_row("Write tests", "Jane", "⏳ In Progress", "High"),
            table_row("Documentation", "Mike", "📋 Todo", "Medium")
        ),
        
        horizontal_rule(),
        
        heading(2, "Example 2: Table with Merged Header"),
        
        paragraph("Headers support colspan and rowspan just like cells:"),
        
        table(
            # Main header spanning all columns
            table_row(
                table_header(paragraph(text("Q1-Q4 2025 Performance", bold=True)), colspan=5)
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
            table_row("Users", "1,000", "1,500", "2,200", "3,000"),
            table_row("Growth", "+20%", "+25%", "+30%", "+35%"),
            # Summary row
            table_row(
                table_cell(paragraph(text("Total Revenue", bold=True))),
                table_cell(paragraph(text("$550K", bold=True)), colspan=4)
            )
        ),
        
        horizontal_rule(),
        
        heading(2, "Example 3: Complex Headers"),
        
        paragraph("Multiple header rows with different spans:"),
        
        table(
            # Top header
            table_row(
                table_header(""),
                table_header(paragraph(text("Frontend", bold=True)), colspan=2),
                table_header(paragraph(text("Backend", bold=True)), colspan=2)
            ),
            # Sub-headers
            table_row(
                table_header("Team"),
                table_header("React"),
                table_header("Vue"),
                table_header("Node.js"),
                table_header("Python")
            ),
            # Data rows
            table_row("Team A", "3", "2", "2", "1"),
            table_row("Team B", "2", "1", "3", "2"),
            table_row(
                table_cell(paragraph(text("Total", bold=True))),
                table_cell("5"),
                table_cell("3"),
                table_cell("5"),
                table_cell("3")
            )
        ),
        
        horizontal_rule(),
        
        heading(2, "Benefits"),
        
        paragraph(text("Why use table_header()?", bold=True)),
        
        paragraph(
            "• ", text("Semantic HTML", bold=True), " - Creates proper ",
            text("<th>", code=True), " elements instead of ", text("<td>", code=True)
        ),
        paragraph(
            "• ", text("Accessibility", bold=True), " - Screen readers can identify headers"
        ),
        paragraph(
            "• ", text("Consistent styling", bold=True), " - Headers are styled appropriately"
        ),
        paragraph(
            "• ", text("Full feature support", bold=True), " - Works with colspan, rowspan, and formatting"
        ),
        
        horizontal_rule(),
        
        paragraph(
            text("Created with Vaiz Python SDK ", italic=True),
            text("v0.9+", code=True)
        )
    ]
    
    # Replace document content
    response = client.replace_json_document(document_id, content)
    print("✅ Document populated with table header examples")
    
    # Verify
    saved = client.get_json_document(document_id)
    saved_blocks = saved.get("default", {}).get("content", [])
    tables = [b for b in saved_blocks if b.get("type") == "extension-table"]
    
    print(f"✅ Created {len(tables)} tables with proper headers")
    print(f"\nDocument ID: {document_id}")
    print("View this document in Vaiz to see the table headers!")


if __name__ == "__main__":
    main()

