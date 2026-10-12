// Build-time values round: the copyright year and "last updated" date.
// The footer is overridden (src/components/Footer.astro) to add the
// copyright notice; YEAR_MODE (build, site or page) and SITE_YEAR choose
// its year, as in the Docusaurus site. lastUpdated: true makes pages
// without a date in their front matter read it from Git.
import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';
import markdoc from '@astrojs/markdoc';

if (process.env.YEAR_MODE === 'site' && !/^\d{4}$/.test(process.env.SITE_YEAR || '')) {
  throw new Error('YEAR_MODE=site needs SITE_YEAR (four digits)');
}

export default defineConfig({
  integrations: [
    starlight({
      title: 'Build-time values round — Starlight',
      lastUpdated: true,
      components: {Footer: './src/components/Footer.astro'},
    }),
    markdoc({allowHTML: true}),
  ],
});
