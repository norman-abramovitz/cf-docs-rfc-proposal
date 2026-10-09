import {defineCollection} from 'astro:content';
import {glob} from 'astro/loaders';
import {docsSchema} from '@astrojs/starlight/schema';

// The same glob as Starlight's docsLoader, plus exclusions: raw passthrough
// pages are kept as evidence and built only with RAW=1, and the one raw page
// that does not parse stops the whole build, so it is never built.
const pattern = ['**/[^_]*.{md,mdx,mdoc}', '!passthrough-raw/troubleshooting_slow_requests.mdoc'];
if (!process.env.RAW) pattern.push('!passthrough-raw/**');

export const collections = {
  docs: defineCollection({loader: glob({base: './src/content/docs', pattern}), schema: docsSchema()}),
};
