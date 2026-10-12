"""Compare the <pre> elements of book-render.rb's pages with published pages.

Usage:
  python3 -I compare-published.py WORK_DIR PAIRS
      WORK_DIR is book-render.rb's (its html/ tree). PAIRS is a file with
      one line per page: the model page's path under html/, a space, and
      the published page's file (relative to the PAIRS file). Prints, per
      page, how many <pre> elements each side has and every pair that
      differs.

The published site rewrites e-mail addresses (Cloudflare's e-mail
obfuscation puts "[email protected]" in a link and decodes it in the browser
with a script); such links are decoded before the comparison, as the
script would. Nothing else is changed: two <pre> elements are the same
when their HTML is the same, character for character.
"""
import os, re, sys

if len(sys.argv) != 3:
    sys.exit(__doc__)
work, pairs = sys.argv[1:]
base = os.path.dirname(os.path.abspath(pairs))
CF = re.compile(r'<a href="/cdn-cgi/l/email-protection" class="__cf_email__" data-cfemail="([0-9a-f]+)">\[email&#160;protected\]</a>')


def cf(m):
    h = m.group(1)
    k = int(h[:2], 16)
    return ''.join(chr(int(h[i:i + 2], 16) ^ k) for i in range(2, len(h), 2))


def pres(path):
    return [CF.sub(cf, p) for p in re.findall(r'<pre[^>]*>.*?</pre>', open(path, encoding='utf-8').read(), re.S)]


total = same = 0
for line in open(pairs):
    if not line.strip() or line.startswith('#'):
        continue
    model, pub = line.split()
    a, b = pres(os.path.join(work, 'html', model)), pres(os.path.join(base, pub))
    diff = [i for i in range(max(len(a), len(b))) if i >= len(a) or i >= len(b) or a[i] != b[i]]
    total += 1
    same += not diff and len(a) == len(b)
    print(f'{"same" if not diff else "DIFF"}  {model}: model {len(a)}, published {len(b)} <pre>'
          + (f'; first difference at <pre> {diff[0] + 1}' if diff else ''))
print(f'{same} of {total} pages: every <pre> the same')
