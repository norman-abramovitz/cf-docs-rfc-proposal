import {defineCollection} from 'astro:content';
import {glob} from 'astro/loaders';
import {docsSchema} from '@astrojs/starlight/schema';

// The same glob as Starlight's docsLoader, as in the tables round's site.
const pattern = ['**/[^_]*.{md,mdx,mdoc}'];

export const collections = {
  docs: defineCollection({loader: glob({base: './src/content/docs', pattern}), schema: docsSchema()}),
};
