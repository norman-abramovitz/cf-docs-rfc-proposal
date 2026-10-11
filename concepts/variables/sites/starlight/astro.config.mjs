// Minimal docs site for the variables round: the notes round's site. The
// site builds once per mode (make build): MODE picks the pages
// (src/content.config.ts), the variables (markdoc.config.mjs) and the
// output folder, .build/<mode>; make merges the two into dist/.
import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';
import markdoc from '@astrojs/markdoc';

export default defineConfig({
  outDir: `.build/${process.env.MODE || 'all'}`,
  integrations: [
    starlight({title: 'Variables round — Starlight'}),
    // Pages are Markdoc (.mdoc); allowHTML lets HTML through.
    markdoc({allowHTML: true}),
  ],
});
