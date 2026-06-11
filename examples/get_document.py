"""
Example: Fetch document content as Markdown by document ID.
"""

from examples.config import get_client


def main():
    client = get_client()
    client.verbose = True

    # Example document ID
    document_id = "6878ff0ad2c2d60e246402c2"

    markdown = client.get_markdown_document(document_id)
    print("\n=== Document Markdown ===")
    print(markdown)
    print("=========================\n")


if __name__ == "__main__":
    main()
