---
sidebar_position: 8
---

# Profile

Get information about the current authenticated user.

## Get User Profile

```python
response = client.get_profile()
profile = response.payload["profile"]

print(f"User: {profile['name']}")
print(f"Email: {profile['email']}")
print(f"ID: {profile['_id']}")
```

## Profile Information

The profile includes:

- **Personal Info**: Name, email, avatar
- **Account Details**: User ID, registration date
- **Workspace**: Current space information
- **Preferences**: User settings

## Example: Check Current User

```python
def get_current_user():
    """Get current authenticated user info"""
    response = client.get_profile()
    profile = response.payload["profile"]
    
    return {
        "id": profile["_id"],
        "name": profile.get("name", "Unknown"),
        "email": profile.get("email", ""),
        "registered": profile.get("registeredDate")
    }

user = get_current_user()
print(f"Logged in as: {user['name']} ({user['email']})")
```

## Use Cases

### Verify Authentication

```python
try:
    response = client.get_profile()
    print("✅ Authenticated")
except Exception as e:
    print("❌ Authentication failed")
```

### Get User ID for Assignments

```python
# Get current user ID
profile = client.get_profile()
my_id = profile.payload["profile"]["_id"]

# Assign tasks to yourself
from vaiz.models import EditTaskRequest

edit = EditTaskRequest(
    task_id="task_id",
    assignees=[my_id]
)
client.edit_task(edit)
```

### Display User Info

```python
profile_response = client.get_profile()
profile = profile_response.payload["profile"]

print("👤 User Profile")
print(f"Name: {profile.get('name', 'N/A')}")
print(f"Email: {profile.get('email', 'N/A')}")
print(f"Registered: {profile.get('registeredDate', 'N/A')}")
```

## See Also

- [Tasks API](./tasks) - Assign tasks to users
- [History](./history) - Track user activity

