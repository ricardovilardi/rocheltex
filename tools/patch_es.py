import re,glob,os
R='../'
EN={'index.html':'en/index.html','rocheltex-proceso.html':'en/process.html','rocheltex-productos.html':'en/products.html',
 'rocheltex-nosotros.html':'en/about.html','rocheltex-esg.html':'en/commitment.html','rocheltex-contacto.html':'en/contact.html',
 'rocheltex-aviso-legal.html':'en/legal-notice.html','rocheltex-privacidad.html':'en/privacy-policy.html','rocheltex-cookies.html':'en/cookie-policy.html'}
def patch(f):
    p=R+f; s=open(p,encoding='utf-8').read(); o=s
    if 'assets/consent.css' not in s:
        s=s.replace('<link rel="stylesheet" href="fonts/fonts.css">','<link rel="stylesheet" href="fonts/fonts.css">\n<link rel="stylesheet" href="assets/consent.css">',1)
    if 'assets/consent.js' not in s:
        s=s.replace('</body>','<script src="assets/consent.js" data-policy="rocheltex-cookies.html"></script>\n</body>',1)
    s=s.replace('''<a href="#">Aviso legal</a>
        <a href="#">Privacidad</a>
        <a href="#">Cookies</a>''','''<a href="rocheltex-aviso-legal.html">Aviso legal</a>
        <a href="rocheltex-privacidad.html">Privacidad</a>
        <a href="rocheltex-cookies.html">Cookies</a>
        <button type="button" class="link-btn" data-open-cookies>Configurar cookies</button>''')
    en=EN.get(f)
    if en:
        s=s.replace('<div class="lang"><b>ES</b> / EN</div>','<div class="lang"><b>ES</b> / <a href="%s" hreflang="en" lang="en">EN</a></div>'%en)
        s=s.replace('<div class="mob-lang"><b>ES</b> / EN</div>','<div class="mob-lang"><b>ES</b> / <a href="%s" hreflang="en" lang="en">EN</a></div>'%en)
        # hreflang alternates (relative; to be made absolute with the final domain)
        if 'hreflang="en"' not in s.split('</head>')[0]:
            s=s.replace('</head>','<link rel="alternate" hreflang="es" href="%s">\n<link rel="alternate" hreflang="en" href="%s">\n</head>'%(f,en),1)
    if f=='rocheltex-contacto.html':
        s=s.replace('<iframe src="https://www.google.com/maps?q=Rocheltex+S.L.,+Pol%C3%ADgono+Serrans,+100,+46812+Aielo+de+Malferit,+Valencia&output=embed" loading="lazy"',
                    '<iframe data-consent="maps" hidden data-link="https://www.google.com/maps?q=Rocheltex+S.L.,+Pol%C3%ADgono+Serrans,+100,+46812+Aielo+de+Malferit,+Valencia" data-src="https://www.google.com/maps?q=Rocheltex+S.L.,+Pol%C3%ADgono+Serrans,+100,+46812+Aielo+de+Malferit,+Valencia&output=embed" loading="lazy"')
        if 'consent-row' not in s:
            s=s.replace('<button type="submit" class="btn">Enviar mensaje</button>','''<div class="consent-row"><label><input type="checkbox" name="Privacidad" required><span>He leído y acepto la <a href="rocheltex-privacidad.html">Política de privacidad</a>.</span></label></div>
        <button type="submit" class="btn">Enviar mensaje</button>
        <p class="form-info"><strong>Información básica sobre protección de datos.</strong> Responsable: Rocheltex, S.L. Finalidad: atender tu consulta. Base jurídica: tu consentimiento. Destinatarios: no se cederán datos a terceros salvo obligación legal. Derechos: acceso, rectificación, supresión, oposición, limitación y portabilidad, escribiendo a jss@rocheltex.es. Más información en la <a href="rocheltex-privacidad.html">Política de privacidad</a>.</p>''',1)
    open(p,'w',encoding='utf-8').write(s); return s!=o
if __name__=='__main__':
    for f in ['index.html','rocheltex-proceso.html','rocheltex-productos.html','rocheltex-nosotros.html','rocheltex-esg.html','rocheltex-contacto.html']:
        print(f,patch(f))
