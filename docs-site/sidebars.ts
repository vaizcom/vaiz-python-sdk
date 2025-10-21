import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    'intro',
    'getting-started',
    {
      type: 'category',
      label: 'Guides',
      items: [
        'guides/overview',
        'guides/boards',
        'guides/comments',
        'guides/custom-fields',
        'guides/documents',
        'guides/files',
        'guides/helpers',
        'guides/history',
        'guides/milestones',
        'guides/profile',
        'guides/projects',
        'guides/blockers',
        'guides/tasks',
      ],
    },
    {
      type: 'category',
      label: 'API Reference',
      items: [
        'api-reference/overview',
        'api-reference/tasks',
        'api-reference/comments',
        'api-reference/files',
        'api-reference/milestones',
        'api-reference/boards',
        'api-reference/projects',
        'api-reference/profile',
        'api-reference/documents',
        'api-reference/history',
        'api-reference/enums',
      ],
    },
    'examples',
  ],
};

export default sidebars;
