// Minimal docs site for the notes round: the headings round's site (the
// tables round's without its table CSS). Default Starlight theme.
import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';
import markdoc from '@astrojs/markdoc';

export default defineConfig({
  integrations: [
    starlight({title: 'Notes round — Starlight'}),
    // Pages are Markdoc (.mdoc); allowHTML lets HTML through.
    markdoc({allowHTML: true}),
  ],
});
