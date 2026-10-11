// The headings round's Markdoc config, plus two tags: Starlight's own aside
// tag, from its Markdoc preset, for native notes; and the tables round's
// rawhtml tag, for a note held in a variable. Only the preset's aside tag is
// taken, so code blocks render as in the earlier rounds. vars.json is passed
// to every page as $vars.
import {defineMarkdocConfig, component} from '@astrojs/markdoc/config';
import {StarlightMarkdocPreset} from '@astrojs/starlight-markdoc';
import vars from './vars.json' with {type: 'json'};

export default defineMarkdocConfig({
  variables: {vars},
  tags: {
    // {% aside type="caution" title="Important" %} … {% /aside %}
    aside: StarlightMarkdocPreset.tags.aside,
    // {% rawhtml value=$vars.external_vol_win_note /%}
    rawhtml: {render: component('./src/components/RawHtml.astro'), attributes: {value: {type: String}}, selfClosing: true},
  },
});
