---
sidebar_position: 11
title: Enums — Task Priority, Avatar Mode & More | Vaiz Python SDK
description: Complete reference for all enum types and values in the Vaiz Python SDK. Includes TaskPriority, AvatarMode, and other enumeration types.
---

# Enums

Complete reference for all enum types and values.

## TaskPriority

Task priority levels:

```python
from vaiz.models import TaskPriority

TaskPriority.Low       # 0 - Low priority
TaskPriority.General   # 1 - General (default)
TaskPriority.Medium    # 2 - Medium
TaskPriority.High      # 3 - High
```

---

## UploadFileType

File type identifiers for uploads:

```python
from vaiz.models.enums import UploadFileType

UploadFileType.Image    # Image files (shows preview)
UploadFileType.Video    # Video files (shows player)
UploadFileType.Pdf      # PDF files (shows viewer)
UploadFileType.File     # Generic files (download link)
```

---

## AvatarMode

Avatar display modes for spaces and profiles:

```python
from vaiz.models.enums import AvatarMode

AvatarMode.Uploaded = 0    # Custom uploaded avatar image
AvatarMode.Generated = 2   # Auto-generated avatar
```

**Usage:**

```python
# Check space avatar mode
space = client.get_space(space_id).space

if space.avatar_mode == AvatarMode.Uploaded:
    print(f"Custom avatar: {space.avatar}")
elif space.avatar_mode == AvatarMode.Generated:
    print("Generated avatar")
```

---

## CommentReactionType

Popular emoji reactions for comments:

```python
from vaiz.models.enums import CommentReactionType

CommentReactionType.THUMBS_UP    # 👍
CommentReactionType.HEART        # ❤️
CommentReactionType.LAUGHING     # 😂
CommentReactionType.WOW          # 😮
CommentReactionType.CRYING       # 😢
CommentReactionType.ANGRY        # 😡
CommentReactionType.PARTY        # 🎉
```

---

## Kind

Entity types for history and documents:

```python
from vaiz.models.enums import Kind

# Entity types
Kind.Space       # Space documents
Kind.Member      # Personal member documents
Kind.Project     # Project documents
Kind.Task        # Tasks
Kind.Board       # Boards
Kind.Document    # Documents
Kind.Milestone   # Milestones
```

---

## CustomFieldType

All custom field types:

```python
from vaiz.models.enums import CustomFieldType

CustomFieldType.TEXT            # Text input field
CustomFieldType.NUMBER          # Number input field
CustomFieldType.CHECKBOX        # Checkbox field
CustomFieldType.DATE            # Date picker field
CustomFieldType.MEMBER          # User selector field
CustomFieldType.TASK_RELATIONS  # Task relations field
CustomFieldType.SELECT          # Dropdown select field
CustomFieldType.URL             # URL input field
CustomFieldType.ESTIMATION      # Time estimation field
```

---

## Icon

All available icons (200+ options):

