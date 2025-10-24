"""
Example: Create a document with various embed blocks (YouTube, Figma, CodeSandbox, etc.).

This example demonstrates how to use the embed_block() helper to create documents
with embedded content from various platforms.
"""

from examples.config import get_client
from vaiz import (
    heading,
    paragraph,
    text,
    embed_block,
    EmbedType,
    horizontal_rule,
    bullet_list
)


def main():
    client = get_client()
    client.verbose = True

    # Replace with your actual document ID
    document_id = "YOUR_DOCUMENT_ID"

    # Build document with various embed blocks
    content = [
        heading(1, "🎬 Embed Blocks Examples"),
        
        paragraph(
            "This document demonstrates different types of embed blocks supported by Vaiz."
        ),
        
        horizontal_rule(),
        
        # YouTube embed
        heading(2, "YouTube Video"),
        paragraph("Embed a YouTube video:"),
        embed_block(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            embed_type=EmbedType.YOUTUBE,
            size="large"
        ),
        
        horizontal_rule(),
        
        # Figma embed
        heading(2, "Figma Design"),
        paragraph("Embed a Figma design file:"),
        embed_block(
            url="https://www.figma.com/file/example",
            embed_type=EmbedType.FIGMA,
            size="large",
            is_content_hidden=True
        ),
        
        horizontal_rule(),
        
        # Vimeo embed
        heading(2, "Vimeo Video"),
        paragraph("Embed a Vimeo video:"),
        embed_block(
            url="https://vimeo.com/123456789",
            embed_type=EmbedType.VIMEO
        ),
        
        horizontal_rule(),
        
        # CodeSandbox embed
        heading(2, "CodeSandbox"),
        paragraph("Embed a live code sandbox:"),
        embed_block(
            url="https://codesandbox.io/s/example",
            embed_type=EmbedType.CODESANDBOX,
            size="large"
        ),
        
        horizontal_rule(),
        
        # GitHub Gist embed
        heading(2, "GitHub Gist"),
        paragraph("Embed a GitHub Gist:"),
        embed_block(
            url="https://gist.github.com/username/1234567890abcdef",
            embed_type=EmbedType.GITHUB_GIST
        ),
        
        horizontal_rule(),
        
        # Miro board embed
        heading(2, "Miro Board"),
        paragraph("Embed a Miro whiteboard:"),
        embed_block(
            url="https://miro.com/app/board/example",
            embed_type=EmbedType.MIRO,
            size="large",
            is_content_hidden=True
        ),
        
        horizontal_rule(),
        
        # Generic Iframe embed (default, no embed_type needed)
        heading(2, "Generic Iframe"),
        paragraph("Embed any webpage using iframe:"),
        embed_block(
            url="https://example.com/embed",
            size="medium"
        ),
        
        horizontal_rule(),
        
        # Summary
        heading(2, "📝 Summary"),
        paragraph(text("Supported embed types:", bold=True)),
        bullet_list(
            "YouTube - Video hosting",
            "Figma - Design files",
            "Vimeo - Video hosting",
            "CodeSandbox - Live code editor",
            "GitHub Gist - Code snippets",
            "Miro - Collaborative whiteboard",
            "Iframe - Generic web content"
        ),
        
        paragraph(
            text("Size options:", bold=True),
            text(" small, medium, large")
        ),
        
        paragraph(
            text("Note:", bold=True),
            text(" For Figma and Miro embeds, you can use "),
            text("is_content_hidden=True", code=True),
            text(" to hide the content by default.")
        )
    ]

    # Replace document content
    print("\n=== Creating Document with Embed Blocks ===")
    response = client.replace_json_document(document_id, content)
    print(f"✅ Document updated successfully!")
    print(f"Document ID: {document_id}")
    print("=" * 50)


if __name__ == "__main__":
    main()

