"""Writes the test pages of each site from one list, so every tool gets the
same titles, text and content dates. Run once; the written pages are kept
in the repository.

Usage: python3 -I pages.py ROUND_DIR

access-control is the headings round's native conversion of the whole page,
copied with its content date added. The other three pages hold the
published page's title and first paragraph (variables resolved, as
published): this round tests the frame around the content, not the content.
"""
import os, re, sys

ROUND = sys.argv[1]
CONCEPTS = os.path.dirname(ROUND)
HEADINGS = os.path.join(CONCEPTS, 'headings', 'sites')

# Content dates: the author date (UTC) of the newest commit to the page's
# source file, skipping the candidate commits in survey/candidates.txt
# (survey/pages.csv, column author_date_skipping_candidates).
PAGES = {
    'access-control': ('Managing access to Service Plans', '2026-06-26', None),
    'architecture': ('Logging and metrics architecture', '2024-12-05',
                     'Logging and metrics architecture includes components that transport logs and metrics '
                     'from your Cloud Foundry deployment to destinations such as the Cloud Foundry '
                     'Command-Line Interface (cf CLI), monitoring tools, or internal system components.'),
    'using-vol-services': ('Using an external file system (volume services)', '2023-05-31',
                           'Here are instructions to help you read and write to a mounted file system from '
                           'your apps. In Cloud Foundry, a volume service provides a volume so your app can '
                           'read or write to a reliable, persistent file system.'),
    'high-availability': ('High Availability in Cloud Foundry', '2026-06-29',
                          'This topic tells you about the components used to ensure high availability in '
                          'Cloud Foundry, vertical and horizontal scaling, and the infrastructure required to '
                          'support scaling component VMs for high availability.'),
}

TOOLS = {
    # tool: (pages folder, extension, how the date is written, source of access-control)
    'docusaurus': ('docs', '.mdx', 'last_update:\n  date: {d}', 'docusaurus/docs/native/access-control.mdx'),
    'zensical': ('docs', '.md', 'revision_date: {d}', 'zensical/docs/native/access-control.md'),
    'starlight': ('src/content/docs', '.mdoc', 'lastUpdated: {d}', 'starlight/src/content/docs/native/access-control.mdoc'),
    'antora': ('pages/modules/ROOT/pages', '.adoc', ':page-last-updated: {d}', 'antora/native/modules/ROOT/pages/access-control.adoc'),
}

for tool, (folder, ext, field, src) in TOOLS.items():
    out = os.path.join(ROUND, 'sites', tool, folder)
    os.makedirs(out, exist_ok=True)
    for name, (title, date, para) in PAGES.items():
        line = field.format(d=date)
        if para is None:
            text = open(os.path.join(HEADINGS, src), encoding='utf-8').read()
            if ext == '.adoc':
                text = re.sub(r'^(= .*\n)', r'\1' + line + '\n', text, count=1)
            else:
                text = text.replace('\n---\n', '\n' + line + '\n---\n', 1)
        elif ext == '.adoc':
            text = f'= {title}\n{line}\n\n{para}\n'
        else:
            text = f'---\ntitle: "{title}"\n{line}\n---\n\n{para}\n'
        open(os.path.join(out, name + ext), 'w', encoding='utf-8').write(text)
    print(tool, out)
