// Three values that hold a link, as a variables module holds markup (the
// variables round's native form): the book's relative URL, a root-relative
// URL, and Docusaurus's Link component with the page's route.
import Link from '@docusaurus/Link';

export const relative = <>For more information, see <a href="../adminguide/supporting-websockets.html">variable relative</a>.</>;
export const root = <>For more information, see <a href="/adminguide/supporting-websockets.html">variable root</a>.</>;
export const native = <>For more information, see <Link to="/adminguide/supporting-websockets">variable native</Link>.</>;
