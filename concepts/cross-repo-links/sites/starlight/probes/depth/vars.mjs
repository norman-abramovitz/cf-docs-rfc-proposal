// Three values that hold a link, parsed by Markdoc into the tree it renders
// (the variables round's native form): the book's relative URL, a
// root-relative URL, and the URL Starlight writes for the page.
import Markdoc from '@markdoc/markdoc';

const inline = (md) => Markdoc.transform(Markdoc.parse(md)).children[0].children;

export default {
  relative: inline('For more information, see [variable relative](../adminguide/supporting-websockets.html).'),
  root: inline('For more information, see [variable root](/adminguide/supporting-websockets.html).'),
  native: inline('For more information, see [variable native](/adminguide/supporting-websockets.html).'),
};
