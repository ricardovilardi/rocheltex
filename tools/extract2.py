import re,json,sys
sys.path.insert(0,'.')
from extract import P,El,INLINE,VOID,SKIP,under_skip,has_only_inline,subtree_text
def norm(s): return re.sub(r'\s+',' ',s).strip()
def collect(e,out):
    # e: element (leaf-block or inline child) that has only-inline subtree
    if e.text or not e.kids:
        if subtree_text(e): out.append(e)
        return
    # no direct text: recurse into children
    for k in e.kids:
        if k.tag in VOID and k.tag!='br': continue
        if k.tag=='br': continue
        collect(k,out)
def units(src):
    p=P(src);p.feed(src);out=[]
    seen=set()
    for e in p.all:
        if e.tag in INLINE or e.tag in VOID or e.eo is None or under_skip(e): continue
        # inside a bigger unit?
        par=e.par;skip=False
        while par is not None and par.tag!='root':
            if par.tag not in INLINE and has_only_inline(par) and subtree_text(par) and not under_skip(par): skip=True;break
            par=par.par
        if skip: continue
        if has_only_inline(e) and subtree_text(e):
            tmp=[];collect(e,tmp)
            for u in tmp:
                if u.eo is None: continue
                out.append((u.se,u.eo))
    # inline elements with their own text that sit under a container with block children (e.g. nav buttons)
    ranges=[(a,b) for a,b in out]
    for e in p.all:
        if e.tag not in INLINE or e.tag=='br' or e.eo is None or under_skip(e) or not e.text: continue
        if any(a<=e.se and e.eo<=b for a,b in ranges): continue
        if not has_only_inline(e): continue
        out.append((e.se,e.eo)); ranges.append((e.se,e.eo))
    return p,out
ATTR=re.compile(r'\b(alt|aria-label|title|placeholder|content)="([^"]*)"')
def attr_units(src):
    res=[]
    for m in re.finditer(r'<(img|a|button|svg|iframe|input|textarea|div|span|meta|link)\b[^>]*>',src):
        tag=m.group(0)
        if tag.startswith('<meta'):
            mm=re.search(r'(name|property)="(description|og:title|og:description)"',tag)
            if mm:
                c=re.search(r'content="([^"]*)"',tag)
                if c: res.append(c.group(1))
            continue
        for a in re.finditer(r'\b(alt|aria-label|title|placeholder)="([^"]*)"',tag):
            res.append(a.group(2))
    t=re.search(r'<title>(.*?)</title>',src,re.S)
    if t: res.append(t.group(1))
    return res
if __name__=='__main__':
    files=sys.argv[1:]
    allu={}
    for f in files:
        src=open(f,encoding='utf-8').read();p,u=units(src)
        for a,b in u: allu.setdefault(norm(src[a:b]),set()).add(f.split('/')[-1])
        for v in attr_units(src): allu.setdefault(norm(v),set()).add(f.split('/')[-1]+'@attr')
    keys=sorted(allu)
    json.dump(keys,open('/tmp/rtx/build/units_es.json','w'),ensure_ascii=False)
    print(len(keys),'unique units;',sum(len(k) for k in keys),'chars')
