---
sidebar_position: 7
---

# Integration Patterns

Integrate the Vaiz SDK with external systems and services.

## Webhook Handler for Task Updates

Handle external webhooks and update Vaiz tasks:

```python
from flask import Flask, request, jsonify
from vaiz import VaizClient
from vaiz.models import EditTaskRequest
from datetime import datetime

app = Flask(__name__)
client = VaizClient(api_key="...", space_id="...")

@app.route('/webhook/task-update', methods=['POST'])
def handle_task_update():
    """Handle external webhook and update Vaiz task."""
    data = request.json
    
    # Update task based on webhook
    edit = EditTaskRequest(
        task_id=data['task_id'],
        completed=data.get('status') == 'done',
        description=f"Updated via webhook at {datetime.now()}"
    )
    
    response = client.edit_task(edit)
    return jsonify({"success": True, "task": response.task.hrid})

if __name__ == '__main__':
    app.run(port=5000)
```

## GitHub Integration

Sync GitHub issues with Vaiz tasks:

```python
import requests
from vaiz.models import CreateTaskRequest, TaskPriority

def sync_github_issues(repo_owner: str, repo_name: str, github_token: str):
    """Fetch GitHub issues and create corresponding Vaiz tasks."""
    
    # Fetch GitHub issues
    headers = {"Authorization": f"token {github_token}"}
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    response = requests.get(url, headers=headers)
    issues = response.json()
    
    # Create tasks for each issue
    for issue in issues:
        # Skip pull requests
        if 'pull_request' in issue:
            continue
        
        # Map labels to priority
        labels = [label['name'] for label in issue['labels']]
        priority = TaskPriority.High if 'bug' in labels else TaskPriority.General
        
        # Create task
        task = CreateTaskRequest(
            name=f"[#{issue['number']}] {issue['title']}",
            board=board_id,
            group=group_id,
            project=project_id,
            priority=priority,
            description=f"{issue['body']}\n\n[View on GitHub]({issue['html_url']})"
        )
        
        result = client.create_task(task)
        print(f"✅ Created task {result.task.hrid} for issue #{issue['number']}")
```

## Slack Notifications

Send Slack notifications for task updates:

```python
import requests
from vaiz.models import GetTasksRequest

def send_slack_notification(webhook_url: str, message: str):
    """Send message to Slack via webhook."""
    requests.post(webhook_url, json={"text": message})

def notify_overdue_tasks(client, slack_webhook: str):
    """Notify about overdue tasks in Slack."""
    from datetime import datetime
    
    # Get all incomplete tasks
    response = client.get_tasks(
        GetTasksRequest(completed=False, limit=50)
    )
    
    # Find overdue tasks
    today = datetime.now().date()
    overdue = [
        task for task in response.payload.tasks
        if task.due_end and task.due_end.date() < today
    ]
    
    if overdue:
        message = f"⚠️ {len(overdue)} overdue tasks:\n"
        for task in overdue[:5]:  # Show first 5
            days = (today - task.due_end.date()).days
            message += f"• {task.name} (overdue by {days} days)\n"
        
        send_slack_notification(slack_webhook, message)
        print(f"✅ Sent notification about {len(overdue)} overdue tasks")
```

## Jira Sync

Synchronize tasks between Vaiz and Jira:

```python
from jira import JIRA
from vaiz.models import CreateTaskRequest, EditTaskRequest

def sync_with_jira(jira_url: str, jira_token: str):
    """Two-way sync between Vaiz and Jira."""
    
    # Initialize Jira client
    jira = JIRA(server=jira_url, token_auth=jira_token)
    
    # Get Vaiz tasks
    vaiz_tasks = client.get_tasks(
        GetTasksRequest(project=project_id, limit=50)
    ).payload.tasks
    
    # Sync each task
    for task in vaiz_tasks:
        # Check if Jira issue exists (stored in custom field)
        jira_id = task.custom_fields.get('jira_id')
        
        if jira_id:
            # Update existing Jira issue
            jira_issue = jira.issue(jira_id)
            jira_issue.update(
                summary=task.name,
                description=get_task_description(task.document)
            )
        else:
            # Create new Jira issue
            new_issue = jira.create_issue(
                project='PROJECT',
                summary=task.name,
                description=get_task_description(task.document),
                issuetype={'name': 'Task'}
            )
            
            # Store Jira ID in Vaiz task
            # (using custom field - setup required)
            print(f"✅ Created Jira issue {new_issue.key} for {task.hrid}")
```

## See Also

- [Real-World Scenarios](./real-world) - Complete use case examples

