// The variables module native pages import: `import vars from '@site/src/vars'`.
// Text values come from the book's file (vars.json, written by ../vars.js).
// Values that hold markup are JSX, as the converter would write them from
// the book's HTML and Markdown, so `{vars.name}` renders a link as a link;
// only the ones the test pages use are written here. A name the module does
// not define stops the build: "Variable not defined: vars.name".
import data from '@site/vars.json';

const markup = {
  // HTML in the book's file
  config_ssh_link: <>For more information, see <a href="../../running/config-ssh.html">Configuring SSH Access for Cloud Foundry</a>.</>,
  container_network_link: <>For information about administering container-to-container network policies, see <a href="../devguide/deploy-apps/cf-networking.html">Configuring Container-to-Container Networking</a>.</>,
  // Markdown in the book's file
  platform_ssh_configuration: <>Cloud Foundry deployments control SSH access to apps at the Cloud Foundry level. Additionally, Cloud Foundry supports load balancing of SSH sessions. For more information about setting SSH access for your deployment, see <a href="../../running/config-ssh.html">Configuring SSH Access</a>.</>,
  app_sec_groups_link: <>For more information about ASGs, see <a href="../adminguide/app-sec-groups.html">App Security Groups</a>.</>,
};

// Names React and the bundler ask for on any module object
const internal = new Set(['$$typeof', '__esModule', 'then', 'toJSON', 'default']);

export default new Proxy({...data, ...markup}, {
  get(values, name) {
    if (typeof name === 'string' && !(name in values) && !internal.has(name)) {
      throw new Error(`Variable not defined: vars.${name}`);
    }
    return values[name];
  },
});
