// The earlier rounds' Markdoc config (the aside tag from Starlight's preset)
// plus the preset's fence node, so fences are drawn by Expressive Code with
// a copy button, and the round's variables (vars.json) as $vars.
//
// The preset passes a fence's raw text to Expressive Code (its `content`
// attribute), so a variable in a fence would show as written,
// `{% $vars.app_domain %}`. The fence node below takes the text from the
// fence's children instead, where Markdoc has put each variable's value
// (eight lines of site code).
import Markdoc from '@markdoc/markdoc';
import {defineMarkdocConfig} from '@astrojs/markdoc/config';
import {StarlightMarkdocPreset} from '@astrojs/starlight-markdoc';
import vars from './vars.json' with {type: 'json'};

const presetFence = StarlightMarkdocPreset.nodes.fence;

export default defineMarkdocConfig({
  variables: {vars},
  nodes: {
    // ```lang … ``` -> Expressive Code's <Code>, with variables replaced
    fence: {
      ...presetFence,
      transform(node, config) {
        const attributes = node.transformAttributes(config);
        const content = node.transformChildren(config).join('');
        return new Markdoc.Tag(this.render, {...attributes, code: content}, []);
      },
    },
  },
  tags: {
    // {% aside type="caution" title="Important" %} … {% /aside %}
    aside: StarlightMarkdocPreset.tags.aside,
  },
});
