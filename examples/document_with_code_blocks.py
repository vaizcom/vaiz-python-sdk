"""
Example of creating documents with code blocks and syntax highlighting.

Demonstrates using code_block() to display code snippets in various programming languages.
"""

from config import get_client
from vaiz import (
    heading,
    paragraph,
    code_block,
    bullet_list,
    horizontal_rule,
    text,
    toc_block,
)

# Initialize client
client = get_client()

# Document ID (replace with your actual document ID)
DOCUMENT_ID = "68fb2452322665c43876937d"

print("Creating document with code blocks...")
print("=" * 80)

# Code examples in different languages
python_example = """def fibonacci(n):
    \"\"\"Calculate the nth Fibonacci number.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Usage
result = fibonacci(10)
print(f"Fibonacci(10) = {result}")"""

javascript_example = """// Async function to fetch data
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        return data;
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

# Create document with code examples
content = [
    toc_block(),
    
    heading(1, "Code Examples Documentation"),
    
    paragraph(
        "This document demonstrates using ",
        text("code_block()", code=True),
        " to display code with syntax highlighting in various programming languages."
    ),
    
    horizontal_rule(),
    
    heading(2, "Python"),
    
    paragraph("Example of Fibonacci function implementation:"),
    
    code_block(code=python_example, language="python"),
    
    paragraph(
        text("Features:", bold=True),
        " Recursive implementation with docstring documentation."
    ),
    
    horizontal_rule(),
    
    heading(2, "JavaScript"),
    
    paragraph("Async function for API interactions:"),
    
    code_block(code=javascript_example, language="javascript"),
    
    paragraph(text("Key points:", bold=True)),
    bullet_list(
        "Using async/await for asynchronous operations",
        "Error handling with try/catch",
        "Template literals for URL formatting"
    ),
    
    horizontal_rule(),
    
    heading(2, "TypeScript"),
    
    paragraph("Typed user creation function:"),
    
    code_block(code=typescript_example, language="typescript"),
    
    paragraph(text("TypeScript benefits:", bold=True)),
    bullet_list(
        "Strong typing with interfaces",
        "Using Partial<T> for optional fields",
        "IDE autocomplete and type checking"
    ),
    
    horizontal_rule(),
    
    heading(2, "Bash"),
    
    paragraph("Deployment script:"),
    
    code_block(code=bash_example, language="bash"),
    
    paragraph("Script installs dependencies, runs tests, and starts the application."),
    
    horizontal_rule(),
    
    heading(1, "Usage in Code"),
    
    heading(2, "Basic Example"),
    
    paragraph("Creating a simple code block:"),
    
    code_block(
        code='''from vaiz import code_block

# Create block with Python code
code = code_block(
    code='print("Hello, World!")',
    language="python"
)''',
        language="python"
    ),
    
    heading(2, "Block Without Language"),
    
    paragraph("You can create a code block without specifying language:"),
    
    code_block(
        code='''code = code_block(code="some code")''',
        language="python"
    ),
    
    heading(2, "Empty Block"),
    
    paragraph("Empty code block for later editing:"),
    
    code_block(
        code='''empty = code_block()''',
        language="python"
    ),
    
    horizontal_rule(),
    
    heading(1, "Supported Languages"),
    
    paragraph("Code blocks support syntax highlighting for many languages:"),
    
    bullet_list(
        "Python, JavaScript, TypeScript",
        "Java, C, C++, C#",
        "Go, Rust, Swift, Kotlin",
        "Ruby, PHP, Perl",
        "HTML, CSS, SCSS",
        "SQL, JSON, YAML, XML",
        "Bash, Shell, PowerShell",
        "Markdown, LaTeX",
        "And many more..."
    ),
    
    paragraph(
        text("Tip: ", bold=True),
        "Always specify the programming language using the ",
        text("language", code=True),
        " parameter for proper syntax highlighting!"
    ),
]

try:
    response = client.replace_json_document(DOCUMENT_ID, content)
    print("✅ Document created successfully!")
    print()
    print("What was added:")
    print("  • TOC block for navigation")
    print("  • Code examples in Python, JavaScript, TypeScript, Bash")
    print("  • Code blocks with syntax highlighting")
    print("  • Usage examples and descriptions")
    print()
    print("Code block features:")
    print("  ✓ Syntax highlighting for many languages")
    print("  ✓ Multiline code support")
    print("  ✓ Can be empty or without language specified")
    print("  ✓ Automatic formatting and indentation")
    print()
except Exception as e:
    print(f"❌ Error: {e}")

