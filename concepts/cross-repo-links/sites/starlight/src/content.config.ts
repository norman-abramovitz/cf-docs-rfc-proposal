// Starlight's docsLoader() is Astro's glob() loader over src/content/docs/
// (packages/starlight/src/loaders.ts). The same loader over another folder
// lets each build take its variant's pages: PAGES_DIR, set by the Makefile.
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

const base = process.env.PAGES_DIR || './pages/passthrough';

export const collections = {
  docs: defineCollection({
    loader: glob({ base, pattern: '**/[^_]*.{md,mdx,mdoc}' }),
    schema: docsSchema(),
  }),
};
