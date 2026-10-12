"""Builds index.html: published tables next to Docusaurus, Zensical, Starlight, and Antora."""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))

PAGES = [
    ("scale-table-host", "_oss_scale_table", "docs-cloudfoundry-concepts · partial included by high-availability",
     "https://docs.cloudfoundry.org/concepts/high-availability.html", [
        ("Component / Total Instances / Notes",
         "Source widths 25/25/50. In extension the key column stays on one line up to a 16em cap, so “Cloud Controller Worker” widens it (Docusaurus 30/24/46, Zensical 26/25/49, Starlight 31/24/45; in Antora it fits at 25%). Zensical, Starlight, and Antora native carry the widths. Plain pipe tables size columns by content; plain AsciiDoc tables make them equal. Passthrough adds <code>class=\"table\"</code>: every HTML table names its style."),
    ]),
    ("credential-types", "credential-types", "docs-credhub", "https://docs.cloudfoundry.org/credhub/credential-types.html", [
        ("Type / Description",
         "The published page never applied its <code>table</code> class: the source wrote it with curly quotes. The quotes are made straight, so <code>class=\"table\"</code> names the standard style, as on every HTML table (decided). Column 1 is 20% wide. Extension adds row headers."),
    ]),
    ("metadata", "metadata", "docs-cf-admin", "https://docs.cloudfoundry.org/adminguide/metadata.html", [
        ("Label requirements",
         "Title: passthrough keeps the source’s spanning row; every other mode shows it as a bold line above the table, because Markdown tables have one header row (decided). The stray backslashes in <code>\\[a-z0-9A-Z\\]</code> are removed in every mode. Pipe tables hold the lists as inline HTML."),
        ("Annotation requirements", "Same shape and decisions as the label table."),
        ("Selector requirement reference", "Already a Markdown table in the source. Extension adds row headers and roles; Antora native already has row headers (its <code>cols</code> marks column 1 with <code>h</code>)."),
    ]),
    ("troubleshooting_slow_requests", "troubleshooting_slow_requests", "docs-cf-admin",
     "https://docs.cloudfoundry.org/adminguide/troubleshooting_slow_requests.html", [
        ("Experiment 1: total round-trip requests",
         "Passthrough carries each table’s widths as written; every other mode uses no widths and lets the column roles decide (variant C, decided). This table sets no widths in the source."),
        ("Experiment 2: request time in access logs", "Sits inside step 4 of a numbered list, so it is narrower. The source sets a width on column 1 only."),
        ("Experiment 3: duplicate latency", "The source sets a width on column 1 only."),
        ("Experiment 4: remove the load balancer", "The source sets a width on column 1 only."),
        ("Experiment 5: remove Gorouter", "The source sets widths on columns 1 and 2."),
        ("Experiment 6: network between router and app", "The source sets widths on columns 1 and 2."),
    ]),
    ("uaa-concepts", "uaa-concepts", "docs-uaa", "https://docs.cloudfoundry.org/uaa/uaa-concepts.html", [
        ("Grant type / User / Details",
         "The <code>implicit</code> row ended with <code>&lt;/td&gt;</code> instead of <code>&lt;/tr&gt;</code>; it is fixed. Column 1 is 30% wide wherever the mode carries widths. Without widths, columns are sized by content or made equal: column 1 is 27% in Docusaurus native, 16% in Zensical native-plain, 27% in Starlight native-plain and 33% in Antora native-plain. Its identifiers do not break."),
        ("Key / Value",
         "In the <code>allowed providers</code> row, <code>&lt;br/&gt;&lt;br/&gt;</code> is a paragraph break (decided): two paragraphs in extension, in Starlight native, and in Antora native and native-plain; passthrough and pipe tables keep the breaks."),
    ]),
    ("uaa-performance", "uaa-performance", "docs-running-cf · first section only; added after the round",
     "https://docs.cloudfoundry.org/running/uaa-performance.html", [
        ("Instances / Threads / Throughput",
         "The example of a second table style, <code>table-media</code>: no cell borders, a rule under the header, centered cells, images filling their cells. Passthrough names it as the class; extension names it in each tool’s own way (a directive class in Docusaurus, a <code>style</code> option in Zensical, Markdoc’s class shorthand in Starlight, a role in Antora). Native keeps the standard style (decided), although Starlight’s and Antora’s own table syntax could name it. The published page opens the charts in a lightbox script; the converted pages link to the image."),
    ]),
    ("roles-table-host", "_oss_roles_table", "docs-cloudfoundry-concepts · partial included by roles; added 2026-10-12",
     "https://docs.cloudfoundry.org/concepts/roles.html", [
        ("Activity / eleven roles",
         "Twelve columns, wider than the content column in every tool. Each tool scrolls it in a box of its own and lays it out at its narrowest, each column as wide as its longest word, so the activity column wraps on every row; Zensical gives every column the same 100 pixels. The published page has no box: the table spills 154 pixels into the margin. <b>Full table</b> shows every column; <b>As seen</b> shows the part each tool’s box shows before the reader scrolls it."),
    ]),
]

