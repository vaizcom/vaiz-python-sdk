# Vaiz SDK Documentation

This directory contains the Docusaurus-based documentation for the Vaiz Python SDK.

## Development

### Installation

```bash
cd docs-site
npm install
```

### Local Development

```bash
npm start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

### Deployment

The documentation is automatically deployed when changes are pushed to the main branch.

## Structure

```
docs-site/
├── docs/                   # Documentation markdown files
│   ├── intro.md           # Introduction
│   ├── getting-started.md # Getting Started guide
│   ├── api/               # API Reference
│   ├── examples.md        # Examples
│   └── contributing.md    # Contributing guide
├── src/                   # Custom React components
│   ├── components/        # Homepage components
│   └── pages/             # Custom pages
├── static/                # Static assets
└── docusaurus.config.ts   # Docusaurus configuration
```

## Writing Documentation

### Markdown Files

All documentation is written in Markdown with optional MDX support.

### Code Blocks

Use syntax highlighting for code examples:

\`\`\`python
from vaiz import VaizClient

client = VaizClient(api_key="...", space_id="...")
\`\`\`

### Admonitions

Use admonitions for notes, tips, warnings:

\`\`\`markdown
:::tip
This is a helpful tip!
:::

:::warning
This is a warning!
:::

:::info
This is informational content.
:::
\`\`\`

### Links

- Internal links: `[Getting Started](./getting-started)`
- External links: `[GitHub](https://github.com/vaizcom/vaiz-python-sdk)`

## Contributing

When adding new documentation:

1. Create/update markdown files in `docs/`
2. Update `sidebars.ts` if adding new sections
3. Test locally with `npm start`
4. Submit a pull request

## Learn More

- [Docusaurus Documentation](https://docusaurus.io/)
- [MDX Documentation](https://mdxjs.com/)
