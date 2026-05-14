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

## 📈 Analytics

The docs site uses Nexly via `@nexly/react-web`.

Set `NEXLY_INGEST_KEY` in the environment that starts or builds `docs-site`:

```bash
NEXLY_INGEST_KEY=your-ingest-key npm start
```

For production, set `NEXLY_INGEST_KEY` in the hosting provider or CI/CD environment
(for example, Vercel project environment variables). `NEXLY_APP_ID` is optional and
defaults to the Vaiz docs app ID configured in `docusaurus.config.ts`.

## 📝 Writing Docs

All documentation is in Markdown with MDX support. Edit files in `docs/` and changes will auto-reload.

## 🚢 Deployment

Documentation auto-deploys via:
- **Vercel**: Push to main branch
- **GitHub Pages**: `.github/workflows/deploy-docs.yml`

See deployment details in project root.
