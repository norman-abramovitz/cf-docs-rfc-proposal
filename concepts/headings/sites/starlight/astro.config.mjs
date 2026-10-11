// Minimal docs site for the headings round: the tables round's site without
// its table CSS, which no page here uses. Default Starlight theme.
import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';
import markdoc from '@astrojs/markdoc';

export default defineConfig({
  integrations: [
    starlight({title: 'Headings round — Starlight'}),
    // Pages are Markdoc (.mdoc); allowHTML lets HTML through.
    markdoc({allowHTML: true}),
  ],
});
