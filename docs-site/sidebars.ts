import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    'intro',
    'getting-started',
    {
      type: 'category',
      label: 'Guides',
      items: [
        'guides/basics',
        'guides/boards',
        'guides/comments',
        'guides/custom-fields',
        'guides/documents',
        'guides/files',
        'guides/helpers',
        'guides/history',
        'guides/members',
        'guides/milestones',
        'guides/profile',
        'guides/projects',
        'guides/spaces',
        'guides/blockers',
        'guides/tasks',
      ],
    },
    {
      type: 'category',
      label: 'API Reference',
      items: [
        'api-reference/overview',
        'api-reference/boards',
        'api-reference/comments',
        'api-reference/documents',
        'api-reference/enums',
        'api-reference/files',
        'api-reference/history',
        'api-reference/members',
        'api-reference/milestones',
        'api-reference/profile',
        'api-reference/projects',
        'api-reference/spaces',
        'api-reference/tasks',
      ],
    },
    {
      type: 'category',
      label: 'Patterns & Best Practices',
      items: [
        'patterns/introduction',
        'patterns/common-patterns',
        'patterns/environment-setup',
        'patterns/error-handling',
        'patterns/integrations',
        'patterns/performance',
        'patterns/ready-to-run',
        'patterns/real-world',
        'patterns/documents',
      ],
    },
  ],
};

export default sidebars;
