"""
Module demonstrating milestone creation functionality with datetime objects.
"""

from datetime import datetime
from vaiz.models import CreateMilestoneRequest
from .config import get_client, BOARD_ID, PROJECT_ID

def create_milestone():
    """Create a new milestone using the Vaiz SDK with datetime objects."""
    client = get_client()
    
    # Example 1: Simple milestone without dates
    milestone = CreateMilestoneRequest(
        name="Test Milestone SDK",
        board=BOARD_ID,
        project=PROJECT_ID
    )

    try:
        response = client.create_milestone(milestone)
        print("✅ Milestone created successfully!")
        print(f"Response type: {response.type}")
        print(f"Milestone ID: {response.milestone.id}")
        print(f"Milestone name: {response.milestone.name}")
        print(f"Due date: {response.milestone.due_end}")  # None by default
        
        # Example 2: Milestone with datetime objects
        print("\n📅 Creating milestone with datetime objects...")
        milestone_with_dates = CreateMilestoneRequest(
            name="Q1 Milestone with Dates",
            description="Milestone with start and end dates",
            board=BOARD_ID,
            project=PROJECT_ID,
            due_start=datetime(2025, 3, 1, 9, 0, 0),      # March 1st, 9:00 AM
            due_end=datetime(2025, 3, 31, 17, 0, 0),      # March 31st, 5:00 PM
            color="#4CAF50"  # Green color
        )
        
        response2 = client.create_milestone(milestone_with_dates)
        print("✅ Milestone with dates created!")
        print(f"Due start: {response2.milestone.due_start} ({type(response2.milestone.due_start).__name__})")
        print(f"Due end: {response2.milestone.due_end} ({type(response2.milestone.due_end).__name__})")

    except Exception as e:
        print(f"Error creating milestone: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    create_milestone() 