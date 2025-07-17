"""
Module demonstrating milestone editing functionality with datetime objects.
"""

from datetime import datetime
from vaiz.models import EditMilestoneRequest
from .config import get_client

def edit_milestone(milestone_id: str = None):
    """Edit an existing milestone using the Vaiz SDK with datetime objects."""
    client = get_client()
    
    # If no milestone_id provided, get one from the list
    if not milestone_id:
        print("No milestone ID provided, getting first available milestone...")
        milestones_response = client.get_milestones()
        if not milestones_response.milestones:
            print("No milestones available!")
            return None
        milestone_id = milestones_response.milestones[0].id
        print(f"Using milestone ID: {milestone_id}")
    
    # Get the current milestone to show before/after
    print("\nBefore edit:")
    before_response = client.get_milestone(milestone_id)
    print(f"Name: {before_response.milestone.name}")
    print(f"Description: {before_response.milestone.description}")
    print(f"Due End: {before_response.milestone.due_end}")
    
    # Edit the milestone with datetime objects
    edit_request = EditMilestoneRequest(
        milestone_id=milestone_id,
        name="Updated Milestone Name (SDK Edit)",
        description="This milestone was updated using the SDK with datetime objects",
        due_start=datetime(2025, 6, 1, 9, 0, 0),      # June 1st, 9:00 AM  
        due_end=datetime(2025, 12, 31, 23, 59, 59)    # December 31st, 11:59 PM
    )

    try:
        response = client.edit_milestone(edit_request)
        milestone = response.milestone
        
        print("\n✅ Milestone edited successfully!")
        print(f"Response type: {response.type}")
        print(f"\nAfter edit:")
        print(f"ID: {milestone.id}")
        print(f"Name: {milestone.name}")
        print(f"Description: {milestone.description}")
        print(f"Due Start: {milestone.due_start} ({type(milestone.due_start).__name__})")
        print(f"Due End: {milestone.due_end} ({type(milestone.due_end).__name__})")
        print(f"Project: {milestone.project}")
        print(f"Board: {milestone.board}")
        print(f"Document: {milestone.document}")
        print(f"Total Tasks: {milestone.total}")
        print(f"Completed Tasks: {milestone.completed}")
        print(f"Progress: {milestone.completed}/{milestone.total} ({(milestone.completed/milestone.total*100):.1f}%)" if milestone.total > 0 else "Progress: 0/0 (0%)")
        print(f"Followers: {milestone.followers}")
        print(f"Creator: {milestone.creator}")
        print(f"Editor: {milestone.editor}")
        print(f"Created At: {milestone.created_at}")
        print(f"Updated At: {milestone.updated_at}")
        
        return milestone.id
    except Exception as e:
        print(f"Error editing milestone: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

if __name__ == "__main__":
    edit_milestone() 