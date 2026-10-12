import Markdoc from '@markdoc/markdoc';
import {defineMarkdocConfig, component} from '@astrojs/markdoc/config';
import vars from './vars.json' with {type: 'json'};
import {table} from './list-table.mjs';
import {document} from './table-attrs.mjs';

export default defineMarkdocConfig({
  variables: {vars},
  nodes: {table, document},
  tags: {
    // {% rawhtml value=$vars.route_services /%}
    rawhtml: {render: component('./src/components/RawHtml.astro'), attributes: {value: {type: String}}, selfClosing: true},
    // {% path %}/var/vcap/jobs/JOB{% /path %}: inline code that is a path. Markdoc
    // puts an annotation on the paragraph or cell, not on the code, so a tag says it.
    path: {inline: true, transform: (node, config) => new Markdoc.Tag('code', {class: 'path'}, node.transformChildren(config))},
  },
});
