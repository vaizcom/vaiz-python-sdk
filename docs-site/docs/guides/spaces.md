---
sidebar_position: 9
---

# Spaces

Get information about your workspace (space).

## Get Space Information

```python
response = client.get_space(space_id)
space = response.space

print(f"📦 {space.name}")
print(f"   Color: {space.color.color}")
print(f"   Created: {space.created_at}")
```

:::tip Model Definition
See the [Spaces API Reference](../api-reference/spaces) for the complete Space model definition.
:::

## Color Configuration

The space color includes the hex code and a brightness flag for UI contrast:

```python
space_color = space.color
print(f"Color: {space_color.color}")      # e.g., "#98a8e8"
print(f"Is Dark: {space_color.is_dark}")  # True if color is dark

# Use is_dark to determine text color for contrast
text_color = "white" if space_color.is_dark else "black"
print(f"Use {text_color} text on {space_color.color} background")
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

# Get space information
space_id = os.getenv("VAIZ_SPACE_ID")
response = client.get_space(space_id)
space = response.space

print("=== Space Information ===")
print(f"Name: {space.name}")
print(f"ID: {space.id}")
print(f"Color: {space.color.color}")
print(f"Color is dark: {space.color.is_dark}")
print(f"Created: {space.created_at}")
print(f"Plan: {space.plan}")
```

## Use Cases

### Verify Space Access

```python
try:
    response = client.get_space(space_id)
    print(f"✅ Connected to space: {response.space.name}")
except Exception as e:
    print("❌ Cannot access space")
```

### Display Space Info in UI

```python
def get_workspace_info(space_id: str):
    """Get formatted workspace information for UI."""
    response = client.get_space(space_id)
    space = response.space
    
    # Determine text color for contrast
    text_color = "#FFFFFF" if space.color.is_dark else "#000000"
    
    return {
        "name": space.name,
        "background_color": space.color.color,
        "text_color": text_color,
        "avatar": space.avatar,
        "created": space.created_at.strftime("%Y-%m-%d")
    }

# Use in your app
info = get_workspace_info(space_id)
print(f"Workspace: {info['name']}")
print(f"Style: color {info['background_color']} with {info['text_color']} text")
```

### Check Space Details

```python
space = client.get_space(space_id).space

# Get basic info
print(f"Space Name: {space.name}")
print(f"Space ID: {space.id}")

# Check branding
if space.avatar:
    print(f"Logo: {space.avatar}")
print(f"Brand Color: {space.color.color}")

# Check metadata
print(f"Created: {space.created_at}")
print(f"Last Updated: {space.updated_at}")
print(f"Is Foreign: {space.is_foreign}")
```

## Avatar Modes

The `avatar_mode` field indicates how the space avatar is displayed:

```python
from vaiz.models import AvatarMode

space = client.get_space(space_id).space

if space.avatar_mode == AvatarMode.Uploaded:
    print(f"Custom avatar uploaded: {space.avatar}")
elif space.avatar_mode == AvatarMode.Generated:
    print("Generated avatar")
```

See [`AvatarMode`](../api-reference/enums#avatarmode) for available avatar modes.

## See Also

- [Spaces API Reference](../api-reference/spaces) - Technical specifications
- [Projects](./projects) - Project management
- [Profile](./profile) - User profile
- [Ready-to-Run Examples](../patterns/ready-to-run) - More examples

