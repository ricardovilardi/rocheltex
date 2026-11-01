import re,sys,os,json
sys.path.insert(0,'.')
from extract2 import units,norm
from en_a import A
from en_b import B
from en_c import C
R='../'
PAGES={'index.html':'index.html','rocheltex-proceso.html':'process.html','rocheltex-productos.html':'products.html',
 'rocheltex-nosotros.html':'about.html','rocheltex-esg.html':'commitment.html','rocheltex-contacto.html':'contact.html',
 'rocheltex-aviso-legal.html':'legal-notice.html','rocheltex-privacidad.html':'privacy-policy.html','rocheltex-cookies.html':'cookie-policy.html'}
TR=A+B+C
EXACT={}
for k,v in TR: EXACT.setdefault(k,v)
used=set();missing={}
def lookup(key):
    if key in EXACT: used.add(key); return EXACT[key]
    c=[(k,v) for k,v in TR if key.startswith(k)]
    if not c: return None
    m=max(len(k) for k,_ in c); best=[(k,v) for k,v in c if len(k)==m]
    if len({v for _,v in best})>1: raise SystemExit('ambiguous: '+key[:60])
    used.add(best[0][0]); return best[0][1]
def tr_unit(inner):
    key=norm(inner)
    # numbers
    if re.fullmatch(r'[\d.,]+(K)?(<small>t</small>)?',key): return re.sub(r'(\d),(\d)',r'\1.\2',inner)
    if re.fullmatch(r'<span class="accent" data-count="\d+">0</span>\.000 m²',key): return inner.replace('</span>.000','</span>,000')
    en=lookup(key)
    if en is None:
        missing[key]=missing.get(key,0)+1; return inner
    lead=re.match(r'\s*',inner).group(0); trail=re.search(r'\s*$',inner).group(0)
    return lead+en+trail
def rewrite_url(v):
    if v.startswith(('http:','https:','mailto:','tel:','#','data:','javascript:')): return v
    base,h,frag=v.partition('#')
    if base in PAGES: return PAGES[base]+(h+frag)
    if base=='' : return v
    return '../'+v
def build(es,en):
    src=open(R+es,encoding='utf-8').read()
    p,us=units(src)
    out=src
    for a,b in sorted(us,reverse=True):
        out=out[:a]+tr_unit(out[a:b])+out[b:]
    # attributes + title + meta
    def attr_sub(m):
        tag=m.group(0)
        def one(mm):
            val=mm.group(2); en_v=lookup(norm(val))
            return mm.group(1)+'="'+(en_v if en_v is not None else val)+'"'
        if tag.startswith('<meta'):
            if re.search(r'(name|property)="(description|og:title|og:description)"',tag):
                return re.sub(r'(content)="([^"]*)"',one,tag)
            return tag
        return re.sub(r'\b(alt|aria-label|title|placeholder)="([^"]*)"',one,tag)
    out=re.sub(r'<[a-zA-Z][^>]*>',attr_sub,out)
    out=re.sub(r'<title>(.*?)</title>',lambda m:'<title>'+(lookup(norm(m.group(1))) or m.group(1))+'</title>',out,flags=re.S)
    # options
    for a,b in {'Automoción':'Automotive','Geotextiles':'Geotextiles','Hilatura':'Spinning','Punzonado':'Needle-punching','Otro':'Other'}.items():
        out=out.replace('<option>%s</option>'%a,'<option>%s</option>'%b)
    out=out.replace("'Ir a la fase '","'Go to step '")
    out=out.replace('<html lang="es">','<html lang="en">')
    # language switchers
    out=re.sub(r'<div class="lang">.*?</div>','<div class="lang"><a href="../%s" hreflang="es" lang="es">ES</a> / <b>EN</b></div>'%es,out)
    out=re.sub(r'<div class="mob-lang">.*?</div>','<div class="mob-lang"><a href="../%s" hreflang="es" lang="es">ES</a> / <b>EN</b></div>'%es,out)
    # urls
    out=re.sub(r'\b(href|src|poster|action)="([^"]*)"',lambda m: m.group(1)+'="'+(m.group(2) if '../'+es==m.group(2) or m.group(2).startswith('../') else rewrite_url(m.group(2)))+'"',out)
    out=out.replace('data-policy="rocheltex-cookies.html"','data-policy="cookie-policy.html"')
    out=re.sub(r'<link rel="alternate" hreflang="es" href="[^"]*">\n<link rel="alternate" hreflang="en" href="[^"]*">','<link rel="alternate" hreflang="es" href="../%s">\n<link rel="alternate" hreflang="en" href="%s">'%(es,en),out)
    return out
if __name__=='__main__':
    os.makedirs(R+'en',exist_ok=True)
    for es,en in PAGES.items():
        o=build(es,en); open(R+'en/'+en,'w',encoding='utf-8').write(o); print(es,'->','en/'+en,len(o))
    unused=[k for k,_ in TR if k not in used]
    print('\nUNTRANSLATED units (kept as is):',len(missing))
    for k,c in sorted(missing.items()): print('  ',repr(k[:110]))
    print('\nUNUSED translation entries:',len(unused))
    for k in unused: print('  ',repr(k[:80]))
