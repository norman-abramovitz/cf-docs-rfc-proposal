// The tables round's Markdoc config without its table hints, which no page
// here uses: vars.json is passed to every page as $vars.
import {defineMarkdocConfig} from '@astrojs/markdoc/config';
import vars from './vars.json' with {type: 'json'};

export default defineMarkdocConfig({
  variables: {vars},
});
