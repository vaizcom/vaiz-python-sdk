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

## Models & Interfaces

### Space

Represents a space in the system.

```python
class Space:
    id: str                    # Space ID
    name: str                  # Space name
    color: SpaceColor          # Color configuration
    avatar_mode: AvatarMode    # Avatar display mode (Uploaded=0, Generated=2)
    avatar: Optional[str]      # Avatar URL
    creator: str               # Creator ID
    plan: str                  # Plan ID
    created_at: datetime       # Creation timestamp
    updated_at: datetime       # Last update timestamp
    is_foreign: bool           # Whether this is a foreign space
```

### SpaceColor

Color configuration for a space.

```python
class SpaceColor:
    color: str        # Hex color code (e.g., "#98a8e8")
    is_dark: bool     # Whether the color is dark
```

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

## See Also

- [Examples](../patterns/ready-to-run) - Ready-to-run code examples

