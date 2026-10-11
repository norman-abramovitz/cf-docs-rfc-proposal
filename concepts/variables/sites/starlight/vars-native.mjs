// The variables native pages read as $vars: text values from the book's
// file (vars.json), and values that hold markup written as Markdown (the
// converter turns the book's HTML into Markdown) and parsed by Markdoc into
// the tree it renders, so {% $vars.name %} renders a link as a link. Only
// the values the test pages use are written here.
import Markdoc from '@markdoc/markdoc';
import data from './vars.json' with {type: 'json'};

const markup = {
  // HTML in the book's file
  config_ssh_link: 'For more information, see [Configuring SSH Access for Cloud Foundry](../../running/config-ssh.html).',
  container_network_link: 'For information about administering container-to-container network policies, see [Configuring Container-to-Container Networking](../devguide/deploy-apps/cf-networking.html).',
  // Markdown in the book's file
  platform_ssh_configuration: data.platform_ssh_configuration,
  app_sec_groups_link: data.app_sec_groups_link,
};

// The inline content of a one-paragraph value
const inline = (md) => Markdoc.transform(Markdoc.parse(md)).children[0].children;

export default {...data, ...Object.fromEntries(Object.entries(markup).map(([k, v]) => [k, inline(v)]))};
