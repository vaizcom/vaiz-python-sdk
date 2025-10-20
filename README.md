# Vaiz SDK for Python

Official Python SDK for the Vaiz platform API.

[![PyPI version](https://badge.fury.io/py/vaiz-sdk.svg)](https://badge.fury.io/py/vaiz-sdk)
[![Python](https://img.shields.io/pypi/pyversions/vaiz-sdk.svg)](https://pypi.org/project/vaiz-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📚 Full Documentation

**[📖 Read the full documentation →](https://vaiz-python-sdk.vercel.app)**

## Features

- ✨ **Fully Typed** - Complete type hints with Pydantic v2
- 📅 **Automatic DateTime Handling** - Seamless conversion between Python datetime and ISO strings  
- 🎨 **Enums** - Type-safe enums for icons, colors, and constants
- 🎛️ **Custom Field Helpers** - Powerful functions for working with custom fields
- 📁 **File Upload** - Easy file upload from local disk or URL
- 💬 **Full Comment System** - Comments with reactions, replies, and file attachments

## Installation

```bash
pip install vaiz-sdk
```

## Quick Start

```python
from vaiz import VaizClient
from vaiz.models import CreateTaskRequest, TaskPriority

# Create client
client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id"
)

# Create a task
task = CreateTaskRequest(
    name="My First Task",
    board="board_id",
    group="group_id",
    priority=TaskPriority.High
)

response = client.create_task(task)
print(f"✅ Task created: {response.task.id}")
```

## Environment Variables

Create a `.env` file:

```env
VAIZ_API_KEY=your_api_key
VAIZ_SPACE_ID=your_space_id
```

```python
from dotenv import load_dotenv
import os

load_dotenv()

client = VaizClient(
    api_key=os.getenv("VAIZ_API_KEY"),
    space_id=os.getenv("VAIZ_SPACE_ID")
)
```

## Documentation

- [Getting Started](https://vaiz-python-sdk.vercel.app/getting-started) - Installation and setup
- [API Reference](https://vaiz-python-sdk.vercel.app/api/overview) - Complete API documentation
  - [Tasks](https://vaiz-python-sdk.vercel.app/api/tasks) - Create, update, and manage tasks
  - [Comments](https://vaiz-python-sdk.vercel.app/api/comments) - Comments, reactions, and replies
  - [Files](https://vaiz-python-sdk.vercel.app/api/files) - File uploads and attachments
  - [Milestones](https://vaiz-python-sdk.vercel.app/api/milestones) - Track progress with milestones
  - [Boards](https://vaiz-python-sdk.vercel.app/api/boards) - Boards and custom fields
  - [Projects](https://vaiz-python-sdk.vercel.app/api/projects) - Projects, profile, and history
- [Examples](https://vaiz-python-sdk.vercel.app/examples) - Ready-to-use code examples
- [Contributing](https://vaiz-python-sdk.vercel.app/contributing) - How to contribute

## Requirements

- Python 3.8+
- `requests` >= 2.31.0
- `pydantic` >= 2.0
- `python-dotenv` >= 0.9.0

## Development

```bash
# Clone repository
git clone https://github.com/vaizcom/vaiz-python-sdk.git
cd vaiz-python-sdk

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests
pip install pytest pytest-mock python-dotenv
PYTHONPATH=. pytest
```

## Examples

Check out the [examples/](examples/) directory for more code samples:

- [Creating tasks](examples/create_task.py)
- [Working with files](examples/upload_file.py)
- [Custom fields](examples/custom_field_helpers_usage.py)
- [Comments and reactions](examples/post_comment.py)
- [Milestones](examples/create_milestone.py)

## Links

- [Documentation](https://vaiz-python-sdk.vercel.app)
- [PyPI Package](https://pypi.org/project/vaiz-sdk/)
- [GitHub Repository](https://github.com/vaizcom/vaiz-python-sdk)
- [Issue Tracker](https://github.com/vaizcom/vaiz-python-sdk/issues)
- [Changelog](CHANGELOG.md)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://vaiz-python-sdk.vercel.app)
- 💬 [GitHub Discussions](https://github.com/vaizcom/vaiz-python-sdk/discussions)
- 🐛 [Issue Tracker](https://github.com/vaizcom/vaiz-python-sdk/issues)
- 📧 Email: support@vaiz.com
