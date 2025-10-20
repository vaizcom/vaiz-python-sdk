import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    'intro',
    'getting-started',
    {
      type: 'category',
      label: 'Guides',
      items: [
        'api/overview',
        'api/boards',
        'api/comments',
        'api/custom-fields',
        'api/documents',
        'api/files',
        'api/helpers',
        'api/history',
        'api/milestones',
        'api/profile',
        'api/projects',
        'api/blockers',
        'api/tasks',
      ],
    },
    'api/methods',
    'examples',
  ],
};

export default sidebars;
