#!/usr/bin/env python3
"""
Example: Get Tasks

This example demonstrates how to retrieve tasks using the getTasks method
with optional filtering by assignees and pagination parameters.
"""

from vaiz.models import GetTasksRequest
from examples.config import get_client


def main():
    """Get tasks with different filter and pagination options."""
    client = get_client()

    print("=== Get Tasks Examples ===\n")

    # Example 1: Get all tasks with default pagination (limit=50, skip=0)
    print("1. Getting all tasks with default pagination...")
    try:
        request = GetTasksRequest()
        response = client.get_tasks(request)

        print(f"Response type: {response.type}")
        print(f"Number of tasks returned: {len(response.payload.tasks)}")

        if response.payload.tasks:
            print("\nFirst task details:")
            first_task = response.payload.tasks[0]
            print(f"  ID: {first_task.id}")
            print(f"  Name: {first_task.name}")
            print(f"  HRID: {first_task.hrid}")
            print(f"  Completed: {first_task.completed}")
            print(f"  Assignees: {first_task.assignees}")
            print(f"  Priority: {first_task.priority}")

    except Exception as e:
        print(f"Error getting all tasks: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 2: Get tasks filtered by specific assignees
    print("2. Getting tasks filtered by assignees...")
    try:
        # Replace with actual user IDs from your space
        assignee_ids = ["68c19e08020b3f8c50a814c1"]  # Example from the API response

        request = GetTasksRequest(assignees=assignee_ids, limit=10, skip=0)
        response = client.get_tasks(request)

        print(f"Response type: {response.type}")
        print(f"Tasks for assignees {assignee_ids}: {len(response.payload.tasks)}")

        for i, task in enumerate(response.payload.tasks[:3], 1):  # Show first 3 tasks
            print(f"\nTask {i}:")
            print(f"  ID: {task.id}")
            print(f"  Name: {task.name}")
            print(f"  HRID: {task.hrid}")
            print(f"  Completed: {task.completed}")
            print(f"  Assignees: {task.assignees}")
            print(f"  Created: {task.created_at}")

    except Exception as e:
        print(f"Error getting tasks by assignees: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 3: Pagination example - get second page
    print("3. Getting tasks with pagination (second page)...")
    try:
        request = GetTasksRequest(
            limit=5,  # Small limit for demo
            skip=5,  # Skip first 5 tasks
        )
        response = client.get_tasks(request)

        print(f"Response type: {response.type}")
        print(f"Tasks on second page (skip=5, limit=5): {len(response.payload.tasks)}")

        for i, task in enumerate(response.payload.tasks, 6):  # Start numbering from 6
            print(f"\nTask {i}:")
            print(f"  Name: {task.name}")
            print(f"  HRID: {task.hrid}")
            print(f"  Completed: {task.completed}")

    except Exception as e:
        print(f"Error getting paginated tasks: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 4: Get tasks filtered by completion status
    print("4. Getting completed tasks only...")
    try:
        request = GetTasksRequest(completed=True, limit=20)
        response = client.get_tasks(request)

        print(f"Response type: {response.type}")
        print(f"Completed tasks returned: {len(response.payload.tasks)}")

        for i, task in enumerate(response.payload.tasks[:3], 1):
            print(f"\nCompleted Task {i}:")
            print(f"  Name: {task.name}")
            print(f"  HRID: {task.hrid}")
            print(f"  Completed at: {task.completed_at}")

    except Exception as e:
        print(f"Error getting completed tasks: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 5: Get tasks filtered by board and project
    print("5. Getting tasks filtered by board and project...")
    try:
        # Replace with actual IDs from your space
        board_id = "68c19e08020b3f8c50a814d6"  # Example from the API response
        project_id = "68c19e08020b3f8c50a814ce"  # Example from the API response

        request = GetTasksRequest(
            board=board_id,
            project=project_id,
            limit=15,
            archived=False,  # Exclude archived tasks
        )
        response = client.get_tasks(request)

        print(f"Response type: {response.type}")
        print(
            f"Tasks in board {board_id} and project {project_id}: {len(response.payload.tasks)}"
        )

        for i, task in enumerate(response.payload.tasks[:2], 1):
            print(f"\nTask {i}:")
            print(f"  Name: {task.name}")
            print(f"  Board: {task.board}")
            print(f"  Project: {task.project}")
            print(f"  Archived: {task.archived_at is not None}")

    except Exception as e:
        print(f"Error getting tasks by board and project: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 6: Get tasks by specific IDs
    print("6. Getting tasks by specific IDs...")
    try:
        # Replace with actual task IDs from your space
        task_ids = [
            "68c19e08020b3f8c50a8150e",
            "68c19e09020b3f8c50a81663",
        ]  # Examples from the API response

        request = GetTasksRequest(ids=task_ids)
        response = client.get_tasks(request)

        print(f"Response type: {response.type}")
        print(f"Tasks by IDs: {len(response.payload.tasks)}")

        for task in response.payload.tasks:
            print(f"\nTask ID {task.id}:")
            print(f"  Name: {task.name}")
            print(f"  HRID: {task.hrid}")
            print(f"  Status: {'Completed' if task.completed else 'Pending'}")

    except Exception as e:
        print(f"Error getting tasks by IDs: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 7: Get subtasks of a parent task
    print("7. Getting subtasks of a parent task...")
    try:
        # Replace with actual parent task ID from your space
        parent_task_id = "68c19e09020b3f8c50a81663"  # Example from the API response

        request = GetTasksRequest(parent_task=parent_task_id, limit=10)
        response = client.get_tasks(request)

        print(f"Response type: {response.type}")
        print(f"Subtasks of parent {parent_task_id}: {len(response.payload.tasks)}")

        for task in response.payload.tasks:
            print("\nSubtask:")
            print(f"  Name: {task.name}")
            print(f"  HRID: {task.hrid}")
            print(f"  Parent Task: {task.parent_task}")

    except Exception as e:
        print(f"Error getting subtasks: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 8: Get tasks with pagination for large datasets
    print("8. Getting tasks with pagination for large datasets...")
    try:
        # Since max limit is 50, we need to paginate for more tasks
        all_tasks = []
        page = 0
        max_pages = 3  # Get up to 150 tasks (3 pages * 50 tasks)
        
        while page < max_pages:
            request = GetTasksRequest(
                limit=50,  # Maximum allowed limit
                skip=page * 50
            )
            response = client.get_tasks(request)
            
            tasks = response.payload.tasks
            if not tasks:
                break  # No more tasks
            
            all_tasks.extend(tasks)
            page += 1
            
            if len(tasks) < 50:
                break  # Last page had fewer than 50 tasks

        print(f"Response type: {response.type}")
        print(f"Total pages fetched: {page}")
        print(f"Total tasks collected: {len(all_tasks)}")

        # Show some statistics
        completed_tasks = sum(1 for task in all_tasks if task.completed)
        pending_tasks = len(all_tasks) - completed_tasks

        print(f"Completed tasks: {completed_tasks}")
        print(f"Pending tasks: {pending_tasks}")

        # Show tasks by priority
        priority_counts = {}
        for task in all_tasks:
            priority = task.priority
            priority_counts[priority] = priority_counts.get(priority, 0) + 1

        print("\nTasks by priority:")
        for priority, count in priority_counts.items():
            print(f"  Priority {priority}: {count} tasks")

    except Exception as e:
        print(f"Error getting paginated tasks: {e}")


if __name__ == "__main__":
    main()
