"""
Example: Fetch JSON document content by document ID.
"""

from examples.config import get_client


def main():
    client = get_client()
    client.verbose = True

    # Example document ID
    document_id = "6878ff0ad2c2d60e246402c2"

    doc = client.get_document_body(document_id)
    print("\n=== Document JSON ===")
    # Print only top-level keys to avoid huge output
    if isinstance(doc, dict):
        print(f"keys: {list(doc.keys())}")
    else:
        print(doc)
    print("====================\n")


if __name__ == "__main__":
    main()


