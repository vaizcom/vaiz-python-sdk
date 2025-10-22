"""
Module demonstrating milestone toggle functionality (attach/detach tasks to/from milestones).
"""

from vaiz.models import ToggleMilestoneRequest
from .config import get_client

def toggle_milestone(task_id: str = None, milestone_id: str = None):
    """Toggle milestone assignment for a task using the Vaiz SDK."""
    client = get_client()
    
    # If no task_id provided, find an existing task
    if not task_id:
        print("No task ID provided, finding an existing task...")
        # We could try to get tasks, but that would require implementing getTasks
        # For now, we'll just indicate this limitation
        print("Please provide a task_id parameter!")
        return None
    
    # If no milestone_id provided, get one from the list
    if not milestone_id:
        print("No milestone ID provided, getting first available milestone...")
        milestones_response = client.get_milestones()
        if not milestones_response.milestones:
            print("No milestones available!")
            return None
        milestone_id = milestones_response.milestones[0].id
        print(f"Using milestone ID: {milestone_id}")
    
    # Toggle the milestone on the task
    toggle_request = ToggleMilestoneRequest(
        task_id=task_id,
        milestone_ids=[milestone_id]
    )

    try:
        response = client.toggle_milestone(toggle_request)
        task = response.task
        
        print("Milestone toggle successful!")
        print(f"Response type: {response.type}")
        print(f"\nTask Details:")
        print(f"ID: {task.id}")
        print(f"Name: {task.name}")
        print(f"Board: {task.board}")
        print(f"Project: {task.project}")
        print(f"Priority: {task.priority}")
        print(f"Completed: {task.completed}")
        print(f"Milestones: {task.milestones}")
        print(f"Main Milestone: {task.milestone}")
        print(f"Assignees: {task.assignees}")
        print(f"Creator: {task.creator}")
        print(f"Editor: {task.editor}")
        print(f"Created At: {task.createdAt}")
        print(f"Updated At: {task.updatedAt}")
        
        # Check if milestone was added or removed
        if milestone_id in task.milestones:
            print(f"\n✅ Milestone {milestone_id} was ATTACHED to the task")
        else:
            print(f"\n❌ Milestone {milestone_id} was DETACHED from the task")
        
        return task.id
    except Exception as e:
        print(f"Error toggling milestone: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return None

def demo_toggle_milestone():
    """Demo function that creates a task and milestone, then toggles them."""
    from vaiz.models import CreateTaskRequest, CreateMilestoneRequest, TaskPriority
    from .config import BOARD_ID, PROJECT_ID, GROUP_ID
    
    client = get_client()
    
    print("Creating a demo task and milestone...")
    
    # Create a test task
    task_request = CreateTaskRequest(
        name="Demo Task for Milestone Toggle",
        group=GROUP_ID,
        board=BOARD_ID,
        priority=TaskPriority.Medium,
        completed=False
    )
    
    task_response = client.create_task(task_request)
    task_id = task_response.task.id
    print(f"Created task: {task_id}")
    
    # Create a test milestone
    milestone_request = CreateMilestoneRequest(
        name="Demo Milestone for Toggle",
        board=BOARD_ID,
        project=PROJECT_ID
    )
    
    milestone_response = client.create_milestone(milestone_request)
    milestone_id = milestone_response.milestone.id
    print(f"Created milestone: {milestone_id}")
    
    print("\nToggling milestone on task (first time - should attach)...")
    toggle_milestone(task_id, milestone_id)
    
    print("\nToggling milestone on task (second time - should detach)...")
    toggle_milestone(task_id, milestone_id)

if __name__ == "__main__":
    # demo_toggle_milestone()  # Uncomment to run full demo
    toggle_milestone()  # This will ask for parameters 