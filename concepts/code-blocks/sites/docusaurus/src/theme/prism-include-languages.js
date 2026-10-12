// The classic theme's prism-include-languages.js (Docusaurus 3.10.2),
// ejected, which Docusaurus allows ("eject: safe"), plus one line: Prism has
// no `console` grammar, so `console` is made a name for `shell-session`.
// customFields.consoleAlias false (make probe) leaves the line out.
import siteConfig from '@generated/docusaurus.config';
export default function prismIncludeLanguages(PrismObject) {
  const {
    themeConfig: {prism},
    customFields,
  } = siteConfig;
  const {additionalLanguages} = prism;
  const PrismBefore = globalThis.Prism;
  globalThis.Prism = PrismObject;
  additionalLanguages.forEach((lang) => {
    // eslint-disable-next-line global-require, import/no-dynamic-require
    require(`prismjs/components/prism-${lang}`);
  });
  if (customFields.consoleAlias !== false) {
    PrismObject.languages.console = PrismObject.languages['shell-session'];
  }
  delete globalThis.Prism;
  if (typeof PrismBefore !== 'undefined') {
    globalThis.Prism = PrismObject;
  }
}
