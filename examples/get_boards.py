from vaiz import VaizClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def main():
    # Initialize client
    client = VaizClient(
        api_key=os.getenv("VAIZ_API_KEY"),
        space_id=os.getenv("VAIZ_SPACE_ID"),
        verify_ssl=False,  # Set to True in production
        base_url="https://api.vaiz.local:10000/v4"  # Use appropriate base URL for your environment
    )

    # Get all boards
    response = client.get_boards()

    # Print board information
    print(f"Found {len(response.payload.boards)} boards:")
    for board in response.payload.boards:
        print(f"\nBoard: {board.name}")
        print(f"ID: {board.id}")
        print(f"Project: {board.project}")
        print(f"Creator: {board.creator}")
        print(f"Archiver: {board.archiver}")
        print(f"Archived At: {board.archived_at}")
        print(f"Created At: {board.created_at}")
        print(f"Deleter: {board.deleter}")
        print(f"Deleted At: {board.deleted_at}")
        print(f"Updated At: {board.updated_at}")
        print(f"Groups: {[g.name for g in (board.groups or [])]}")
        print(f"Types: {[t.label for t in (board.types_list or [])]}")
        print(f"Custom Fields: {[cf.name for cf in (board.custom_fields or [])]}")
        print(f"Task Order By Groups: {board.task_order_by_groups}")

if __name__ == "__main__":
    main() 