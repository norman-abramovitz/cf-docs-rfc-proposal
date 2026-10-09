// Minimal docs site for the tables round. Default Starlight theme.
import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';
import markdoc from '@astrojs/markdoc';

export default defineConfig({
  integrations: [
    starlight({
      title: 'Tables round — Starlight',
      customCss: ['./src/styles/hints.css'],
    }),
    // Pages are Markdoc (.mdoc); allowHTML lets the HTML tables through.
    markdoc({allowHTML: true}),
  ],
});
