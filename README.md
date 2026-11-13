# Vaiz Python SDK

> Official Python SDK for the [Vaiz](https://vaiz.com) App

[![PyPI version](https://badge.fury.io/py/vaiz-sdk.svg)](https://badge.fury.io/py/vaiz-sdk)
[![Python](https://img.shields.io/pypi/pyversions/vaiz-sdk.svg)](https://pypi.org/project/vaiz-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## About

**Vaiz** is a modern project management app that helps teams collaborate and get work done. 
This SDK provides a complete Python interface to the Vaiz API, making it easy to integrate Vaiz into your Python applications and workflows.

## Installation

```bash
pip install vaiz-sdk
```

## Quick Start

```python
from vaiz import VaizClient, CreateTaskRequest

client = VaizClient(api_key="your_api_key", space_id="your_space_id")

task = client.create_task(
    CreateTaskRequest(name="Write release notes", board="board_id", group="group_id")
).task

# Documents and task descriptions are written in Markdown
client.replace_markdown_document(
    task.document,
    "# Release notes\n\n- [x] Draft\n- [ ] Review\n\nSee **docs** for details.",
)
print(client.get_markdown_document(task.document))
```

## Documentation

**[Documentation](https://docs-python-sdk.vaiz.com)**

- [Getting Started](https://docs-python-sdk.vaiz.com/) - Installation and quick start guide
- [API Reference](https://docs-python-sdk.vaiz.com/guides/overview) - Complete API documentation
- [Examples](https://docs-python-sdk.vaiz.com/examples) - Practical code examples

## Links

- [PyPI Package](https://pypi.org/project/vaiz-sdk/)
- [GitHub Repository](https://github.com/vaizcom/vaiz-python-sdk)
- [Changelog](https://github.com/vaizcom/vaiz-python-sdk/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/vaizcom/vaiz-python-sdk/blob/main/CONTRIBUTING.md)
- [Known Issues and Tasks](https://github.com/vaizcom/vaiz-python-sdk/blob/main/KNOWN_ISSUES.md)

## License

MIT License - see [LICENSE](https://github.com/vaizcom/vaiz-python-sdk/blob/main/LICENSE) file for details.

---

Made with ❤️ by the Vaiz team