# Each table's nearest anchor on the published page: the id on the heading above it
ANCHORS = {
    "scale-table-host": ["instance-counts"],
    "credential-types": ["cred-types"],
    "metadata": ["reqs-labels", "reqs-annotations", "requirements-reference"],
    "troubleshooting_slow_requests": ["total-latency", "within-cf", "duplicate-latency",
                                      "remove-the-load-balancer", "remove-the-gorouter", "test-internal-network"],
    "uaa-concepts": ["select-type", "additional-info"],
    "uaa-performance": ["client-credentials"],
    "roles-table-host": ["activeroles"],
}

TOOLS = [("docusaurus", "Docusaurus 3.10.2"), ("zensical", "Zensical 0.0.69"), ("starlight", "Starlight 0.42.6"), ("antora", "Antora 3.2.1")]
MODES = [
    ("passthrough", "Passthrough", "The source HTML with only the changes each tool forces: closed tags, style objects, tbody and colgroup for Docusaurus (MDX); none beyond the intent cleanup for Zensical; entities and one-line cells for Starlight, where Markdoc cannot take the HTML as is; in Antora the HTML sits in an AsciiDoc passthrough block, and the page around it is rewritten as AsciiDoc."),
    ("extension", "Extension", "A list-table carrying the hints (row headers, roles, capped no-wrap) through each tool’s extension point: a remark plugin in Docusaurus, a Python-Markdown block in Zensical, attributes on Markdoc’s table tag in Starlight, AsciiDoc’s own table options plus CSS in Antora (no code)."),
    ("native", "Native", "Each tool’s own table syntax and whatever hints it carries: pipe tables in Docusaurus (no widths), pipe tables with widths on header cells in Zensical, Markdoc’s table tag in Starlight, AsciiDoc tables with column specs in Antora."),
    ("native-plain", "Native, plain", "Tables with no width or alignment specs: bare pipe tables, columns sized by their content (Docusaurus native is already this); in Antora, AsciiDoc tables without <code>cols</code>, which get equal columns."),
]


def esc(t):
    return html.escape(t, quote=True)


def figure(page, n, tool, label):
    src = f"img/{tool}-passthrough-{page}-t{n}.jpg"
    return (f'<figure class="tool-{tool}" data-tool="{tool}"><figcaption><span class="tag conv">{esc(label)}</span>'
            f' <span class="mode-name">passthrough</span></figcaption>'
            f'<a class="shot" href="{src}" target="_blank" rel="noopener"><img class="conv-img" src="{src}" alt="{esc(label)} table {n}" loading="lazy"></a></figure>')


sections = []
for page, name, repo, url, tables in PAGES:
    pairs = []
    for i, (title, note) in enumerate(tables, 1):
        pub = f"img/published-{page}-t{i}.jpg"
        figs = [f'<figure class="pub"><figcaption><span class="tag pub">Published</span> docs.cloudfoundry.org</figcaption>'
                f'<a class="shot" href="{pub}" target="_blank" rel="noopener"><img src="{pub}" alt="Published {esc(name)} table {i}" loading="lazy"></a></figure>']
        figs += [figure(page, i, t, label) for t, label in TOOLS]
        pairs.append(f'''      <article class="pair" data-page="{page}" data-table="{i}">
        <header class="pair-head"><h3><span class="tno">Table {i}</span> {esc(title)}</h3><p class="note">{note} <a href="{url}#{ANCHORS[page][i - 1]}" target="_blank" rel="noopener">This table on the published page</a>.</p></header>
        <div class="cols">{''.join(figs)}</div>
      </article>''')
    n = len(tables)
    sections.append(f'''    <section id="{page}" class="page">
      <div class="page-head"><h2>{esc(name)}</h2><p class="meta"><span>{esc(repo)}</span> · <a href="{url}" target="_blank" rel="noopener">published page</a> · {n} table{'s' if n > 1 else ''}</p></div>
{chr(10).join(pairs)}
    </section>''')

mode_buttons = ''.join(f'<button type="button" data-mode="{m}" aria-pressed="{str(i == 0).lower()}">{esc(l)}</button>' for i, (m, l, _) in enumerate(MODES))
tool_buttons = ''.join(f'<button type="button" data-tool="{t}" aria-pressed="true">{esc(l.split()[0])}</button>' for t, l in TOOLS)
nav = ''.join(f'<a href="#{p}">{esc(n)}</a>' for p, n, *_ in PAGES)
desc = json.dumps({m: d for m, _, d in MODES})

# Tables that scroll in their box also have a screenshot of the whole table
full = json.dumps(sorted(f[:-len('-full.jpg')] for f in os.listdir(os.path.join(HERE, 'img')) if f.endswith('-full.jpg')))
page = open(os.path.join(HERE, 'template.html')).read()
page = (page.replace('{{MODE_BUTTONS}}', mode_buttons).replace('{{TOOL_BUTTONS}}', tool_buttons)
        .replace('{{NAV}}', nav).replace('{{SECTIONS}}', '\n'.join(sections)).replace('{{DESC}}', desc).replace('{{FULL}}', full))
open(os.path.join(HERE, 'index.html'), 'w').write(page)
