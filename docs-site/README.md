# Vaiz SDK Documentation

This directory contains the Docusaurus documentation for the Vaiz Python SDK.

## 🚀 Quick Start

```bash
npm install
npm start
```

Opens at `http://localhost:3000`

## 📂 Structure

```
docs/
├── intro.md              # Introduction
├── getting-started.md    # Installation and setup
├── api/                  # API Reference
│   ├── overview.md       # API overview
│   ├── tasks.md          # Tasks API
│   ├── comments.md       # Comments API
│   ├── files.md          # Files API
│   ├── milestones.md     # Milestones API
│   ├── boards.md         # Boards API
│   ├── custom-fields.md  # Custom Fields API
│   ├── projects.md       # Projects API
│   ├── profile.md        # Profile API
│   ├── documents.md      # Documents API
│   ├── history.md        # History Events API
│   ├── blockers.md       # Task Blockers API
│   └── helpers.md        # Helper Functions
├── examples.md           # Code examples
└── ...
```

## 🛠️ Commands

```bash
npm start          # Development server
npm run build      # Production build
npm run serve      # Serve production build
```

## 📝 Writing Docs

All documentation is in Markdown with MDX support. Edit files in `docs/` and changes will auto-reload.

## 🚢 Deployment

Documentation auto-deploys via:
- **Vercel**: Push to main branch
- **GitHub Pages**: `.github/workflows/deploy-docs.yml`

See deployment details in project root.
