---
sidebar_position: 8
---

# Profile

Complete reference for profile-related methods.

## Methods

### `get_profile`

```python
get_profile() -> ProfileResponse
```

Get current user's profile information.

**Returns:** `ProfileResponse` with user data

---

## Models

### Profile

```python
class Profile:
    id: str                              # User ID
    full_name: Optional[str]             # Full name
    nick_name: Optional[str]             # Nickname
    email: str                           # Primary email
    emails: List[ProfileEmail]           # All email addresses
    color: ProfileColor                  # User color configuration
    avatar: Optional[str]                # Avatar URL
    avatar_mode: AvatarMode              # Avatar display mode
    registered_date: datetime            # Registration timestamp
    member_id: Optional[str]             # Member ID in current space
    is_email_confirmed: Optional[bool]   # Email confirmation status
    incomplete_steps: List[str]          # Onboarding steps not completed
    phone_number: Optional[str]          # Phone number
    password_changed_date: Optional[datetime]  # Last password change
    recovery_codes: List[Dict]           # Account recovery codes
    recovery_codes_viewed_date: Optional[datetime]  # Recovery codes viewed date
    webauthn_credentials: List[Dict]     # WebAuthn credentials
    invited: Optional[bool]              # Invited user flag
    created_at: Optional[datetime]       # Creation timestamp
    updated_at: datetime                 # Last update timestamp
    c_data: Dict[str, Optional[str]]     # Custom data
```

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
    is_dark: Optional[bool]   # Dark theme flag
```

---

### ProfileResponse

```python
class ProfileResponse:
    type: str                   # Response type
    payload: Dict[str, Profile] # Response payload
    
    @property
    def profile(self) -> Profile:  # Convenience property
        ...
```

---

## See Also

- [Profile Guide](../guides/profile) - Usage examples and patterns

