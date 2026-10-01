---
sidebar_position: 8
sidebar_label: Profile
title: Working with Profile — Member Info | Vaiz Python SDK
description: Learn how to retrieve the authenticated member's profile in the current space using the Vaiz Python SDK. Get name, email, avatar and member ID.
---

# Profile

Get information about the current authenticated member in the current space.

## Get Profile

```python
response = client.get_profile()
profile = response.profile

print(f"Member: {profile.full_name or profile.nick_name}")
print(f"Email: {profile.email}")
print(f"Member ID: {profile.member_id}")
```

## Profile Information

The profile is **per space**: name, nickname, email, avatar and color belong to your member in the current space, so they can differ between spaces.

The profile includes:

- **Personal Info**: Full name, nickname, email, avatar, position, bio
- **Identity**: Member ID (`member_id`) and user account ID (`user_id`)
- **Membership**: Space, status, join date

Use `member_id` wherever the API expects a member — assignees, mentions, Member documents.

:::tip Model Definition
See the [Profile API Reference](../api-reference/profile) for the complete Profile model definition.
:::

## Edit Profile

Update your profile in the current space. Only the fields you pass are changed, and other spaces are not affected:

```python
from vaiz import EditProfileRequest

response = client.edit_profile(EditProfileRequest(
    position="Backend Developer",
    bio="Working on the API",
))

print(f"Position: {response.profile.position}")
```

You can also change `full_name`, `nick_name` and `phone_number`. If you use a generated avatar, changing the name regenerates it with the new initials.

## Example: Check Current Member

```python
def get_current_member():
    """Get current authenticated member info"""
    profile = client.get_profile().profile
    
    return {
        "member_id": profile.member_id,
        "name": profile.full_name or profile.nick_name or "Unknown",
        "email": profile.email,
        "joined": profile.joined_date,
    }

me = get_current_member()
print(f"Logged in as: {me['name']} ({me['email']})")
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

### Assign Tasks to Yourself

```python
from vaiz.models import EditTaskRequest

my_member_id = client.get_profile().profile.member_id

edit = EditTaskRequest(
    task_id="task_id",
    assignees=[my_member_id]
)
client.edit_task(edit)
```

### Display Profile Info

```python
profile = client.get_profile().profile

print("👤 Profile")
print(f"Full Name: {profile.full_name or 'N/A'}")
print(f"Nickname: {profile.nick_name or 'N/A'}")
print(f"Email: {profile.email}")
print(f"Position: {profile.position or 'N/A'}")
print(f"Joined: {profile.joined_date}")
print(f"Avatar: {profile.avatar or 'No avatar'}")
```

## See Also

- [Tasks API](./tasks) - Assign tasks to members
- [History](./history) - Track member activity
