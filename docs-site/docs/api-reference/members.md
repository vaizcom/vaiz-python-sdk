---
sidebar_position: 10
sidebar_label: Members
title: Members API — Retrieve Team Members & User Info | Vaiz Python SDK
description: Learn how to use the Vaiz Python SDK to retrieve space members, user information, and team details. Complete API reference with examples.
---

# Members

Complete reference for member-related methods.

## Methods

### `get_space_members`

```python
get_space_members() -> GetSpaceMembersResponse
```

Get all members in the current space.

**Returns:** `GetSpaceMembersResponse` with list of members

**Example:**
```python
# Get all space members
response = client.get_space_members()

print(f"Total members: {len(response.members)}")
for member in response.members:
    print(f"- {member.full_name} ({member.email})")
```

---

### `get_members`

```python
get_members(member_ids: List[str]) -> GetMembersResponse
```

Get members by their IDs. Useful for resolving member IDs from tasks (assignees, creator), comments or history into names and emails.

**Parameters:**
- `member_ids` - List of member IDs. Invalid or unknown IDs are skipped.

**Returns:** `GetMembersResponse` with the found members

**Example:**
```python
response = client.get_members(["member_id_1", "member_id_2"])

for member in response.members:
    print(f"- {member.full_name} ({member.email})")
```

---

## Models

### Member

Main member model representing a space member.

```python
class Member:
    id: str                    # Member ID
    nick_name: Optional[str]   # Nickname
    full_name: Optional[str]   # Full name
    email: str                 # Email address
    avatar: Optional[str]      # Avatar URL
    avatar_mode: AvatarMode    # Avatar display mode (Uploaded=0, Generated=2)
    color: ColorInfo           # Color configuration
    position: Optional[str]    # Position / job title
    bio: Optional[str]         # Bio
    phone_number: Optional[str]  # Phone number
    invited_by: Optional[str]  # Member ID of the inviter
    space: Optional[str]       # Space ID (absent for global bot members)
    status: str                # Member status (e.g., "Active")
    joined_date: str           # Join date as string
    updated_at: str            # Last update date as string
    kind: Optional[str]        # Bot kind (e.g. "AiBot"); None for regular members
```

Name, nickname, email, avatar and color are stored on the member, so they are specific to the space.

---

### ColorInfo

Color configuration shared across spaces, members, and profiles.

```python
class ColorInfo:
    color: str        # Hex color code (e.g., "#a8f8b8")
    is_dark: bool     # Brightness flag - True if color is dark (for UI text contrast)
```

---

## Response Models

### GetSpaceMembersResponse

Response containing list of space members.

```python
class GetSpaceMembersResponse:
    type: str                       # Response type ("GetSpaceMembers")
    payload: GetSpaceMembersPayload # Response payload
    
    @property
    def members(self) -> List[Member]:  # Convenience property to access members
        ...
```

---

### GetSpaceMembersPayload

Payload wrapper for members list.

```python
class GetSpaceMembersPayload:
    members: List[Member]      # List of space members
```

---

### GetMembersResponse

Response containing the requested members.

```python
class GetMembersResponse:
    type: str                  # Response type ("GetMembers")
    payload: GetMembersPayload # Response payload
    
    @property
    def members(self) -> List[Member]:  # Convenience property to access members
        ...
```

---

### GetMembersPayload

```python
class GetMembersPayload:
    members: List[Member]      # Requested members
```

---

## Request Models

### GetMembersRequest

Request model used by `get_members()`. You normally pass IDs directly to `get_members()`.

```python
class GetMembersRequest:
    member_ids: List[str]      # Member IDs (sent as "memberIds")
```

---

## See Also

- [Members Guide](../guides/members) - Usage examples and patterns
- [Profile API](./profile) - Current user profile
- [Spaces API](./spaces) - Space information
- [Enums](./enums) - AvatarMode enum

