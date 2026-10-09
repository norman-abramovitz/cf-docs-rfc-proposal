"""Prints each table in a built page: rows, cells per row, caption, and
"NESTED-CELLS" when a cell opens inside another cell.
Usage: python3 tables.py PAGE.html [--text]"""
import sys, html.parser
class P(html.parser.HTMLParser):
    def __init__(s):
        super().__init__(); s.tables=[]; s.stack=[]; s.cell=None; s.cap=None
    def handle_starttag(s,t,a):
        if t=='table': s.stack.append({'rows':[], 'caption':None})
        elif not s.stack: return
        elif t=='tr': s.stack[-1]['rows'].append([])
        elif t in('td','th') and s.stack[-1]['rows']:
            if s.cell is not None: s.stack[-1].setdefault('nested',0); s.stack[-1]['nested']+=1
            s.cell={'tag':t,'text':'','attrs':dict(a),'code':0,'p':0,'li':0}; s.stack[-1]['rows'][-1].append(s.cell)
        elif t=='caption': s.cap=''
        elif s.cell is not None:
            if t=='code': s.cell['code']+=1
            if t=='p': s.cell['p']+=1
            if t=='li': s.cell['li']+=1
    def handle_endtag(s,t):
        if t=='table' and s.stack: s.tables.append(s.stack.pop())
        elif t in('td','th'): s.cell=None
        elif t=='caption' and s.stack: s.stack[-1]['caption']=s.cap.strip(); s.cap=None
    def handle_data(s,d):
        if s.cap is not None: s.cap+=d
        elif s.cell is not None: s.cell['text']+=d
p=P(); p.feed(open(sys.argv[1]).read())
for i,t in enumerate(p.tables,1):
    shape=[len(r) for r in t['rows'] if r]
    print(f"table {i}: rows={len(shape)} cells/row={shape} caption={t['caption']!r}" + (f" NESTED-CELLS={t['nested']}" if t.get('nested') else ''))
    if '--text' in sys.argv:
        for r in t['rows']:
            print('   |', ' | '.join(f"{c['tag']}{'[code%d]'%c['code'] if c['code'] else ''}{'[p%d]'%c['p'] if c['p'] else ''}{'[li%d]'%c['li'] if c['li'] else ''}:{' '.join(c['text'].split())[:60]}" for c in r))
