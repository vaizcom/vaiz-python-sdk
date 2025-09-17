#!/usr/bin/env python3
"""
Example: Get All Tasks with Automatic Pagination

This example demonstrates how to use the get_all_tasks helper method
that automatically handles pagination to fetch large numbers of tasks.
"""

from vaiz.models import GetTasksRequest
from examples.config import get_client


def main():
    """Demonstrate automatic pagination with get_all_tasks helper."""
    client = get_client()

    print("=== Get All Tasks with Automatic Pagination ===\n")

    # Example 1: Get all tasks (up to default limit of 500)
    print("1. Getting all tasks with default limit...")
    try:
        all_tasks = client.get_all_tasks()
        print(f"Total tasks fetched: {len(all_tasks)}")

        # Show statistics
        completed = sum(1 for task in all_tasks if task.completed)
        pending = len(all_tasks) - completed

        print(f"  Completed: {completed}")
        print(f"  Pending: {pending}")

    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 2: Get all completed tasks with custom limit
    print("2. Getting all completed tasks (max 200)...")
    try:
        request = GetTasksRequest(completed=True)
        completed_tasks = client.get_all_tasks(request, max_tasks=200)

        print(f"Completed tasks fetched: {len(completed_tasks)}")

        if completed_tasks:
            print("\nFirst 3 completed tasks:")
            for i, task in enumerate(completed_tasks[:3], 1):
                print(f"  {i}. {task.name} (HRID: {task.hrid})")

    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 3: Get all tasks for specific board
    print("3. Getting all tasks for a specific board...")
    try:
        board_id = "68c19e08020b3f8c50a814d6"  # Replace with your board ID
        request = GetTasksRequest(board=board_id)
        board_tasks = client.get_all_tasks(request, max_tasks=150)

        print(f"Tasks in board {board_id}: {len(board_tasks)}")

        # Group by project
        projects = {}
        for task in board_tasks:
            project = task.project
            if project not in projects:
                projects[project] = []
            projects[project].append(task)

        print(f"Tasks grouped by {len(projects)} projects:")
        for project_id, tasks in projects.items():
            print(f"  Project {project_id}: {len(tasks)} tasks")

    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 4: Get all pending tasks with assignees
    print("4. Getting all pending tasks with specific assignees...")
    try:
        assignee_ids = ["68c19e08020b3f8c50a814c1"]  # Replace with actual IDs
        request = GetTasksRequest(
            assignees=assignee_ids, completed=False, archived=False
        )
        pending_assigned_tasks = client.get_all_tasks(request, max_tasks=100)

        print(f"Pending tasks for assignees: {len(pending_assigned_tasks)}")

        # Show priority distribution
        priority_counts = {}
        for task in pending_assigned_tasks:
            priority = task.priority
            priority_counts[priority] = priority_counts.get(priority, 0) + 1

        print("\nPriority distribution:")
        for priority, count in sorted(priority_counts.items()):
            print(f"  Priority {priority}: {count} tasks")

    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 5: Demonstrate the safety limit
    print("5. Testing safety limit (max 10000 tasks)...")
    try:
        # This will raise an error
        client.get_all_tasks(max_tasks=15000)
    except ValueError as e:
        print(f"✅ Safety check working: {e}")

    print("\n" + "=" * 50 + "\n")

    # Example 6: Manual pagination vs automatic
    print("6. Comparison: Manual vs Automatic Pagination")

    # Manual pagination
    print("\nManual pagination (traditional way):")
    manual_tasks = []
    page = 0
    while True:
        request = GetTasksRequest(limit=50, skip=page * 50)
        response = client.get_tasks(request)
        tasks = response.payload.tasks

        if not tasks:
            break

        manual_tasks.extend(tasks)
        page += 1

        if page >= 3:  # Limit to 3 pages for demo
            break

    print(f"  Fetched {len(manual_tasks)} tasks in {page} pages")

    # Automatic pagination
    print("\nAutomatic pagination (using helper):")
    auto_tasks = client.get_all_tasks(max_tasks=150)
    print(f"  Fetched {len(auto_tasks)} tasks automatically")

    print("\n✅ The helper method handles all pagination complexity for you!")


if __name__ == "__main__":
    main()
