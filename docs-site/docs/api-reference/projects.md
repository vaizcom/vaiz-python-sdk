---
sidebar_position: 7
sidebar_label: Projects
title: Projects API — Manage Projects & Lists | Vaiz Python SDK
description: Learn how to use the Vaiz Python SDK to retrieve projects, lists, and organize your workspace structure. Complete API reference with examples.
---

# Projects

Complete reference for project-related methods.

## Methods

### `get_projects`

```python
get_projects() -> ProjectsResponse
```

Get all projects in current space.

**Returns:** `ProjectsResponse` with list of projects

---

### `get_project`

```python
get_project(project_id: str) -> ProjectResponse
```

Get a single project by ID.

**Parameters:**
- `project_id` - Project ID

**Returns:** `ProjectResponse` with project data

---

## Models

### Project

Main project model representing a project in the system.

```python
class Project:
    id: str                      # Project ID
    name: str                    # Project name
    slug: Optional[str]          # URL-friendly slug
    color: Optional[str]         # Color enum value
    icon: Optional[Icon]         # Icon enum value
    description: Optional[str]   # Project description
    team: List[str]              # Team member IDs
    space: Optional[str]         # Space ID
    creator: str                 # Creator ID
    archiver: Optional[str]      # Archiver ID (if archived)
    archived_at: Optional[datetime]  # Archive timestamp
    created_at: datetime         # Creation timestamp
    updated_at: datetime         # Last update timestamp
```

---

## Response Models

### ProjectResponse

```python
class ProjectResponse:
    type: str                    # Response type ("GetProject")
    payload: ProjectPayload      # Response payload
    
    @property
    def project(self) -> Project:  # Convenience property
        ...
```

---

### ProjectPayload

```python
class ProjectPayload:
    project: Project             # Project object
```

---

### ProjectsResponse

```python
class ProjectsResponse:
    type: str                    # Response type ("GetProjects")
    payload: ProjectsPayload     # Response payload
    
    @property
    def projects(self) -> List[Project]:  # Convenience property
        ...
```

---

### ProjectsPayload

```python
class ProjectsPayload:
    projects: List[Project]      # List of projects
```

---

## See Also

- [Projects Guide](../guides/projects) - Usage examples and patterns

