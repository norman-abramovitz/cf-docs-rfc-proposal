import {defineCollection} from 'astro:content';
import {glob} from 'astro/loaders';
import {docsSchema} from '@astrojs/starlight/schema';

// The same glob as Starlight's docsLoader, as in the earlier rounds' sites,
// limited to one mode's folder (and the home page) when MODE is set.
const mode = process.env.MODE;
const pattern = mode ? ['index.mdoc', `${mode}/**/[^_]*.{md,mdx,mdoc}`] : ['**/[^_]*.{md,mdx,mdoc}'];

export const collections = {
  docs: defineCollection({loader: glob({base: './src/content/docs', pattern}), schema: docsSchema()}),
};
