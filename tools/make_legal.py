import re
R='../'
base=open(R+'rocheltex-contacto.html',encoding='utf-8').read()
head=base[:base.index('<section class="intro-band">')]
tail=base[base.index('<footer>'):]
CSS='''
  /* LEGAL */
  .legal{padding:64px 0 120px;}
  .intro-band .wrap{max-width:860px;}
  .legal .wrap.legal-body{max-width:860px;}
  .legal-body .meta{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--ink-soft);margin:0 0 36px;}
  .legal-body h2{font-size:clamp(20px,2.2vw,25px);letter-spacing:-.015em;margin:44px 0 14px;line-height:1.25;}
  .legal-body h2:first-of-type{margin-top:0;}
  .legal-body h3{font-size:16.5px;margin:26px 0 8px;}
  .legal-body p,.legal-body li{font-size:15.5px;line-height:1.72;color:var(--ink-soft);}
  .legal-body p{margin:0 0 14px;}
  .legal-body ul,.legal-body ol{margin:0 0 16px;padding-left:22px;}
  .legal-body li{margin:0 0 6px;}
  .legal-body a{color:var(--red);text-decoration:underline;text-underline-offset:2px;}
  .legal-body strong{color:var(--ink);}
  .legal-table{width:100%;border-collapse:collapse;margin:6px 0 22px;font-size:14px;}
  .legal-table th,.legal-table td{border:1px solid var(--line);padding:11px 13px;text-align:left;vertical-align:top;line-height:1.55;color:var(--ink-soft);}
  .legal-table th{background:var(--cream-2);color:var(--ink);font-weight:600;font-family:'JetBrains Mono',monospace;font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;}
  .legal-table td:first-child{color:var(--ink);font-weight:600;}
  .legal-scroll{overflow-x:auto;}
  .legal-id{display:grid;grid-template-columns:200px 1fr;border:1px solid var(--line);margin:0 0 22px;}
  .legal-id div{padding:11px 14px;border-bottom:1px solid var(--line);font-size:14.5px;line-height:1.55;}
  .legal-id div:nth-last-child(-n+2){border-bottom:0;}
  .legal-id .k{background:var(--cream-2);font-family:'JetBrains Mono',monospace;font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink);font-weight:600;}
  .legal-id .v{color:var(--ink-soft);}
  .todo{background:#ffe66d;color:#14110e;padding:0 4px;font-weight:600;}
  @media (max-width:700px){.legal-id{grid-template-columns:1fr;}.legal-id .k{border-bottom:0;padding-bottom:2px;}.legal-id .v{padding-top:2px;}}
'''
def page(fn,title,desc,eyebrow,h1,intro,body,lang_href):
    h=head
    h=re.sub(r'<title>.*?</title>','<title>%s</title>'%title,h,1,flags=re.S)
    h=re.sub(r'(<meta name="description" content=")[^"]*(")',r'\g<1>%s\g<2>'%desc,h,1)
    h=h.replace('</style>',CSS+'</style>',1)
    h=re.sub(r'<link rel="alternate" hreflang="es" href="[^"]*">\n<link rel="alternate" hreflang="en" href="[^"]*">','<link rel="alternate" hreflang="es" href="%s">\n<link rel="alternate" hreflang="en" href="%s">'%(fn,lang_href),h)
    h=h.replace('en/contact.html',lang_href)
    h=h.replace('<a href="rocheltex-contacto.html">Contacto</a>','<a href="rocheltex-contacto.html">Contacto</a>')
    mid='''<section class="intro-band">
  <div class="wrap">
    <div class="eyebrow">%s</div>
    <h1>%s</h1>
    <p>%s</p>
  </div>
</section>

<section class="legal">
  <div class="wrap legal-body">
%s
  </div>
</section>

'''%(eyebrow,h1,intro,body)
    open(R+fn,'w',encoding='utf-8').write(h+mid+tail)
