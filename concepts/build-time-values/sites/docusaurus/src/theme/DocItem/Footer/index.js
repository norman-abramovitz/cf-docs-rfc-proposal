// The doc footer as the theme draws it ("Last updated on ..."), plus, when
// YEAR_MODE=page, the copyright notice with the year of this page's own
// content date. The site footer cannot read a page's metadata, so the
// per-page notice sits here. A wrapped theme component: React code.
import React from 'react';
import Footer from '@theme-original/DocItem/Footer';
import {useDoc} from '@docusaurus/plugin-content-docs/client';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function FooterWrapper(props) {
  const {siteConfig} = useDocusaurusContext();
  const {metadata} = useDoc();
  const at = metadata.lastUpdatedAt;
  return (
    <>
      <Footer {...props} />
      {siteConfig.customFields.yearMode === 'page' && at && (
        <p className="page-copyright">
          <a href="/">Cloud Foundry Documentation</a> &copy; {new Date(at).getUTCFullYear()}{' '}
          <a href="https://cloudfoundry.org">Cloud Foundry Foundation</a>. All Rights Reserved.
        </p>
      )}
    </>
  );
}
