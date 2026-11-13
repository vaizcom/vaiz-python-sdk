"""
Example: Documents with code blocks and syntax highlighting in Markdown.

Code blocks are fenced with triple backticks followed by the language name.
A ```mermaid fence becomes an interactive diagram block.
"""

from examples.config import get_client
from vaiz.models import CreateDocumentRequest, Kind


def build_markdown() -> str:
    python_example = '''def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Usage
result = fibonacci(10)
print(f"Fibonacci(10) = {result}")'''

    javascript_example = """// Async function to fetch data
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching user:', error);
        throw error;
    }
}"""

    typescript_example = """interface User {
    id: string;
    name: string;
    email: string;
    roles: string[];
}

function createUser(data: Partial<User>): User {
    return {
        id: crypto.randomUUID(),
        name: data.name || 'Anonymous',
        email: data.email || '',
        roles: data.roles || ['user']
    };
}"""

    bash_example = """#!/bin/bash

# Install dependencies and start application
echo "Installing dependencies..."
npm install

echo "Running tests..."
npm test

echo "Starting application..."
npm start"""

    mermaid_example = """graph LR
    A[Write code] --> B[Run tests]
    B --> C[Deploy]"""

    return f"""# Code Examples Documentation

This document demonstrates fenced code blocks with syntax highlighting
in various programming languages.

---

## Python

Example of a Fibonacci function implementation:

```python
{python_example}
```

**Features:** recursive implementation with a docstring.

## JavaScript

Async function for API interactions:

```javascript
{javascript_example}
```

**Key points:**

- Using async/await for asynchronous operations
- Error handling with try/catch
- Template literals for URL formatting

## TypeScript

Typed user creation function:

```typescript
{typescript_example}
```

## Bash

Deployment script:

```bash
{bash_example}
```

## Diagram

```mermaid
{mermaid_example}
```

---

> **Tip:** always specify the programming language after the opening fence.
> A fence without a language gets a default language assigned by the editor.
"""


def main():
    client = get_client()
    client.verbose = True

    print("Creating document with code blocks...")
    print("=" * 80)

    try:
        document_id = client.create_document(
            CreateDocumentRequest(
                kind=Kind.Space,
                kind_id=client.space_id,
                title="Code Blocks Example",
                index=0,
            )
        ).payload.document.id

        client.replace_markdown_document(document_id, build_markdown())
        print(f"✅ Document created successfully: {document_id}")

        saved = client.get_markdown_document(document_id)
        fences = [line for line in saved.splitlines() if line.startswith("```") and len(line) > 3]
        print(f"Code fences with a language: {fences}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
