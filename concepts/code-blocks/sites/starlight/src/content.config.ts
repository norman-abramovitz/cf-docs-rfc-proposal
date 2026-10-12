import {defineCollection} from 'astro:content';
import {glob} from 'astro/loaders';
import {docsSchema} from '@astrojs/starlight/schema';

// The same glob as Starlight's docsLoader, as in the earlier rounds' sites.
// PROBE=1 builds only the home page and the probe folder (make probe).
const pattern = process.env.PROBE ? ['index.mdoc', 'probe/**/[^_]*.mdoc'] : ['index.mdoc', '{passthrough,native}/**/[^_]*.{md,mdx,mdoc}'];

export const collections = {
  docs: defineCollection({loader: glob({base: './src/content/docs', pattern}), schema: docsSchema()}),
};