T=lambda s:'<span class="todo">%s</span>'%s
ID='''    <div class="legal-id">
      <div class="k">Titular</div><div class="v">Rocheltex, S.L.</div>
      <div class="k">NIF</div><div class="v">%s</div>
      <div class="k">Domicilio social</div><div class="v">Pol. Ind. Serrans II, s/n · 46812 Aielo de Malferit (Valencia), España</div>
      <div class="k">Correo electrónico</div><div class="v"><a href="mailto:jss@rocheltex.es">jss@rocheltex.es</a></div>
      <div class="k">Teléfono</div><div class="v"><a href="tel:+34962904384">+34 96 290 43 84</a></div>
      <div class="k">Registro Mercantil</div><div class="v">Registro Mercantil de Valencia — %s</div>
    </div>'''%(T('B96120159 [verificar]'),T('Tomo [__], Folio [__], Hoja [__], Inscripción [__]'))
# ---------------- AVISO LEGAL
aviso='''    <p class="meta">Última actualización: %s</p>
    <h2>1. Datos identificativos del titular</h2>
    <p>En cumplimiento del artículo 10 de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de que el titular de este sitio web (el «Sitio Web») es:</p>
%s
    <p>Dirección del Sitio Web: %s.</p>

    <h2>2. Objeto</h2>
    <p>El Sitio Web tiene por finalidad ofrecer información corporativa y comercial sobre Rocheltex, S.L. («Rocheltex»), empresa dedicada a la fabricación de fibra textil regenerada (borra) para los sectores de automoción, geotextiles, hilatura y punzonado, así como sobre sus productos, procesos, certificaciones y compromisos, y facilitar el contacto con la empresa.</p>

    <h2>3. Condiciones de acceso y uso</h2>
    <p>El acceso al Sitio Web es libre y gratuito. La navegación por el Sitio Web atribuye la condición de usuario e implica la aceptación plena de este Aviso Legal. El usuario se compromete a utilizar el Sitio Web, sus contenidos y servicios de conformidad con la ley, la buena fe, el orden público y el presente Aviso Legal, y a abstenerse de:</p>
    <ul>
      <li>realizar actividades ilícitas, contrarias a la buena fe o lesivas de derechos o intereses de Rocheltex o de terceros;</li>
      <li>introducir o difundir virus informáticos u otros sistemas capaces de dañar o inutilizar el Sitio Web o los equipos de terceros;</li>
      <li>intentar acceder a áreas restringidas, alterar el funcionamiento del Sitio Web o extraer sus contenidos de forma masiva o automatizada sin autorización.</li>
    </ul>

    <h2>4. Propiedad intelectual e industrial</h2>
    <p>Los contenidos del Sitio Web (textos, fotografías, vídeos, gráficos, diseño, código, estructura) y los signos distintivos, incluidos el nombre comercial, la marca y el logotipo de Rocheltex, son titularidad de Rocheltex o de terceros que han autorizado su uso, y están protegidos por la normativa de propiedad intelectual e industrial.</p>
    <p>Queda prohibida su reproducción, distribución, comunicación pública, transformación o cualquier otro uso sin autorización expresa y por escrito de Rocheltex, salvo para uso personal y no comercial. Los logotipos de certificaciones y normas (por ejemplo, ISO, IATF, VDA QMC) pertenecen a sus respectivos titulares y se muestran únicamente para acreditar las certificaciones de Rocheltex.</p>

    <h2>5. Exclusión de garantías y responsabilidad</h2>
    <p>Rocheltex se esfuerza por mantener actualizada la información del Sitio Web, pero no garantiza la ausencia de errores ni su disponibilidad continuada. La información sobre productos, composiciones, capacidades y certificaciones tiene carácter informativo; las especificaciones técnicas, la disponibilidad y las condiciones comerciales aplicables se confirman en cada oferta o contrato.</p>
    <p>Rocheltex no será responsable de los daños derivados del uso del Sitio Web, de interrupciones del servicio, de fallos técnicos, ni del contenido y disponibilidad de sitios web de terceros a los que pueda enlazar el Sitio Web.</p>

    <h2>6. Enlaces</h2>
    <p>El Sitio Web puede contener enlaces a sitios de terceros con fines informativos. Rocheltex no controla ni se responsabiliza de su contenido ni de sus políticas. Quien desee establecer un enlace al Sitio Web deberá dirigirse a la página principal, sin falsear su procedencia ni sugerir una relación con Rocheltex que no exista.</p>

    <h2>7. Protección de datos y cookies</h2>
    <p>El tratamiento de los datos personales se rige por la <a href="rocheltex-privacidad.html">Política de privacidad</a>. El uso de cookies y tecnologías similares se describe en la <a href="rocheltex-cookies.html">Política de cookies</a>.</p>

    <h2>8. Modificaciones</h2>
    <p>Rocheltex se reserva el derecho de modificar este Aviso Legal y los contenidos del Sitio Web en cualquier momento, sin necesidad de previo aviso. Se recomienda revisarlo periódicamente.</p>

    <h2>9. Legislación aplicable y jurisdicción</h2>
    <p>Este Aviso Legal se rige por la legislación española. Para cualquier controversia relacionada con el Sitio Web, las partes se someten a los juzgados y tribunales de Valencia, salvo que la normativa aplicable establezca otro fuero.</p>'''%(T('[fecha]'),ID,T('[dominio definitivo, p. ej. www.rocheltex.com]'))