```python
from vaiz.models.enums import Icon

# Shapes
Icon.Cursor, Icon.Square, Icon.Hexagon, Icon.Rhombus, Icon.Triangle
Icon.Checkbox, Icon.Diamonds, Icon.Circle

# UI & Interface
Icon.Light, Icon.Search, Icon.Stop, Icon.User, Icon.People
Icon.UserGroup2, Icon.ConnectedPeople, Icon.Col, Icon.Code, Icon.Todo
Icon.Board, Icon.Document, Icon.Project

# Science & Tech
Icon.Air, Icon.Atom, Icon.Molecule, Icon.Battery, Icon.BatteryCharging
Icon.BatteryLevel, Icon.BenzeneRing, Icon.BGRemover

# Objects & Items
Icon.Barcode, Icon.QR, Icon.Basilica, Icon.Basketball, Icon.Binoculars
Icon.BlackHat, Icon.Hat, Icon.Bot, Icon.Broom, Icon.CampingChair
Icon.Cable, Icon.Terminal, Icon.Rs232Female, Icon.CD

# Music & Media
Icon.Music, Icon.Music2, Icon.MusicPlaylist, Icon.Video, Icon.Play
Icon.Camera, Icon.Camera2, Icon.Aperture, Icon.Image

# Time & Actions
Icon.Clock, Icon.Watch, Icon.Tenses, Icon.Voicemail, Icon.WatchesFrontView
Icon.WeddingRings, Icon.List, Icon.Restart, Icon.Swap, Icon.Target

# Weather & Nature
Icon.Moon, Icon.Sun, Icon.Cloud, Icon.Snow, Icon.Fire, Icon.Drop

# Medical & Health
Icon.DoctorsBag, Icon.Hospital, Icon.MedicalDoctor

# Work & Education
Icon.ELearning, Icon.Laptop, Icon.FanSpeed, Icon.MindMap, Icon.Mirror
Icon.Attach, Icon.Table, Icon.Chart, Icon.Broadcast

# Achievement & Status
Icon.Flag, Icon.Finish, Icon.Crown, Icon.Money, Icon.Coins
Icon.Shield, Icon.Trophy, Icon.Star

# Characters & People
Icon.WomanHead, Icon.Knight

# Animals & Creatures
Icon.Bug, Icon.Bird, Icon.PeacePigeon, Icon.Penguin, Icon.Fish
Icon.Alien, Icon.Panda, Icon.Cat, Icon.Dog, Icon.Unicorn

# Sports & Activities
Icon.Run, Icon.Swimming, Icon.Ball

# Location & Navigation
Icon.Geography, Icon.Planet, Icon.Location, Icon.Navigate

# Vehicles & Transportation
Icon.Stormtrooper, Icon.SpaceFighter, Icon.Submarine, Icon.Plane
Icon.Ship, Icon.ShipWheel, Icon.Lifebuoy, Icon.Launch, Icon.Car
Icon.BikePath, Icon.Cycling, Icon.MotorbikeHelmet, Icon.Road

# Communication & Tech
Icon.GpsSignal, Icon.Radio, Icon.InternetAntenna, Icon.Satellites
Icon.Satellite, Icon.Speed, Icon.Info, Icon.Help, Icon.Quote
Icon.Attention, Icon.Phone, Icon.Email, Icon.Mail, Icon.Message
Icon.Chat, Icon.Sound

# Editing & Content
Icon.Rename, Icon.New, Icon.Add, Icon.Delete, Icon.Type, Icon.Asterisk
Icon.Thumb, Icon.Percent, Icon.Percent25, Icon.Percent50

# Food & Drink
Icon.Coffee, Icon.Beer, Icon.Champagne, Icon.WineGlass, Icon.Cocktail
Icon.Plate

# Misc & Fun
Icon.Heart, Icon.Link, Icon.Happy, Icon.Layers, Icon.Apps, Icon.Up
Icon.Lab, Icon.Cancel, Icon.Poo, Icon.Skull, Icon.Bone, Icon.Dice
Icon.Puzzle, Icon.Bang, Icon.Explosion, Icon.Gun, Icon.Shower
Icon.SpaFlower, Icon.FoamBubbles, Icon.Galaxy, Icon.Bookmark, Icon.Book
Icon.Sent, Icon.Home, Icon.MarkerPen, Icon.Illustrator, Icon.Paint
Icon.Paint2, Icon.Gear, Icon.BoxClose

# Greek Letters
Icon.Alpha, Icon.Beta, Icon.Gamma, Icon.Lambda, Icon.Mu
Icon.Omega, Icon.Pi, Icon.Sigma

# Field Type Icons
Icon.TypeText, Icon.TypeNumber, Icon.TypeDate, Icon.TypeCheck, Icon.TypeUser
```

---

## Color

All available colors:

```python
from vaiz.models.enums import Color

Color.Silver = 'silver'
Color.Red = 'red'
Color.Orange = 'orange'
Color.Gold = 'gold'
Color.Olive = 'olive'
Color.Green = 'green'
Color.Mint = 'mint'
Color.Blue = 'blue'
Color.Violet = 'violet'
Color.Lavender = 'lavender'
Color.Magenta = 'magenta'
Color.Rose = 'rose'
```

---

## Usage Examples

### TaskPriority

```python
from vaiz.models import CreateTaskRequest, TaskPriority

task = CreateTaskRequest(
    name="High Priority Task",
    board="board_id",
    group="group_id",
    priority=TaskPriority.High  # 3
)
```

### Icon & Color

```python
from vaiz.models import CreateBoardTypeRequest
from vaiz.models.enums import Icon, Color

type_request = CreateBoardTypeRequest(
    board_id="board_id",
    label="Bug",
    icon=Icon.Bug,
    color=Color.Red
)
```

### UploadFileType

```python
from vaiz.models.enums import UploadFileType

response = client.upload_file("screenshot.png", UploadFileType.Image)
```

### Kind

```python
from vaiz.models import GetDocumentsRequest
from vaiz.models.enums import Kind

docs = client.get_documents(
    GetDocumentsRequest(
        kind=Kind.Project,
        kind_id="project_id"
    )
)
```

### AvatarMode

```python
from vaiz.models.enums import AvatarMode

space = client.get_space(space_id).space

if space.avatar_mode == AvatarMode.Uploaded:
    print(f"Custom avatar uploaded: {space.avatar}")
elif space.avatar_mode == AvatarMode.Generated:
    print("Generated avatar")
```

