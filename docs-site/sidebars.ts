import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    'intro',
    'getting-started',
    {
      type: 'category',
      label: 'API Reference',
      items: [
        'api/overview',
        'api/tasks',
        'api/comments',
        'api/files',
        'api/milestones',
        'api/boards',
        'api/custom-fields',
        'api/projects',
        'api/profile',
        'api/documents',
        'api/history',
        'api/blockers',
        'api/helpers',
      ],
    },
    'examples',
  ],
};

export default sidebars;
