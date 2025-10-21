---
sidebar_position: 10
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

## Models & Interfaces

### Member

Represents a member in the space.

```python
class Member:
    id: str                    # Member ID
    nick_name: Optional[str]   # Nickname
    full_name: Optional[str]   # Full name
    email: str                 # Email address
    avatar: Optional[str]      # Avatar URL
    avatar_mode: AvatarMode    # Avatar display mode (Uploaded=0, Generated=2)
    color: MemberColor         # Color configuration
    space: str                 # Space ID
    status: str                # Member status (e.g., "Active")
    joined_date: str           # Join date as string
    updated_at: str            # Last update date as string
```

### MemberColor

Color configuration for a member.

```python
class MemberColor:
    color: str        # Hex color code (e.g., "#a8f8b8")
    is_dark: bool     # Whether the color is dark
```

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

## See Also

- [Members Guide](../guides/members) - Usage examples and patterns
- [Profile API](./profile) - Current user profile
- [Spaces API](./spaces) - Space information

