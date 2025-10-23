import React from 'react';
import { useDoc } from '@docusaurus/plugin-content-docs/client';
import Head from '@docusaurus/Head';

export default function DocItemMetadata(): JSX.Element {
  const { metadata, frontMatter } = useDoc();
  const { permalink, title, description } = metadata;

  // Skip if no title or description
  if (!title || !description) {
    return null;
  }

  // Determine proficiency level based on path
  let proficiencyLevel = 'Intermediate';
  if (permalink.includes('/getting-started') || permalink === '/') {
    proficiencyLevel = 'Beginner';
  } else if (permalink.includes('/api-reference/')) {
    proficiencyLevel = 'Advanced';
  } else if (permalink.includes('/guides/basics')) {
    proficiencyLevel = 'Beginner';
  } else if (permalink.includes('/patterns/')) {
    proficiencyLevel = 'Intermediate';
  }

  // Clean title (remove " | Vaiz Python SDK" suffix if present)
  const cleanTitle = title.replace(/ \| Vaiz Python SDK$/g, '').trim();

  // Create structured data
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    headline: cleanTitle,
    description: description,
    proficiencyLevel: proficiencyLevel,
    programmingLanguage: 'Python',
    mainEntityOfPage: `https://docs-python-sdk.vaiz.com${permalink}`,
    creator: {
      '@type': 'Organization',
      name: 'Vaiz',
      url: 'https://vaiz.com',
    },
    datePublished: '2024-01-01',
    dateModified: new Date().toISOString().split('T')[0],
    inLanguage: 'en',
    about: {
      '@type': 'SoftwareSourceCode',
      name: 'Vaiz Python SDK',
      programmingLanguage: 'Python',
      codeRepository: 'https://github.com/vaizcom/vaiz-python-sdk',
    },
  };

  return (
    <Head>
      <title>{title}</title>
      <meta property="og:title" content={title} />
      <script type="application/ld+json">
        {JSON.stringify(structuredData)}
      </script>
    </Head>
  );
}

