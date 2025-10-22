---
sidebar_position: 10
---

# Members

Get information about members in your space.

## Get Space Members

```python
response = client.get_space_members()

for member in response.members:
    print(f"👤 {member.full_name}")
    print(f"   Email: {member.email}")
    print(f"   Status: {member.status}")
```

:::tip Model Definition
See the [Members API Reference](../api-reference/members) for the complete Member model definition.
:::

## Color Configuration

The member color includes both the color code and theme:

```python
member_color = member.color
print(f"Color: {member_color.color}")      # e.g., "#a8f8b8"
print(f"Is Dark: {member_color.is_dark}")  # True/False
```

## Complete Example

```python
from vaiz import VaizClient
import os

# Initialize client
client = VaizClient(
    api_key=os.getenv("VAIZ_API_KEY"),
    space_id=os.getenv("VAIZ_SPACE_ID")
)

# Get all space members
response = client.get_space_members()

print(f"Total members: {len(response.members)}")
print()

for member in response.members:
    print(f"👤 {member.full_name or member.nick_name}")
    print(f"   Email: {member.email}")
    print(f"   Status: {member.status}")
    print(f"   Joined: {member.joined_date}")
    print()
```

## Use Cases

### List All Team Members

```python
def list_team_members():
    """Get list of all team members."""
    response = client.get_space_members()
    
    members = []
    for member in response.members:
        members.append({
            "id": member.id,
            "name": member.full_name or member.nick_name,
            "email": member.email,
            "status": member.status
        })
    
    return members

team = list_team_members()
print(f"Team size: {len(team)}")
```

### Filter Active Members

```python
response = client.get_space_members()

active_members = [
    member for member in response.members
    if member.status == "Active"
]

print(f"Active members: {len(active_members)}")
for member in active_members:
    print(f"  - {member.email}")
```

### Get Member by Email

```python
def find_member_by_email(email: str):
    """Find a member by email address."""
    response = client.get_space_members()
    
    for member in response.members:
        if member.email == email:
            return member
    
    return None

member = find_member_by_email("user@example.com")
if member:
    print(f"Found: {member.full_name} (ID: {member.id})")
else:
    print("Member not found")
```

### Display Member Info

```python
response = client.get_space_members()

for member in response.members:
    print(f"👤 Member: {member.full_name or member.nick_name}")
    print(f"   ID: {member.id}")
    print(f"   Email: {member.email}")
    print(f"   Status: {member.status}")
    print(f"   Color: {member.color.color}")
    
    if member.avatar:
        print(f"   Avatar: {member.avatar}")
    
    print(f"   Joined: {member.joined_date}")
    print()
```

### Check Member Avatar Mode

```python
from vaiz.models import AvatarMode

response = client.get_space_members()

for member in response.members:
    if member.avatar_mode == AvatarMode.Uploaded:
        print(f"{member.email}: Custom avatar")
    elif member.avatar_mode == AvatarMode.Generated:
        print(f"{member.email}: Generated avatar")
```

## See Also

- [Members API Reference](../api-reference/members) - Technical specifications
- [Profile](./profile) - Current user profile
- [Spaces](./spaces) - Space information
- [Ready-to-Run Examples](../patterns/ready-to-run) - More examples

