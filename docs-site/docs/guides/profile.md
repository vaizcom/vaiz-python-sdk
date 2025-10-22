---
sidebar_position: 8
---

# Profile

Get information about the current authenticated user.

## Get User Profile

```python
response = client.get_profile()
profile = response.profile

print(f"User: {profile.full_name or profile.nick_name}")
print(f"Email: {profile.email}")
print(f"ID: {profile.id}")
```

## Profile Information

The profile includes:

- **Personal Info**: Full name, nickname, email, avatar
- **Account Details**: User ID, registration date
- **Security**: Recovery codes, password changes
- **Status**: Email confirmation, incomplete onboarding steps

:::tip Model Definition
See the [Profile API Reference](../api-reference/profile) for the complete Profile model definition.
:::

## Example: Check Current User

```python
def get_current_user():
    """Get current authenticated user info"""
    response = client.get_profile()
    profile = response.profile
    
    return {
        "id": profile.id,
        "name": profile.full_name or profile.nick_name or "Unknown",
        "email": profile.email,
        "registered": profile.registered_date
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
profile_response = client.get_profile()
my_id = profile_response.profile.id

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
profile = profile_response.profile

print("👤 User Profile")
print(f"Full Name: {profile.full_name or 'N/A'}")
print(f"Nickname: {profile.nick_name or 'N/A'}")
print(f"Email: {profile.email}")
print(f"Registered: {profile.registered_date}")
print(f"Avatar: {profile.avatar or 'No avatar'}")
print(f"Email Confirmed: {profile.is_email_confirmed}")
```

## See Also

- [Tasks API](./tasks) - Assign tasks to users
- [History](./history) - Track user activity

