"""
Module demonstrating milestone creation functionality.
"""

from vaiz.models import CreateMilestoneRequest
from .config import get_client, BOARD_ID, PROJECT_ID

def create_milestone():
    """Create a new milestone using the Vaiz SDK."""
    client = get_client()
    
    milestone = CreateMilestoneRequest(
        name="Test Milestone SDK",
        board=BOARD_ID,
        project=PROJECT_ID
    )

    try:
        response = client.create_milestone(milestone)
        print("Milestone created successfully!")
        print(f"Response type: {response.type}")
        print(f"Milestone ID: {response.milestone.id}")
        print(f"Milestone name: {response.milestone.name}")
        print(f"Milestone description: {response.milestone.description}")  # Empty by default, set via edit method
        print(f"Due date: {response.milestone.due_end}")  # None by default, set via edit method
        print(f"Board: {response.milestone.board}")
        print(f"Project: {response.milestone.project}")
        print(f"Total tasks: {response.milestone.total}")
        print(f"Completed tasks: {response.milestone.completed}")
        print(f"Creator: {response.milestone.creator}")
        print(f"Document: {response.milestone.document}")
        print(f"Created at: {response.milestone.created_at}")
        print(f"Updated at: {response.milestone.updated_at}")
        print(f"Followers: {response.milestone.followers}")
        return response.milestone.id
    except Exception as e:
        print(f"Error creating milestone: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    create_milestone() 