---
sidebar_position: 2
slug: /
---

# Getting Started

Learn how to install and configure the Vaiz Python SDK.

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

Install the SDK using pip:

```bash
pip install vaiz-sdk
```

## Environment Setup

### Environment Variables

Create a `.env` file in your project root:

```env
VAIZ_API_KEY=your_api_key
VAIZ_SPACE_ID=your_space_id
```

:::tip Where to get API key?
You can get your API key from your [profile settings](https://app.vaiz.com/settings/api-tokens) on the Vaiz App.
:::

### Loading Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("VAIZ_API_KEY")
space_id = os.getenv("VAIZ_SPACE_ID")
```

## Creating a Client

### Production Environment

```python
from vaiz import VaizClient

client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id"
)
```

## Next Steps

Now you know the basics of working with Vaiz SDK! Here's what to explore next:

- 📖 [API Overview](./guides/basics) - Complete overview of all SDK capabilities
- 📋 [Tasks](./guides/tasks) - Full task management
- 💬 [Comments](./guides/comments) - Comments, reactions, and replies
- 📁 [Files](./guides/files) - File uploads and attachments
- 🎯 [Milestones](./guides/milestones) - Track progress with milestones
- 📊 [Boards](./guides/boards) - Board types and groups
- 🎛️ [Custom Fields](./guides/custom-fields) - Extend tasks with custom data
- 📂 [Projects](./guides/projects) - Project management
- 👤 [Profile](./guides/profile) - User information
- 📝 [Documents](./guides/documents) - Task descriptions
- 📜 [History Events](./guides/history) - Change tracking
- 🔗 [Task Blockers](./guides/blockers) - Manage task dependencies
- 🛠️ [Helper Functions](./guides/helpers) - Utility functions for common tasks
- 💡 [Examples](./patterns/introduction) - Ready-to-use code examples

## Useful Links

- [GitHub Repository](https://github.com/vaizcom/vaiz-python-sdk)
- [PyPI Package](https://pypi.org/project/vaiz-sdk/)
- [Contributing Guide](https://github.com/vaizcom/vaiz-python-sdk/blob/main/CONTRIBUTING.md)
- [Changelog](https://github.com/vaizcom/vaiz-python-sdk/blob/main/CHANGELOG.md)

