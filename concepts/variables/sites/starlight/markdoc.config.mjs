// The notes round's Markdoc config (the aside tag from Starlight's preset,
// the tables round's rawhtml tag), plus a link tag for a variable that holds
// a link target. The site builds once per mode (make build); MODE picks the
// variables the pages read as $vars: passthrough, the book's file as it is
// (vars.json); native, the values prepared for Markdoc (vars-native.mjs).
import {defineMarkdocConfig, component} from '@astrojs/markdoc/config';
import {StarlightMarkdocPreset} from '@astrojs/starlight-markdoc';
import vars from './vars.json' with {type: 'json'};
import nativeVars from './vars-native.mjs';

export default defineMarkdocConfig({
  variables: {vars: process.env.MODE === 'native' ? nativeVars : vars},
  tags: {
    // {% aside type="caution" title="Important" %} … {% /aside %}
    aside: StarlightMarkdocPreset.tags.aside,
    // {% rawhtml value=$vars.config_ssh_link /%}: an HTML value as markup
    rawhtml: {render: component('./src/components/RawHtml.astro'), attributes: {value: {type: String}}, selfClosing: true},
    // {% link href=$vars.gorouter_metrics_link %}metrics{% /link %}: Markdown
    // links take no tag in their target, so a variable target needs a tag
    link: {render: 'a', attributes: {href: {type: String, required: true}}},
  },
});
