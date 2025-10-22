---
sidebar_position: 11
---

# Spaces

Complete reference for space-related methods.

## Methods

### `get_space`

```python
get_space(space_id: str) -> GetSpaceResponse
```

Get information about a specific space.

**Parameters:**
- `space_id` - The ID of the space to retrieve

**Returns:** `GetSpaceResponse` with space information

**Example:**
```python
# Get space information
response = client.get_space("68f78b1bf0066408bf9befa8")
space = response.space

print(f"Space: {space.name}")
print(f"Color: {space.color.color}")
print(f"Created: {space.created_at}")
```

---

## Models

### Space

Main space model representing a workspace in the system.

```python
class Space:
    id: str                    # Space ID
    name: str                  # Space name
    color: ColorInfo           # Color configuration
    avatar_mode: AvatarMode    # Avatar display mode (Uploaded=0, Generated=2)
    avatar: Optional[str]      # Avatar URL
    creator: str               # Creator ID
    plan: str                  # Plan ID
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last update timestamp
    is_foreign: bool           # Whether this is a foreign space
```

---

### ColorInfo

Color configuration shared across spaces, members, and profiles.

```python
class ColorInfo:
    color: str        # Hex color code (e.g., "#98a8e8")
    is_dark: bool     # Brightness flag - True if color is dark (for UI text contrast)
```

---

## Response Models

### GetSpaceResponse

Response containing space information.

```python
class GetSpaceResponse:
    type: str                  # Response type ("GetSpace")
    payload: GetSpacePayload   # Response payload
    
    @property
    def space(self) -> Space:  # Convenience property to access space
        ...
```

---

### GetSpacePayload

Payload wrapper for space data.

```python
class GetSpacePayload:
    space: Space               # Space object
```

---

## See Also

- [Spaces Guide](../guides/spaces) - Usage examples and patterns
- [Members API](./members) - Space members
- [Enums](./enums) - AvatarMode enum

