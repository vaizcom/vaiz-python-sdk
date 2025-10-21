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
    'guides/methods',
    'examples',
  ],
};

export default sidebars;