page('rocheltex-aviso-legal.html','Aviso legal — Rocheltex','Aviso legal de Rocheltex, S.L.: titular del sitio web, condiciones de uso, propiedad intelectual y legislación aplicable.','Legal','Aviso legal','Información sobre el titular del sitio web y las condiciones de uso, conforme a la LSSI-CE.',aviso,'en/legal-notice.html')
# ---------------- PRIVACIDAD
priv='''    <p class="meta">Última actualización: %s</p>
    <h2>1. Responsable del tratamiento</h2>
    <p>El responsable del tratamiento de tus datos personales es:</p>
%s
    <p>Puedes contactar con nosotros para cualquier cuestión sobre protección de datos en <a href="mailto:jss@rocheltex.es">jss@rocheltex.es</a>.</p>

    <h2>2. Qué datos tratamos y de dónde proceden</h2>
    <p>Tratamos los datos que nos facilitas directamente al usar el formulario de contacto o al escribirnos o llamarnos: nombre, empresa, correo electrónico, teléfono, sector de actividad y el contenido de tu mensaje. Si los datos pertenecen a un tercero, declaras contar con su autorización para facilitarlos.</p>
    <p>Además, el servidor que aloja el Sitio Web puede registrar datos técnicos de conexión (como la dirección IP y la fecha y hora de acceso) por razones de seguridad y funcionamiento. Este Sitio Web no utiliza cookies de analítica ni de publicidad.</p>

    <h2>3. Finalidades y base jurídica</h2>
    <div class="legal-scroll"><table class="legal-table">
      <thead><tr><th>Finalidad</th><th>Base jurídica</th></tr></thead>
      <tbody>
        <tr><td>Atender las consultas, solicitudes de información y peticiones de oferta recibidas a través del formulario, el correo electrónico o el teléfono.</td><td>Tu consentimiento (art. 6.1.a RGPD) y la aplicación de medidas precontractuales a petición tuya (art. 6.1.b RGPD).</td></tr>
        <tr><td>Gestionar la relación comercial y profesional con clientes, proveedores y contactos de empresa.</td><td>Ejecución del contrato o medidas precontractuales (art. 6.1.b) e interés legítimo en mantener la relación comercial (art. 6.1.f).</td></tr>
        <tr><td>Cumplir las obligaciones legales aplicables (fiscales, contables y otras).</td><td>Obligación legal (art. 6.1.c RGPD).</td></tr>
        <tr><td>Garantizar la seguridad y el correcto funcionamiento del Sitio Web.</td><td>Interés legítimo (art. 6.1.f RGPD).</td></tr>
      </tbody>
    </table></div>
    <p>No adoptamos decisiones automatizadas ni elaboramos perfiles a partir de tus datos.</p>

    <h2>4. Plazo de conservación</h2>
    <p>Conservaremos tus datos durante el tiempo necesario para atender tu consulta y, en su caso, mientras dure la relación comercial. Después, se mantendrán debidamente bloqueados durante los plazos de prescripción de las responsabilidades legales que pudieran derivarse, y se suprimirán una vez transcurridos.</p>

    <h2>5. Destinatarios y transferencias internacionales</h2>
    <p>No cederemos tus datos a terceros, salvo obligación legal (por ejemplo, a Administraciones Públicas, jueces y tribunales). Podrán acceder a ellos proveedores de servicios tecnológicos (alojamiento web, correo electrónico y mantenimiento) que actúan como encargados del tratamiento bajo contrato conforme al art. 28 del RGPD.</p>
    <p>Con carácter general no realizamos transferencias de datos fuera del Espacio Económico Europeo. Si algún proveedor estuviera ubicado fuera de él, la transferencia se amparará en una decisión de adecuación de la Comisión Europea o en cláusulas contractuales tipo. Si aceptas cargar el mapa de Google en la página de Contacto, Google LLC podrá tratar datos de tu navegación conforme a su <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">política de privacidad</a>.</p>

    <h2>6. Tus derechos</h2>
    <p>Puedes ejercer los derechos de <strong>acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad</strong>, así como retirar en cualquier momento el consentimiento prestado (sin que ello afecte a la licitud del tratamiento previo), escribiendo a <a href="mailto:jss@rocheltex.es">jss@rocheltex.es</a> e indicando el derecho que deseas ejercer. Podemos solicitarte una copia de un documento que acredite tu identidad.</p>
    <p>Responderemos en el plazo máximo de un mes. Si consideras que tus derechos no han sido atendidos correctamente, puedes presentar una reclamación ante la Agencia Española de Protección de Datos (<a href="https://www.aepd.es" target="_blank" rel="noopener noreferrer">www.aepd.es</a>).</p>

    <h2>7. Seguridad</h2>
    <p>Aplicamos medidas técnicas y organizativas adecuadas para proteger tus datos frente a accesos no autorizados, pérdida o alteración, de acuerdo con el nivel de riesgo.</p>

    <h2>8. Menores de edad</h2>
    <p>Este Sitio Web no está dirigido a menores de 14 años. Si tienes conocimiento de que un menor nos ha facilitado datos sin autorización de sus representantes legales, escríbenos para que los eliminemos.</p>

    <h2>9. Modificaciones de esta política</h2>
    <p>Podemos actualizar esta Política de privacidad para adaptarla a cambios legales o de funcionamiento. La versión vigente es la publicada en esta página, con su fecha de actualización.</p>'''%(T('[fecha]'),ID)
