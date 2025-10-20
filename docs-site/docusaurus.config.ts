import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Vaiz Python SDK',
  tagline: 'Official Python SDK for the Vaiz platform',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://docs-python-sdk.vaiz.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'vaizcom', // Usually your GitHub org/user name.
  projectName: 'vaiz-python-sdk', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',  // Docs at root instead of /docs
          editUrl:
            'https://github.com/vaizcom/vaiz-python-sdk/tree/main/docs-site/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    // Algolia DocSearch configuration
    algolia: {
      // Application ID provided by Algolia
      appId: '55Y6IM29JE',
      
      // Public API key: it is safe to commit it
      apiKey: 'e3a005e6dcc969173ae27b34390db823',
      
      // Index name
      indexName: 'vaiz-python-sdk',
      
      // Optional: see doc section below
      contextualSearch: true,
      
      // Optional: Specify domains where the navigation should occur through window.location instead of history.push
      // externalUrlRegex: 'external\\.com|domain\\.com',
      
      // Optional: Replace parts of the item URLs from Algolia
      // replaceSearchResultPathname: {
      //   from: '/docs/', // or as RegExp: /\/docs\//
      //   to: '/',
      // },
      
      // Optional: Algolia search parameters
      searchParameters: {},
      
      // Optional: path for search page that enabled by default (`false` to disable it)
      searchPagePath: 'search',
      
      // Optional: whether the insights feature is enabled or not on Docsearch (`false` by default)
      insights: false,
    },
    navbar: {
      title: 'Vaiz Python SDK',
      logo: {
        alt: 'Vaiz Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          href: 'https://github.com/vaizcom/vaiz-python-sdk',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Introduction',
              to: '/',
            },
            {
              label: 'Getting Started',
              to: '/',
            },
            {
              label: 'API Reference',
              to: '/api/methods',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/vaizcom/vaiz-python-sdk',
            },
            {
              label: 'Vaiz App',
              href: 'https://vaiz.com',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Examples',
              to: '/examples',
            },
            {
              label: 'Contributing',
              href: 'https://github.com/vaizcom/vaiz-python-sdk/blob/main/CONTRIBUTING.md',
            },
            {
              label: 'Changelog',
              href: 'https://github.com/vaizcom/vaiz-python-sdk/blob/main/CHANGELOG.md',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Vaiz. Made with ❤️`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
