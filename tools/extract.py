import re,sys,json
from html.parser import HTMLParser
INLINE={'button','a','strong','b','em','i','span','sup','sub','br','small','mark','abbr','u','wbr'}
VOID={'br','img','input','meta','link','source','hr','area','base','col','embed','track','wbr'}
SKIP={'script','style','svg','head','noscript','iframe','video','canvas','select','option'}
ATTRS=('alt','title','aria-label','placeholder')
class El:
    def __init__(s,tag,attrs,so,se,par):
        s.tag=tag;s.attrs=attrs;s.so=so;s.se=se;s.eo=None;s.par=par;s.kids=[];s.text=False
class P(HTMLParser):
    def __init__(s,src):
        super().__init__(convert_charrefs=False)
        s.src=src;s.ls=[0]
        for m in re.finditer('\n',src): s.ls.append(m.end())
        s.root=El('root',{},0,0,None);s.cur=s.root;s.skipdepth=0;s.all=[]
    def off(s): 
        l,c=s.getpos(); return s.ls[l-1]+c
    def handle_starttag(s,tag,attrs):
        so=s.off();se=so+len(s.get_starttag_text())
        e=El(tag,dict(attrs),so,se,s.cur);s.cur.kids.append(e);s.all.append(e)
        if tag not in VOID: s.cur=e
        else: e.eo=se
    def handle_startendtag(s,tag,attrs):
        so=s.off();se=so+len(s.get_starttag_text())
        e=El(tag,dict(attrs),so,se,s.cur);e.eo=se;s.cur.kids.append(e);s.all.append(e)
    def handle_endtag(s,tag):
        if tag in VOID: return
        e=s.cur
        while e is not None and e.tag!=tag: e=e.par
        if e is None: return
        e.eo=s.off(); s.cur=e.par
    def handle_data(s,d):
        if d.strip(): s.cur.text=True
        # record raw text
def under_skip(e):
    while e is not None:
        if e.tag in SKIP: return True
        e=e.par
    return False
def has_only_inline(e):
    for k in e.kids:
        if k.tag not in INLINE: return False
        if not has_only_inline(k): return False
    return True
def subtree_text(e):
    if e.text: return True
    return any(subtree_text(k) for k in e.kids)
def units(src):
    p=P(src);p.feed(src);out=[]
    for e in p.all:
        if e.tag in INLINE or e.tag in VOID or e.eo is None: continue
        if under_skip(e): continue
        # parent already a unit?
        par=e.par;inunit=False
        while par is not None and par.tag!='root':
            if par.tag not in INLINE and has_only_inline(par) and subtree_text(par) and not under_skip(par): inunit=True;break
            par=par.par
        if inunit: continue
        if has_only_inline(e) and subtree_text(e):
            out.append(('html',e.se,e.eo,src[e.se:e.eo]))
    # attributes
    for e in p.all:
        if under_skip(e) and e.tag not in ('title','meta'): pass
    return p,out
if __name__=='__main__':
    allu={}
    for f in sys.argv[1:]:
        src=open(f,encoding='utf-8').read();p,u=units(src)
        keys={re.sub(r'\s+',' ',x[3]).strip() for x in u}
        for k in keys: allu.setdefault(k,[]).append(f)
        print(f,len(u),'units',len(keys),'unique')
    print('TOTAL unique',len(allu), 'chars',sum(len(k) for k in allu))
    json.dump(sorted(allu),open('/tmp/rtx/build/units_es.json','w'),ensure_ascii=False,indent=0)
