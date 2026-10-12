// Minimal docs site for the code blocks round: the earlier rounds' site.
// Pages are Markdoc (.mdoc); allowHTML lets HTML through. Code blocks are
// drawn by Expressive Code, which Starlight sets up, through the fence node
// of Starlight's Markdoc preset (markdoc.config.mjs).
import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';
import markdoc from '@astrojs/markdoc';

export default defineConfig({
  outDir: './dist',
  integrations: [
    starlight({title: 'Code blocks round — Starlight'}),
    markdoc({allowHTML: true}),
  ],
});