page('rocheltex-privacidad.html','Política de privacidad — Rocheltex','Política de privacidad de Rocheltex, S.L.: responsable, finalidades, base jurídica, conservación, destinatarios y derechos (RGPD y LOPDGDD).','Legal','Política de privacidad','Cómo tratamos tus datos personales, conforme al Reglamento (UE) 2016/679 (RGPD) y a la Ley Orgánica 3/2018 (LOPDGDD).',priv,'en/privacy-policy.html')
# ---------------- COOKIES
cook='''    <p class="meta">Última actualización: %s</p>
    <h2>1. ¿Qué son las cookies?</h2>
    <p>Las cookies y tecnologías similares (como el almacenamiento local del navegador) son pequeños archivos o datos que un sitio web guarda en tu dispositivo para que funcione, recordar tus preferencias o, en su caso, analizar el uso o mostrar publicidad. Esta política se ha elaborado conforme al artículo 22.2 de la LSSI-CE y a la guía de la Agencia Española de Protección de Datos.</p>

    <h2>2. Qué utilizamos en este sitio web</h2>
    <p>Este Sitio Web <strong>no utiliza cookies de analítica, de publicidad ni de perfilado</strong>, y las tipografías se sirven desde nuestro propio servidor. Únicamente utiliza:</p>
    <div class="legal-scroll"><table class="legal-table">
      <thead><tr><th>Nombre</th><th>Titular</th><th>Finalidad</th><th>Duración</th><th>Tipo</th></tr></thead>
      <tbody>
        <tr><td>rtx_consent_v1 (almacenamiento local)</td><td>Propia</td><td>Guardar tu decisión sobre cookies para no volver a preguntarte.</td><td>12 meses</td><td>Técnica, necesaria (no requiere consentimiento)</td></tr>
        <tr><td>Cookies de Google Maps</td><td>Google LLC (tercero)</td><td>Mostrar el mapa interactivo de la página de Contacto. Solo se cargan si aceptas «Contenido de terceros».</td><td>Según Google</td><td>De terceros, previo consentimiento</td></tr>
      </tbody>
    </table></div>
    <p>Mientras no aceptes el contenido de terceros, el mapa no se carga y Google no recibe ningún dato tuyo. En su lugar se muestra un enlace para abrir la ubicación directamente en Google Maps. Más información sobre las cookies de Google en <a href="https://policies.google.com/technologies/cookies" target="_blank" rel="noopener noreferrer">policies.google.com/technologies/cookies</a>.</p>

    <h2>3. Cómo gestionar tus preferencias</h2>
    <p>La primera vez que visitas el Sitio Web te mostramos un aviso con las opciones <strong>Aceptar todo</strong>, <strong>Rechazar todo</strong> y <strong>Configurar</strong>; rechazar es tan sencillo como aceptar. Puedes cambiar o retirar tu consentimiento en cualquier momento con el enlace «Configurar cookies» del pie de página: <button type="button" class="link-btn" style="appearance:none;background:none;border:0;padding:0;font:inherit;cursor:pointer;color:var(--red);text-decoration:underline;font-weight:600" data-open-cookies>Configurar cookies</button>.</p>
    <p>También puedes bloquear o eliminar cookies desde la configuración de tu navegador:</p>
    <ul>
      <li><a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener noreferrer">Google Chrome</a></li>
      <li><a href="https://support.mozilla.org/es/kb/habilitar-y-deshabilitar-cookies-sitios-web-rastrear-preferencias" target="_blank" rel="noopener noreferrer">Mozilla Firefox</a></li>
      <li><a href="https://support.apple.com/es-es/guide/safari/sfri11471/mac" target="_blank" rel="noopener noreferrer">Safari</a></li>
      <li><a href="https://support.microsoft.com/es-es/microsoft-edge/eliminar-las-cookies-en-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09" target="_blank" rel="noopener noreferrer">Microsoft Edge</a></li>
    </ul>

    <h2>4. Más información y actualizaciones</h2>
    <p>Para saber cómo tratamos tus datos personales consulta la <a href="rocheltex-privacidad.html">Política de privacidad</a>. Podemos actualizar esta política si cambian las cookies que utilizamos; la versión vigente es la publicada en esta página.</p>'''%(T('[fecha]'))
page('rocheltex-cookies.html','Política de cookies — Rocheltex','Política de cookies de Rocheltex, S.L.: qué cookies usa el sitio web, para qué y cómo gestionarlas.','Legal','Política de cookies','Qué almacenamiento utilizamos en este sitio web, para qué sirve y cómo puedes gestionarlo.',cook,'en/cookie-policy.html')
print('ok')
