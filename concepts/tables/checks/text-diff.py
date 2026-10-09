"""Word-by-word comparison of a page's main text: the published page against a
built page. Prints only the differences.
Usage: python3 text-diff.py PUBLISHED.html BUILT.html
PUBLISHED.html is saved from docs.cloudfoundry.org; BUILT.html from a site build."""
import sys, re, html.parser, difflib
BLOCK = {'p','li','td','th','tr','h1','h2','h3','h4','h5','h6','div','pre','ul','ol','table','thead','tbody','caption','br','section','figure','blockquote'}
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','source','track','wbr'}
class X(html.parser.HTMLParser):
    def __init__(s, start):
        super().__init__(); s.start=start; s.depth=None; s.skip_at=None; s.out=[]; s.d=0
    def handle_starttag(s, t, a):
        if t in BLOCK: s.out.append(' ')
        if t in VOID: return
        s.d += 1; a = dict(a); cls = a.get('class') or ''
        if s.depth is None and s.start(t, a): s.depth = s.d
        if s.depth is not None and s.skip_at is None and (t in ('script','style','nav','button') or 'hash-link' in cls or 'theme-doc-toc' in cls or 'breadcrumbs' in cls or 'theme-doc-version' in cls):
            s.skip_at = s.d
    def handle_endtag(s, t):
        if t in BLOCK: s.out.append(' ')
        if t in VOID: return
        if s.skip_at is not None and s.d == s.skip_at: s.skip_at = None
        if s.depth is not None and s.d == s.depth: s.depth = -1
        s.d -= 1
    def handle_data(s, d):
        if s.depth not in (None, -1) and s.skip_at is None: s.out.append(d)
def words(path, start):
    x = X(start); x.feed(open(path).read())
    return re.findall(r'\S+', ''.join(x.out).replace('​', '').replace(' ', ' '))
pub = words(sys.argv[1], lambda t, a: t == 'main' and a.get('id') == 'js-content')
got = words(sys.argv[2], lambda t, a: t == 'article')
sm = difflib.SequenceMatcher(None, pub, got, autojunk=False)
print(f'published {len(pub)} words, converted {len(got)} words, matching {sm.ratio():.3f}')
for op, a1, a2, b1, b2 in sm.get_opcodes():
    if op == 'equal': continue
    print(f'  {op:8} published: {" ".join(pub[a1:a2])[:150]!r}\n           converted: {" ".join(got[b1:b2])[:150]!r}')
