---
sidebar_position: 5
---

# Real-World Scenarios

Complete examples for common real-world use cases.

## Automated Task Creation from Issues

Convert GitHub issues to Vaiz tasks:

```python
def create_task_from_github_issue(issue_data: dict):
    """Convert GitHub issue to Vaiz task."""
    from vaiz.models import CreateTaskRequest, TaskPriority
    
    # Map priority
    priority_map = {
        "critical": TaskPriority.High,
        "high": TaskPriority.High,
        "medium": TaskPriority.Medium,
        "low": TaskPriority.Low
    }
    
    priority = priority_map.get(
        issue_data.get("priority", "medium"),
        TaskPriority.General
    )
    
    # Create task
    task = CreateTaskRequest(
        name=issue_data["title"],
        board=board_id,
        group=group_id,
        project=project_id,
        priority=priority,
        description=f"""
# GitHub Issue #{issue_data['number']}

**Author**: {issue_data['author']}
**URL**: {issue_data['url']}

## Description
{issue_data['body']}
"""
    )
    
    response = client.create_task(task)
    return response.task

# Usage
task = create_task_from_github_issue({
    "number": 123,
    "title": "Fix login bug",
    "author": "john_doe",
    "url": "https://github.com/org/repo/issues/123",
    "body": "Users can't login with email",
    "priority": "high"
})
```

## Daily Standup Report Generator

Generate daily standup reports for team members:

```python
from vaiz.models import GetTasksRequest
from datetime import datetime, timedelta

def generate_standup_report(client, user_id: str):
    """Generate daily standup report for a user."""
    
    # Get user's tasks
    response = client.get_tasks(
        GetTasksRequest(
            assignees=[user_id],
            completed=False
        )
    )
    
    # Categorize by due date
    today = datetime.now().date()
    overdue = []
    due_today = []
    upcoming = []
    
    for task in response.payload.tasks:
        if task.due_end:
            due_date = task.due_end.date()
            if due_date < today:
                overdue.append(task)
            elif due_date == today:
                due_today.append(task)
            else:
                upcoming.append(task)
    
    # Generate report
    report = f"""
# Standup Report - {today.strftime("%Y-%m-%d")}

## 🔴 Overdue ({len(overdue)})
{chr(10).join(f"- {t.name} (due: {t.due_end.strftime('%Y-%m-%d')})" for t in overdue)}

## ⚡ Due Today ({len(due_today)})
{chr(10).join(f"- {t.name}" for t in due_today)}

## 📋 Upcoming ({len(upcoming[:5])})
{chr(10).join(f"- {t.name} (due: {t.due_end.strftime('%Y-%m-%d')})" for t in upcoming[:5])}
"""
    
    return report

# Usage
report = generate_standup_report(client, user_id)
print(report)
```

## Sync Tasks with External System

Synchronize task statuses to external tracking systems:

```python
from vaiz.models import GetTasksRequest, EditTaskRequest

def sync_task_status_to_external(client, project_id: str):
    """Sync task statuses to external tracking system."""
    
    # Get all tasks
    tasks = client.get_tasks(
        GetTasksRequest(project=project_id, limit=50)
    ).payload.tasks
    
    # Prepare batch update for external system
    updates = []
    for task in tasks:
        updates.append({
            'external_id': task.hrid,
            'status': 'completed' if task.completed else 'active',
            'assignees': task.assignees,
            'updated_at': task.updated_at.isoformat()
        })
    
    # Send to external system (pseudocode)
    # external_api.batch_update(updates)
    
    print(f"✅ Synced {len(updates)} tasks")
```

