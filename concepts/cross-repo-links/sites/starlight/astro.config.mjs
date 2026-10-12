// Site for the cross-repository links round: the earlier rounds' Starlight
// site with Markdoc pages. URLS picks the URL style:
//   html:    pages are written as <path>.html (build.format: 'file'), the
//            book's URLs, and Starlight writes its own links that way
//   default: Astro's default, <path>/index.html
// One edit link base for the whole site.
import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';
import markdoc from '@astrojs/markdoc';

const html = (process.env.URLS || 'html') === 'html';
// The redirect probe (REDIRECTS=1): two old URLs that the book's redirects.rb
// sends to routes-domains (L38, L115), one in the same repository's folder
// and one in another's
const redirects = process.env.REDIRECTS === '1' ? {
  '/devguide/deploy-apps/domains-routes': '/devguide/deploy-apps/routes-domains.html',
  '/adminguide/manage-domains-routes': '/devguide/deploy-apps/routes-domains.html',
} : {};

export default defineConfig({
  site: 'https://docs.cloudfoundry.org',
  redirects,
  ...(html ? {build: {format: 'file'}, trailingSlash: 'never'} : {}),
  integrations: [
    starlight({
      title: 'Cross-repository links round — Starlight',
      editLink: {baseUrl: 'https://github.com/cloudfoundry/docs-dev-guide/blob/master/'},
    }),
    // Pages are Markdoc (.mdoc); allowHTML lets HTML through.
    markdoc({allowHTML: true}),
  ],
});
