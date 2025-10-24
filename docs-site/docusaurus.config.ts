import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: "Vaiz Python SDK",
  tagline: "Official Python SDK for the Vaiz platform",
  favicon: "img/favicon.ico",

  plugins: [
    [
      "docusaurus-plugin-plausible",
      {
        domain: "docs-python-sdk.vaiz.com",
      },
    ],
    // Inject additional <head> tags
    function () {
      return {
        name: "custom-favicon-tags",
        injectHtmlTags() {
          return {
            headTags: [
              {
                tagName: "link",
                attributes: {
                  rel: "apple-touch-icon",
                  href: "/apple-touch-icon.png",
                  sizes: "180x180",
                },
              },
              {
                tagName: "link",
                attributes: {
                  rel: "icon",
                  type: "image/png",
                  sizes: "48x48",
                  href: "/favicon-48x48.png",
                },
              },
              {
                tagName: "link",
                attributes: {
                  rel: "icon",
                  type: "image/png",
                  sizes: "96x96",
                  href: "/favicon-96x96.png",
                },
              },
              {
                tagName: "link",
                attributes: {
                  rel: "icon",
                  type: "image/png",
                  sizes: "32x32",
                  href: "/favicon-32x32.png",
                },
              },
              {
                tagName: "link",
                attributes: {
                  rel: "icon",
                  type: "image/png",
                  sizes: "16x16",
                  href: "/favicon-16x16.png",
                },
              },
              {
                tagName: "link",
                attributes: {
                  rel: "icon",
                  type: "image/svg+xml",
                  href: "/favicon.svg",
                },
              },
              {
                tagName: "link",
                attributes: {
                  rel: "manifest",
                  href: "/site.webmanifest",
                },
              },
              {
                tagName: "link",
                attributes: {
                  rel: "icon",
                  type: "image/x-icon",
                  href: "/favicon.ico",
                },
              },
            ],
          };
        },
      };
    },
  ],

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: "https://docs-python-sdk.vaiz.com",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: "/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "vaizcom", // Usually your GitHub org/user name.
  projectName: "vaiz-python-sdk", // Usually your repo name.

  onBrokenLinks: "throw",

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          routeBasePath: "/", // Docs at root instead of /docs
          // editUrl: 'https://github.com/vaizcom/vaiz-python-sdk/tree/main/docs-site/', // Disabled to hide "Edit this page" button
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: "img/docusaurus-social-card.jpg",
    colorMode: {
      respectPrefersColorScheme: true,
    },
    // Algolia DocSearch configuration
    algolia: {
      // Application ID provided by Algolia
      appId: "55Y6IM29JE",

      // Public API key: it is safe to commit it
      apiKey: "e3a005e6dcc969173ae27b34390db823",

      // Index name
      indexName: "docs_python_sdk_vaiz_com_55y6im29je_docs",

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
      searchParameters: {
        // Show more content in snippets
        attributesToSnippet: ["content:30"],
        // Retrieve hierarchy for better context
        attributesToRetrieve: [
          "hierarchy.lvl0",
          "hierarchy.lvl1",
          "hierarchy.lvl2",
          "hierarchy.lvl3",
          "content",
          "url",
          "type",
        ],
        // Highlight matching terms
        attributesToHighlight: [
          "hierarchy.lvl1",
          "hierarchy.lvl2",
          "hierarchy.lvl3",
          "content",
        ],
      },

      // Optional: path for search page that enabled by default (`false` to disable it)
      searchPagePath: "search",

      // Optional: whether the insights feature is enabled or not on Docsearch (`false` by default)
      insights: false,
    },
    navbar: {
      title: "Vaiz Python SDK",
      logo: {
        alt: "Vaiz Logo",
        src: "img/logo.svg",
      },
      items: [
        {
          label: "v0.15.0",
          href: "https://pypi.org/project/vaiz-sdk/0.15.0/",
          position: "left",
        },
        {
          href: "https://github.com/vaizcom/vaiz-python-sdk",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Documentation",
          items: [
            {
              label: "Getting Started",
              to: "/",
            },
            {
              label: "Introduction",
              to: "/intro",
            },
            {
              label: "API Reference",
              to: "/api-reference/overview",
            },
          ],
        },
        {
          title: "Community",
          items: [
            {
              label: "PyPI Package",
              href: "https://pypi.org/project/vaiz-sdk/",
            },
            {
              label: "GitHub",
              href: "https://github.com/vaizcom/vaiz-python-sdk",
            },
            {
              label: "Vaiz App",
              href: "https://vaiz.com",
            },
          ],
        },
        {
          title: "More",
          items: [
            {
              label: "Examples",
              to: "/patterns/introduction",
            },
            {
              label: "Contributing",
              href: "https://github.com/vaizcom/vaiz-python-sdk/blob/main/CONTRIBUTING.md",
            },
            {
              label: "Changelog",
              href: "https://github.com/vaizcom/vaiz-python-sdk/blob/main/CHANGELOG.md",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Vaiz. Made with ❤️`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ["python", "bash"],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
