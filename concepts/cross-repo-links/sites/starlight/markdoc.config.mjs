// Markdoc variables for the depth probe (make probe-depth); no test page
// uses them.
import {defineMarkdocConfig} from '@astrojs/markdoc/config';
import vars from './probes/depth/vars.mjs';

export default defineMarkdocConfig({variables: {vars}});
