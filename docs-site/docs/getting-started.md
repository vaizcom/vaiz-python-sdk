---
sidebar_position: 2
slug: /
---

# Getting Started

Get up and running with Vaiz SDK in minutes! 🚀

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

# For production use (verify_ssl=True by default)
client = VaizClient(
    api_key="your_api_key",
    space_id="your_space_id"
)
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    response = client.get_task("invalid_task_id")
except HTTPError as e:
    print(f"❌ HTTP Error: {e}")
    print(f"   Status: {e.response.status_code}")
    print(f"   Response: {e.response.text}")
except Exception as e:
    print(f"❌ Unknown error: {e}")
```

## Next Steps

Now you know the basics of working with Vaiz SDK! Here's what to explore next:

- 📖 [API Reference](./api/client) - Complete documentation of all methods
- 🎛️ [Custom Fields](./guides/custom-fields) - Working with custom fields
- 💬 [Comments](./api/comments) - Create and manage comments
- 📁 [Files](./api/files) - Upload and attach files
- 💡 [Examples](./examples) - Ready-to-use examples for different scenarios

## Useful Links

- [GitHub Repository](https://github.com/vaizcom/vaiz-python-sdk)
- [PyPI Package](https://pypi.org/project/vaiz-sdk/)
- [Changelog](https://github.com/vaizcom/vaiz-python-sdk/blob/main/CHANGELOG.md)

