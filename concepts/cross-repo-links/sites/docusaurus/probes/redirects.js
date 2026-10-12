// Client-side redirects for the redirect probe (make probe-redirects): two
// old URLs that the book's redirects.rb sends to routes-domains (L38, L115),
// one in the same repository's folder and one in another's. With the default
// URL style, also a redirect from every page's old <path>.html.
const urls = process.env.URLS || 'html';
module.exports = {
  redirects: [
    {from: '/devguide/deploy-apps/domains-routes', to: '/devguide/deploy-apps/routes-domains'},
    {from: '/adminguide/manage-domains-routes', to: '/devguide/deploy-apps/routes-domains'},
  ],
  ...(urls === 'default' ? {fromExtensions: ['html']} : {}),
};
