---
sidebar_position: 8
sidebar_label: Profile
title: Profile API — Get Current User Profile | Vaiz Python SDK
description: Learn how to use the Vaiz Python SDK to retrieve the authenticated user's profile information, including name, email, and avatar settings.
---

# Profile

Complete reference for profile-related methods.

## Methods

### `get_profile`

```python
get_profile() -> ProfileResponse
```

Get the current member's profile in the current space.

**Returns:** `ProfileResponse` with member profile data

---

### `edit_profile`

```python
edit_profile(request: EditProfileRequest) -> ProfileResponse
```

Edit the current member's profile in the current space. Only the provided fields are updated; the change does not affect your profile in other spaces.

If the member uses a generated avatar, changing `full_name` or `nick_name` regenerates it with the new initials.

**Parameters:**
- `request` - [`EditProfileRequest`](#editprofilerequest) with fields to update

**Returns:** `ProfileResponse` with the updated profile

**Example:**
```python
from vaiz import EditProfileRequest

response = client.edit_profile(EditProfileRequest(
    position="Backend Developer",
    bio="Working on the API",
))
print(response.profile.position)
```

---

## Models

### Profile

Profile of the current member in the current space. Name, nickname, email, avatar and color are stored per space, so the same user can have different profiles in different spaces.

```python
class Profile:
    id: str                              # Member ID (raw `_id` from the API)
    member_id: str                       # Member ID in current space — use for assignees, mentions, Member documents
    user_id: Optional[str]               # ID of the underlying user account
    space: Optional[str]                 # Space ID
    status: Optional[str]                # Member status (e.g. "Active")
    full_name: Optional[str]             # Full name
    nick_name: Optional[str]             # Nickname
    email: str                           # Email in this space
    color: ProfileColor                  # Color configuration
    avatar: Optional[str]                # Avatar URL
    avatar_mode: AvatarMode              # Avatar display mode
    position: Optional[str]              # Position / job title
    bio: Optional[str]                   # Bio
    phone_number: Optional[str]          # Phone number
    joined_date: Optional[datetime]      # Date the member joined the space
    invited_by: Optional[str]            # Member ID of the inviter
    kind: Optional[str]                  # Bot kind; None for regular members
    created_at: Optional[datetime]       # Creation timestamp
    updated_at: datetime                 # Last update timestamp
```

:::note Legacy fields
Before Release 100 the profile was user-based: `id` was the user ID and account fields (`emails`, `registered_date`, `incomplete_steps`, `recovery_codes`, `webauthn_credentials`, etc.) were returned. These fields remain on the model as optional for older API versions, but are empty on current API versions. `member_id` and `user_id` are resolved correctly for both versions.
:::

---

### ProfileEmail

```python
class ProfileEmail:
    email: str         # Email address
    confirmed: bool    # Confirmation status
    primary: bool      # Primary email flag
```

---

### ProfileColor

```python
class ProfileColor:
    color: Optional[str]      # Color hex code (e.g., "#a8f8b8")
    is_dark: Optional[bool]   # Brightness flag - True if color is dark (for UI text contrast)
```

---

## Request Models

### EditProfileRequest

```python
class EditProfileRequest:
    full_name: Optional[str]      # Full name (must not be blank)
    nick_name: Optional[str]      # Nickname (letters and digits only)
    position: Optional[str]       # Position / job title
    bio: Optional[str]            # Bio
    phone_number: Optional[str]   # Phone number
```

Fields left as `None` are not sent and stay unchanged. Pass an empty string to clear `position`, `bio` or `phone_number`.

---

## Response Models

### ProfileResponse

```python
class ProfileResponse:
    type: str                   # Response type ("GetProfile" or "EditProfile")
    payload: Dict[str, Profile] # Response payload
    
    @property
    def profile(self) -> Profile:  # Convenience property
        ...
```

---

## See Also

- [Profile Guide](../guides/profile) - Usage examples and patterns

