import {defineMarkdocConfig, component} from '@astrojs/markdoc/config';
import vars from './vars.json' with {type: 'json'};
import {table} from './list-table.mjs';

export default defineMarkdocConfig({
  variables: {vars},
  nodes: {table},
  tags: {
    // {% rawhtml value=$vars.route_services /%}
    rawhtml: {render: component('./src/components/RawHtml.astro'), attributes: {value: {type: String}}, selfClosing: true},
  },
});
