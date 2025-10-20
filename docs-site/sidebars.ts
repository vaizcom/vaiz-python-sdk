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
      ],
    },
    'examples',
    'contributing',
  ],
};

export default sidebars;
