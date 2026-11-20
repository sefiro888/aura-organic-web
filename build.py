"""Generador de la web de AURA Organic Salón (v3). Ejecutar: python build.py"""
from pathlib import Path
from html import escape as e
import json
from content import SERVICES, PA, GOOGLE, INSTAGRAM, FACEBOOK

ROOT = Path(__file__).parent
OUT = ROOT / 'dist'
ORIGIN = 'https://aura-organic-sauzal.sefiro888.chatgpt.site'
TEL = '+34642636970'


def ig(code, kind='p'):
    return f'https://www.instagram.com/{kind}/{code}/'


# ───────────── imágenes ─────────────
def img(name, alt, cls='', eager=False, style=''):
    a = f' class="{cls}"' if cls else ''
    s = f' style="{style}"' if style else ''
    load = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"'
    return f'<img{a}{s} src="assets/img/{name}.webp" alt="{e(alt)}"{load} decoding="async">'


# (archivo, título, categoría, fuente)
GALLERY = [
    ('balayage', 'Balayage con ondas suaves', 'Color', ig('DTylPUPjEwq')),
    ('recogido-1', 'Recogido bajo con textura', 'Novias', ig('DfQGH5pA6AN')),
    ('letrero-ondas', 'Ondas con brillo junto al letrero AURA', 'Peinados', ig('DYqX4A8R3pU')),
    ('novia-1', 'Novia con peinado y maquillaje', 'Novias', ig('DezpExfjv0U')),
    ('largo-reflejos', 'Melena larga con reflejos', 'Color', ig('DcGdB7_AtnT')),
    ('planta-1', 'Verde y calidez en el salón', 'Salón', ig('DQh2x_2DOBb')),
    ('real-12', 'Manicura en rosa vibrante', 'Estética', PA),
    ('recogido-trenza', 'Torsiones y acabado pulido', 'Novias', ig('DfQFvxCgYAS')),
    ('bob-miel', 'Bob con reflejos miel', 'Color', ig('DTykg7pjMlB')),
    ('arkhe-expositor', 'Expositor de cuidado capilar Arkhē', 'Productos', ig('DegxbahAvfA')),
    ('semirrecogido', 'Semirrecogido con ondas', 'Peinados', ig('DcGc34pgHhf')),
    ('equipo', 'El equipo de AURA', 'Salón', ig('DefN9xpgI5v')),
    ('rubio-rizos', 'Rubio con rizos amplios', 'Color', ig('DTyleRyDBx2')),
    ('recogido-2', 'Recogido con ondas sueltas', 'Novias', ig('DcoFSPGApCI')),
    ('real-05', 'Cuidado de manos', 'Estética', PA),
    ('liso-oscuro', 'Liso largo con brillo', 'Peinados', ig('DTykx7EDOtq')),
    ('letrero-1', 'El letrero de AURA', 'Salón', ig('DNJH39UIxCc')),
    ('opi-repair', 'Esmaltes y cuidado de uñas OPI', 'Estética', ig('DKSFMisIloM')),
    ('invitada-sombrero', 'Preparando a una invitada con tocado', 'Novias', ig('DexXXegABF6')),
    ('ondas-castano', 'Ondas castañas con reflejos', 'Color', ig('DTylYJ-DIQM')),
    ('olaplex', 'Tratamientos Olaplex', 'Productos', ig('DQh0mKAgCrJ')),
    ('cobrizo', 'Cobre intenso y brillo', 'Color', ig('DVv48tkDMAz')),
    ('salon-estanteria', 'Estantería de producto profesional', 'Salón', ig('DQh1y42AFtI')),
    ('novia-maquillaje', 'Maquillaje de novia', 'Novias', ig('DexQTkgAitJ')),
    ('moreno-liso', 'Moreno liso y luminoso', 'Peinados', ig('DeJy_5UjmiU')),
    ('real-06', 'Color para las uñas', 'Estética', PA),
    ('corte-pixie', 'Corte corto con reflejos', 'Peinados', ig('DYff4OQiaFm')),
    ('aniversario-arco', 'Celebrando dos años de AURA', 'Salón', ig('DGqkEoDom6-')),
]

PAIRS = {
    'ondulado-liso': 'De ondas a un liso largo y brillante',
    'bob-miel': 'Un bob con reflejos miel',
    'rizos': 'Rizos con matiz y definición',
    'reflejos': 'Reflejos dorados con volumen',
    'rubio-raiz': 'Del cobre a un rubio dorado',
    'azul-negro': 'Negro azulado, liso y con brillo',
    'rubio-claro': 'Un rubio claro más uniforme',
    'capas': 'De castaño a rubio platino con capas',
    'castano': 'Un bob castaño con reflejos caramelo',
    'fantasia': 'De mechas desiguales a un bob uniforme',
    'castano-rojizo': 'Brillo cobrizo y suavidad',
    'corto': 'Un corte corto con reflejos rubios',
}

CARD = {'peluqueria': 'largo-reflejos', 'coloracion': 'ritual-color', 'rubios': 'rubio-rizos',
        'keratina': 'liso-oscuro', 'estetica': 'real-12', 'novias': 'novia-1'}

HERO = {  # slug: (posición del fondo, arco grande, arco pequeño)
    'index': ('62% 40%', 'letrero-liso', 'balayage'),
    'servicios': ('50% 40%', 'ritual-color', 'real-12'),
    'peluqueria': ('40% 50%', 'letrero-ondas', 'bob-miel'),
    'coloracion': ('58% 40%', 'ritual-color', 'cobrizo'),
    'rubios': ('70% 30%', 'rubio-rizos', 'balayage'),
    'keratina': ('30% 50%', 'liso-oscuro', 'letrero-liso'),
    'estetica': ('80% 60%', 'real-12', 'real-06'),
    'novias': ('68% 20%', 'novia-1', 'recogido-1'),
    'salon': ('50% 50%', 'equipo', 'letrero-1'),
    'galeria': ('60% 30%', 'recogido-2', 'balayage'),
    'cuidados': ('45% 60%', 'arkhe-producto', 'olaplex'),
    'contacto': ('55% 40%', 'fachada-clienta-2', 'real-13'),
    'informacion': ('50% 50%', 'letrero-1', None),
    '404': ('50% 50%', 'letrero-2', None),
}

PAGE_MEDIA = {  # fotos de apoyo por servicio: secciones (2), trabajos, antes/después
    'peluqueria': dict(sec=['largo-reflejos', 'bob-miel'], works=['corte-pixie', 'bob-rubio', 'castano-claro'],
                       pairs=['bob-miel', 'corto', 'fantasia', 'reflejos']),
    'coloracion': dict(sec=['cobrizo', 'rubio-capas'], works=['balayage', 'ondas-castano', 'moreno-liso'],
                       pairs=['castano', 'castano-rojizo', 'fantasia', 'capas', 'rubio-raiz']),
    'rubios': dict(sec=['rubio-ondas', 'bob-rubio'], works=['rubio-capas', 'largo-reflejos', 'rubio-rizos'],
                   pairs=['rubio-raiz', 'rubio-claro', 'capas', 'reflejos']),
    'keratina': dict(sec=['letrero-liso', 'keratina-bk'], works=['moreno-liso', 'alisado-hialuronico', 'liso-oscuro'],
                     pairs=['ondulado-liso', 'azul-negro', 'castano-rojizo']),
    'estetica': dict(sec=['opi-repair', 'unas-puesto'], works=['real-12', 'real-05', 'real-06'], pairs=[]),
    'novias': dict(sec=['recogido-1', 'recogido-trenza'],
                   works=['recogido-2', 'novia-maquillaje', 'invitada-sombrero', 'trenza-corta', 'semirrecogido'], pairs=[]),
}
WORK_SRC = {k: s for k, t, c, s in [(g[0], g[1], g[2], g[3]) for g in GALLERY]}
WORK_TITLE = {g[0]: g[1] for g in GALLERY}


# ───────────── piezas ─────────────
def kicker(t):
    return f'<p class="eyebrow">{t}</p>'


def book(label='Pedir mi cita', service='', cls='btn'):
    return f'<button class="{cls}" data-book="{e(service)}">{label}</button>'


def link(slug, label, cls='link'):
    return f'<a class="{cls}" href="{slug}.html">{label} <span aria-hidden="true">→</span></a>'


def ext(url, label, cls='link'):
    return f'<a class="{cls}" href="{url}" target="_blank" rel="noopener">{label} <span aria-hidden="true">↗</span></a>'


def lines(title, i0=0):
    parts = [x[:1] + x[1:].lower() if x.isupper() else x for x in title.split('\n')]
    out = ''
    for i, p in enumerate(parts):
        inner = f'<em>{p}</em>' if (i == len(parts) - 1 and len(parts) > 1) else p
        out += f'<span class="ln"><span style="--i:{i + i0}">{inner}</span></span>'
    return out


def seal():
    return ('<div class="seal" aria-hidden="true"><svg viewBox="0 0 180 180"><defs><path id="sp" d="M90,90 m-66,0 a66,66 0 1,1 132,0 a66,66 0 1,1 -132,0"/></defs>'
            '<circle cx="90" cy="90" r="86"/><circle cx="90" cy="90" r="50"/><text><textPath href="#sp" textLength="408">BELLEZA CON RAÍCES · AURA · EL SAUZAL · </textPath></text>'
            '<path class="lotus" d="M90 124C58 106 66 78 90 56c24 22 32 50 0 68Zm0 0c-44-9-40-40-34-50 27 8 40 30 34 50Zm0 0c44-9 40-40 34-50-27 8-40 30-34 50Z"/></svg></div>')


def petals():
    spec = [(8, 14, 17, 0), (19, 10, 21, 3), (31, 16, 15, 6), (44, 11, 19, 1), (57, 13, 23, 9), (68, 9, 18, 4), (79, 15, 20, 11), (90, 12, 16, 7), (96, 10, 24, 2)]
    return '<div class="petals" aria-hidden="true">' + ''.join(f'<i style="--x:{x}%;--s:{s}px;--t:{t}s;--d:-{d}s"></i>' for x, s, t, d in spec) + '</div>'


def hero(slug, eyebrow, title, intro, crumb=None, chips=(), cta=True, big=False, extra=''):
    pos, a1, a2 = HERO[slug]
    svc = SERVICES.get(slug, {}).get('title', '')
    crumbs = f'<nav class="crumbs" aria-label="Migas de pan"><a href="index.html">Inicio</a><span>/</span><span>{crumb}</span></nav>' if crumb else ''
    chip_html = '<div class="hero-chips">' + ''.join(f'<span>{c}</span>' for c in chips) + '</div>' if chips else ''
    act = f'<div class="actions">{book("Pedir mi cita", svc)}<a class="link" href="#descubrir">Descubrir más <span aria-hidden="true">↓</span></a></div>' if cta else ''
    arches = ''
    if a1:
        arches += f'<div class="arch ghost" aria-hidden="true"></div><figure class="arch a1">{img(a1, "Trabajo real de AURA Organic Salón", eager=True)}</figure>'
    if a2:
        arches += f'<figure class="arch a2">{img(a2, "Detalle de un trabajo de AURA", eager=True)}</figure>'
    side = f'<div class="hero-arches">{arches}{seal() if big else ""}</div>' if a1 else '<div></div>'
    cls = 'hero hero--home' if big else 'hero hero--sub'
    return (f'<section class="{cls}" style="--bgpos:{pos}"><div class="hero-bg"><img src="assets/img/ambiente-hero.webp" alt="" fetchpriority="high" decoding="async"></div>'
            f'<div class="hero-veil"></div><div class="hero-light"></div>{petals()}'
            f'<div class="wrap hero-grid"><div class="hero-copy">{crumbs}{kicker(eyebrow)}<h1>{lines(title)}</h1><p class="intro">{intro}</p>{act}{chip_html}{extra}</div>{side}</div>'
            f'<a class="scroll-cue" href="#descubrir" aria-label="Seguir bajando"><span>Descubrir</span><i></i></a></section>')


def header(active):
    nav = [('index', 'Inicio'), ('servicios', 'Servicios'), ('novias', 'Novias'), ('salon', 'El salón'), ('galeria', 'Galería'), ('contacto', 'Contacto')]
    items = ''.join(f'<a href="{s}.html"' + (' aria-current="page"' if active == s else '') + f'>{t}</a>' for s, t in nav)
    mega = ''.join(f'<a href="{s}.html">{img(CARD[s], v["title"])}<span>{v["short"]}</span></a>' for s, v in SERVICES.items())
    msub = ''.join('<a href="' + k + '.html">' + v['short'] + '</a>' for k, v in SERVICES.items())
    phone = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>'
    return (f'<a class="skip" href="#contenido">Saltar al contenido</a>'
            f'<header class="header"><div class="header-in"><a href="index.html" class="brand" aria-label="AURA Organic Salón, inicio"><img src="assets/img/logo.webp" alt="" width="56" height="56"><span>AURA<small>ORGANIC SALÓN</small></span></a>'
            f'<nav class="desktop-nav" aria-label="Navegación principal">{items}</nav>'
            f'<div class="header-actions"><a class="header-phone" href="tel:{TEL}">{phone}642 63 69 70</a>{book("Tu momento AURA")}<button class="menu-toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span></button></div></div></header>'
            f'<div class="mobile-menu" id="mobile-menu" hidden><nav aria-label="Navegación móvil">{items}</nav><div class="mobile-sub">{msub}<a href="cuidados.html">Cuidado en casa</a></div><a class="btn" href="tel:{TEL}">Llamar · 642 63 69 70</a></div>'
            f'<div class="service-menu" id="service-menu"><div class="wrap"><div>{kicker("Elige cómo cuidarte")}<h2>Un cuidado<br><em>muy tuyo.</em></h2>{link("servicios", "Todos los servicios")}</div><div class="mega-grid">{mega}</div></div></div><div class="reading-progress" aria-hidden="true"></div>')


def closing():
    return (f'<section class="closing"><img src="assets/img/ambiente-logo.webp" alt="" loading="lazy"><div class="wrap"><div class="closing-copy reveal">{kicker("Hay un momento que es solo tuyo")}'
            f'<h2>Hazte<br><em>un hueco.</em></h2><p>Cuéntanos qué necesitas. Nosotras ponemos el tiempo, las manos y el cuidado.</p><div class="actions">{book("Encontrar mi momento")}'
            f'<a class="btn btn--ghost" href="https://wa.me/34642636970" target="_blank" rel="noopener">WhatsApp</a></div></div></div></section>')


def footer():
    wa = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M20 11.5a8 8 0 0 1-11.6 7.2L4 20l1.3-4.4A8 8 0 1 1 20 11.5Z"/><path d="M9 8c0 4 3 7 7 7l1-2-3-1-1 1-2-2 1-1-1-3Z"/></svg>'
    opts = ''.join('<option>' + v['title'] + '</option>' for v in SERVICES.values())
    svc = ''.join(f'<a href="{s}.html">{v["short"]}</a>' for s, v in SERVICES.items())
    return (closing() +
            f'<footer><div class="wrap"><div class="footer-main"><div><p>Peluquería y estética unisex<br>con una mirada más natural.</p></div>'
            f'<div><h3>Servicios</h3>{svc}</div>'
            f'<div><h3>Ven a conocernos</h3><span>Av. Inmaculada Concepción, 42<br>38360 El Sauzal · Tenerife</span><a href="{GOOGLE}" target="_blank" rel="noopener">Cómo llegar ↗</a><a href="tel:{TEL}">642 63 69 70</a><a href="mailto:auraesteticasauzal@gmail.com">Escríbenos</a></div>'
            f'<div><h3>Sigue el día a día</h3><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram ↗</a><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook ↗</a><a href="galeria.html">Galería</a><a href="cuidados.html">Cuidado en casa</a><a href="contacto.html">Organiza tu visita</a></div></div>'
            f'<div class="footer-mark" aria-hidden="true">AURA</div>'
            f'<div class="footer-bottom"><span>© 2026 AURA Organic Salón</span><span>BELLEZA CON RAÍCES · EL SAUZAL</span><a href="informacion.html">Información y privacidad</a></div></div></footer>'
            f'<a class="whatsapp-float" href="https://wa.me/34642636970?text=Hola%20AURA%2C%20me%20gustar%C3%ADa%20pedir%20cita." target="_blank" rel="noopener" aria-label="Pedir cita por WhatsApp">{wa}<span>Hablemos</span></a>'
            f'<div class="mobile-dock"><a href="tel:{TEL}">Llamar</a>{book("Pedir cita", "", "")}<a href="{GOOGLE}" target="_blank" rel="noopener">Ruta</a></div>'
            f'<dialog id="booking" aria-labelledby="booking-title"><button class="dialog-close" data-close aria-label="Cerrar solicitud">×</button><div class="booking-head">{kicker("Tu momento empieza aquí")}<h2 id="booking-title">¿Qué te apetece<br><em>hacer por ti?</em></h2><p>Prepara tu mensaje. El equipo confirmará disponibilidad, hora y presupuesto por WhatsApp.</p></div>'
            f'<form id="booking-form"><label>Me gustaría…<select name="service" required><option value="">Elegir un servicio</option><option>Asesoramiento personalizado</option>{opts}<option>Corte y peinado</option><option>Manicura y pedicura</option><option>Maquillaje</option><option>Depilación con hilo</option><option>Depilación láser</option><option>Presoterapia</option><option>Cuidado facial o corporal</option></select></label>'
            f'<div class="form-row"><label>Tu nombre<input name="name" autocomplete="given-name" maxlength="70" placeholder="¿Cómo te llamas?" required></label><label>Día preferido<input type="date" name="date"></label></div>'
            f'<label>Te viene mejor<select name="time"><option>Cualquier franja</option><option>Por la mañana</option><option>Por la tarde</option></select></label>'
            f'<label>Algo que quieras contarnos<textarea name="notes" rows="2" maxlength="600" placeholder="Tu idea, la fecha del evento, una duda…"></textarea></label>'
            f'<p class="form-note">Esta solicitud no reserva automáticamente. Los datos se incorporan al mensaje de WhatsApp y no se guardan en esta web.</p><button class="btn" type="submit">Preparar mi mensaje</button>'
            f'<div class="message-preview" hidden><p>Tu mensaje está listo:</p><pre id="message-text"></pre><a class="btn" id="send-whatsapp" target="_blank" rel="noopener">Abrir WhatsApp</a><p class="form-note">Revisa el texto y envíalo tú desde WhatsApp.</p></div></form></dialog>'
            f'<dialog id="lightbox" class="lightbox" aria-label="Fotografía ampliada"><button class="dialog-close" data-close aria-label="Cerrar fotografía">×</button><button class="lightbox-prev" aria-label="Foto anterior">‹</button><figure><img src="assets/img/equipo.webp" alt=""><figcaption><span id="lightbox-caption"></span><a id="lightbox-source" target="_blank" rel="noopener">Ver publicación original</a></figcaption></figure><button class="lightbox-next" aria-label="Foto siguiente">›</button></dialog>')


def page(slug, title, desc, body):
    schema = {'@context': 'https://schema.org', '@type': 'HairSalon', 'name': 'AURA Organic Salón', 'telephone': TEL,
              'address': {'@type': 'PostalAddress', 'streetAddress': 'Av. Inmaculada Concepción, 42', 'addressLocality': 'El Sauzal', 'postalCode': '38360', 'addressRegion': 'Santa Cruz de Tenerife', 'addressCountry': 'ES'},
              'sameAs': [INSTAGRAM, FACEBOOK], 'image': ORIGIN + '/assets/img/equipo.webp'}
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#150b05">'
            f'<title>{e(title)} · AURA Organic Salón · El Sauzal</title><meta name="description" content="{e(desc)}"><meta property="og:title" content="{e(title)} · AURA"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">'
            f'<meta property="og:image" content="{ORIGIN}/assets/img/ambiente-logo.webp"><meta property="og:locale" content="es_ES"><link rel="icon" type="image/png" href="assets/img/favicon.png">'
            f'<link rel="preload" href="assets/fonts/cormorant.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script>'
            f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head><body data-page="{slug}">{header(slug)}<main id="contenido">{body}</main>{footer()}</body></html>')
    (OUT / f'{slug}.html').write_text(html, encoding='utf8')


def faqs(items, title='Hablemos\nclaro.', dark=False):
    a, b = title.split('\n')
    cls = 'section dark grain' if dark else 'section'
    return (f'<section class="{cls}" id="preguntas"><div class="wrap faq-grid"><div class="reveal">{kicker("Sin dudas, sin prisas")}<h2>{a}<br><em>{b}</em></h2><p style="margin-top:22px;max-width:30ch">Si hay algo más que quieras saber, estamos al otro lado.</p><div class="actions">{book("Preguntar al equipo", "", "link")}</div></div>'
            f'<div class="faqs">' + ''.join(f'<details class="reveal"><summary>{q}<span aria-hidden="true">+</span></summary><p>{a_}</p></details>' for q, a_ in items) + '</div></div></section>')


def transform(keys, head='Hay resultados<br>que <em>se ven.</em>', text='Desliza para comparar trabajos reales publicados por el salón. Cada cabello parte de un punto distinto y por eso cada propuesta se valora de forma personal.', dark=False, link_html=''):
    k0 = keys[0]
    thumbs = ''.join(f'<button type="button" data-pair="ba-{k}" data-label="{e(PAIRS[k])}" aria-pressed="{"true" if i == 0 else "false"}" aria-label="Ver: {e(PAIRS[k])}"><img src="assets/img/ba-{k}-despues.webp" alt="" loading="lazy"></button>' for i, k in enumerate(keys))
    cls = 'section pearl' if not dark else 'section dark grain'
    return (f'<section class="{cls} transformation" id="transformaciones"><div class="wrap tf-grid"><div class="reveal">'
            f'<div class="compare-frame" style="--split:50%"><img data-before src="assets/img/ba-{k0}-antes.webp" alt="Cabello antes del trabajo"><div class="compare-after"><img data-after src="assets/img/ba-{k0}-despues.webp" alt="Cabello después del trabajo"></div>'
            f'<div class="compare-line"><span>↔</span></div><span class="compare-tag before">Antes</span><span class="compare-tag after">Después</span>'
            f'<input id="compare" type="range" min="0" max="100" value="50" aria-label="Deslizar para comparar el antes y el después"></div></div>'
            f'<div class="tf-copy reveal" style="--d:.15s">{kicker("El cambio, a tu ritmo")}<h2>{head}</h2><p>{text}</p>'
            f'<div class="tf-thumbs" role="group" aria-label="Elegir trabajo">{thumbs}</div><p class="tf-caption" aria-live="polite">{e(PAIRS[k0])}</p>'
            f'<p class="muted" style="margin-top:14px">Fotografías reales de AURA con ángulos e iluminación distintos. Los resultados dependen de cada cabello.</p>{link_html}</div></div></section>')


def svc_cards(keys):
    out = ''
    for i, s in enumerate(keys):
        v = SERVICES[s]
        out += (f'<a class="svc reveal" style="--d:{(i % 3) * .12}s" href="{s}.html"><div class="ph">{img(CARD[s], v["title"])}<span class="num" aria-hidden="true">0{i + 1}</span></div>'
                f'<div class="cap"><small>{v["short"]}</small><h3>{v["title"]}</h3><p>{v["intro"][:112].rsplit(" ", 1)[0]}…</p></div></a>')
    return '<div class="svc-grid">' + out + '</div>'


def gallery(items, filters=True, cols=''):
    cats = ['Todo', 'Color', 'Peinados', 'Novias', 'Estética', 'Salón', 'Productos']
    tabs = ('<div class="gallery-filters" role="group" aria-label="Filtrar fotografías">' + ''.join(f'<button class="filter{" active" if t == "Todo" else ""}" data-filter="{t}" aria-pressed="{"true" if t == "Todo" else "false"}">{t}</button>' for t in cats) + '</div><p class="filter-status sr-only" aria-live="polite"></p>') if filters else ''
    figs = ''.join(f'<figure class="gallery-item reveal" data-category="{c}"><button class="gallery-open" data-image="assets/img/{im}.webp" data-caption="{e(t)}" data-source="{s}" aria-label="Ampliar: {e(t)}">{img(im, t)}<span class="zoom-icon" aria-hidden="true">+</span></button><figcaption>{t}<small>{c}</small></figcaption></figure>' for im, t, c, s in items)
    return tabs + f'<div class="gallery-grid">{figs}</div>'


def works(keys, five=False):
    figs = ''.join(f'<figure class="reveal" style="--d:{i * .08}s"><button class="gallery-open" data-image="assets/img/{k}.webp" data-caption="{e(WORK_TITLE.get(k, "Trabajo de AURA"))}" data-source="{WORK_SRC.get(k, INSTAGRAM)}" aria-label="Ampliar foto">{img(k, WORK_TITLE.get(k, "Trabajo de AURA"))}<span class="zoom-icon" aria-hidden="true">+</span></button></figure>' for i, k in enumerate(keys))
    return f'<div class="works{" five" if five else ""}">{figs}</div>'


def reviews():
    data = [('Conchi Cabello', 'Me encanta el trato y los productos orgánicos. Y no tardan en darte cita.', '5'),
            ('kali cabrera avila', 'Muy profesionales. Puntualidad, buen trato, te aconsejan y te dejan exactamente lo que tú quieres.', '4'),
            ('Noemí Perez diaz', 'Desde que llegué, el ambiente, el buen rollo y la atención hicieron que me sintiera súper cómoda.', '5')]
    cards = ''.join(f'<article class="review"><span class="stars" aria-label="{s} de 5 estrellas">{"★" * int(s)}{"☆" * (5 - int(s))}</span><blockquote>«{t}»</blockquote><div><strong>{n}</strong><span>Reseña de Google · extracto</span></div></article>' for n, t, s in data)
    return (f'<section class="section dark grain reviews"><div class="wrap"><div class="section-head reveal"><div>{kicker("Lo que se siente, se cuenta")}<h2>El cariño<br><em>de quienes vuelven.</em></h2></div>'
            f'<a class="google-score" href="{GOOGLE}" target="_blank" rel="noopener"><strong>4,8<span>/5</span></strong><div><span class="stars" aria-label="Valoración de Google">★★★★★</span><br><span>32 reseñas en Google</span></div></a></div>'
            f'<div class="review-track" tabindex="0" aria-label="Testimonios de Google">{cards}</div>'
            f'<div class="review-bottom"><p>Extractos visibles en Google el 20 de noviembre de 2026. La valoración puede cambiar.</p><div><button class="round-button" data-review="prev" aria-label="Reseña anterior">‹</button><button class="round-button" data-review="next" aria-label="Siguiente reseña">›</button></div></div></div></section>')


def ig_wall():
    wall = [('recogido-collage', ig('DffQEiTgNtk')), ('novia-1', ig('DezpExfjv0U')), ('arkhe-expositor', ig('DegxbahAvfA')), ('balayage', ig('DTylPUPjEwq')),
            ('equipo', ig('DefN9xpgI5v')), ('opi-jelly', ig('DKSFYKYIlI7')), ('largo-reflejos', ig('DcGdB7_AtnT')), ('aniversario-arco', ig('DGqkEoDom6-'))]
    cells = ''.join(f'<a class="reveal" style="--d:{(i % 4) * .08}s" href="{u}" target="_blank" rel="noopener" aria-label="Ver publicación en Instagram">{img(n, "Publicación de AURA en Instagram")}</a>' for i, (n, u) in enumerate(wall))
    return (f'<section class="section"><div class="wrap"><div class="section-head reveal"><div>{kicker("La vida en el salón")}<h2>Muy real.<br><em>Muy AURA.</em></h2></div><p>Cabello, manos, recogidos y el equipo que lo hace posible. Fotografías publicadas por el propio salón.</p></div>'
            f'<div class="ig-grid">{cells}</div><div class="ig-foot"><p class="muted">252 publicaciones · 277 seguidores en Instagram</p>{ext(INSTAGRAM, "@aurasalonsauzal", "btn btn--dark")}</div></div></section>')


# ───────────── portada ─────────────
def home():
    h = hero('index', 'Peluquería + estética unisex · El Sauzal, Tenerife', 'Belleza\ncon raíces.',
             'Tu pelo. Tu piel. Tu forma de ser. Un cuidado que empieza por escucharte y termina haciéndote sentir muy tú.', big=True,
             chips=('Sin amoniaco', 'Diagnóstico personalizado', 'Más de 20 años'),
             extra=f'<a class="rating" href="{GOOGLE}" target="_blank" rel="noopener"><b>4,8</b><span><span class="stars" aria-hidden="true">★★★★★</span><small>32 opiniones en Google</small></span></a>')
    tick = '<span>Tu belleza tiene carácter</span><b>✦</b><span>Y tu cuidado, raíces</span><b>✦</b><span>AURA Organic Salón</span><b>✦</b><span>Escuchamos primero</span><b>✦</b>'
    ticker = f'<div class="ticker" aria-hidden="true"><div>{tick * 3}</div></div>'
    manifesto = (f'<section class="section manifesto" id="descubrir"><div class="wrap"><div class="manifesto-grid"><div class="reveal">{kicker("Nuestra forma de mirar")}'
                 f'<h2>Tienes algo<br>que te hace<br><span class="out">diferente.</span></h2><p class="lead">Y eso es lo que queremos cuidar. Tu gesto, tu textura, tu manera de llevar el pelo. En AURA unimos técnica, productos profesionales y una atención que se toma su tiempo.</p>'
                 f'<div class="actions">{link("salon", "Conoce a tu equipo")}{book("Pedir mi cita", "", "btn")}</div></div>'
                 f'<div class="duo reveal" style="--d:.15s"><figure class="arch a1">{img("equipo", "Las tres profesionales de AURA Organic Salón")}</figure><figure class="arch a2">{img("letrero-1", "El letrero circular de AURA sobre los listones de madera")}</figure><p class="tag">«Tu pelo no es uno más.»</p></div></div>'
                 f'<div class="stats"><div><strong data-count="20">0<small>+</small></strong><span>Años de oficio</span></div><div><strong data-count="3">0</strong><span>Profesionales</span></div><div><strong data-count="4.8">0</strong><span>En Google · 32 reseñas</span></div><div><strong data-count="2">0</strong><span>Años de este sueño</span></div></div></div></section>')
    services = (f'<section class="section dark grain" id="rituales"><div class="wrap"><div class="section-head reveal"><div>{kicker("Elige tu próximo ritual")}<h2>¿Qué te<br><em>apetece sentir?</em></h2></div><p>El cuidado cambia contigo. Explora tu lado AURA.</p></div>{svc_cards(list(SERVICES))}<div class="svc-more">{link("servicios", "Toda nuestra carta")}</div></div></section>')
    tf = transform(['ondulado-liso', 'bob-miel', 'rubio-raiz', 'capas', 'azul-negro', 'rizos', 'castano-rojizo', 'fantasia'], link_html=f'<div class="actions">{link("galeria", "Ver más trabajos")}</div>')
    space = (f'<section class="section dark grain"><div class="wrap"><div class="text-two reveal"><div>{kicker("Un espacio con raíces")}<h2>Madera, verde<br><em>y buenas<br>conversaciones.</em></h2></div>'
             f'<div><p>Listones de nogal, plantas, luz cálida y un letrero que te da la bienvenida. Queremos que tu visita tenga algo de pausa y mucho de cuidado personal.</p><ul class="checks"><li>Salón unisex: todas las personas, identidades y edades.</li><li>Productos profesionales de marcas como Arkhē, Olaplex, OPI o Masglo.</li><li>Un diagnóstico antes de decidir: escuchamos y miramos tu cabello.</li></ul></div></div>'
             f'<div class="mosaic"><figure class="m1 reveal-img">{img("arkhe-expositor", "Expositor Arkhē entre listones de madera y plantas")}<figcaption>Madera y producto profesional</figcaption></figure>'
             f'<figure class="m2 reveal-img" style="--d:.1s">{img("letrero-2", "El letrero circular de AURA iluminado")}<figcaption>Tu bienvenida</figcaption></figure>'
             f'<figure class="m3 reveal-img" style="--d:.2s">{img("salon-estanteria", "Estantería con productos profesionales")}<figcaption>Producto profesional</figcaption></figure>'
             f'<figure class="m4 reveal-img" style="--d:.15s">{img("planta-1", "Monstera sobre una pared cálida del salón")}<figcaption>Un rincón verde</figcaption></figure>'
             f'<figure class="m5 reveal-img" style="--d:.25s">{img("lavado", "Una clienta en el lavacabezas con el espejo del salón al fondo")}<figcaption>Un momento de calma</figcaption></figure>'
             f'<figure class="m6 reveal-img" style="--d:.3s">{img("aniversario-arco", "Arco de globos en la fachada de AURA", style="object-position:50% 40%")}<figcaption>Dos años cumpliendo un sueño</figcaption></figure></div></div></section>')
    story = (f'<section class="story emerald grain"><div class="story-img reveal-img">{img("ritual-color", "Una profesional de AURA preparando el color en un cuenco de madera")}</div>'
             f'<div class="story-copy"><span class="watermark" aria-hidden="true">color</span><div class="reveal">{kicker("Color con intención")}<h2>Tu color.<br>Tu forma<br><em>de ser.</em></h2><p>Un reflejo que ilumina tu rostro. Un tono con el que te reconoces. Elegimos el color después de conocer tu cabello, tu historia y lo que buscas.</p>'
             f'<div class="tags"><span>Sin amoniaco</span><span>Diagnóstico personalizado</span><span>Balayage y rubios</span></div><div class="actions">{link("coloracion", "Encuentra tu color", "btn")}</div></div></div></section>')
    bridal = (f'<section class="section bridal pearl"><span class="watermark" aria-hidden="true">Sí, quiero</span><div class="wrap bridal-grid"><div class="trio reveal"><figure class="arch t1">{img("recogido-1", "Recogido bajo con textura")}</figure><figure class="arch t2">{img("novia-1", "Novia con peinado suelto y maquillaje")}</figure><figure class="arch t3">{img("recogido-trenza", "Recogido con torsiones")}</figure></div>'
              f'<div class="reveal" style="--d:.15s">{kicker("Novias + invitadas")}<h2>Ese día.<br><em>Tan tú.</em></h2><p style="margin-top:26px;max-width:46ch">Que el peinado acompañe tu sonrisa. Que el maquillaje siga hablando de ti. Preparamos los detalles, con prueba y con tiempo, para que tú te dediques a vivirlos.</p><div class="actions">{link("novias", "Vamos a preparar tu día", "btn btn--em")}</div></div></div></section>')
    brands = (f'<section class="section"><div class="wrap"><div class="section-head reveal"><div>{kicker("Marcas con criterio")}<h2>Lo que usamos,<br><em>lo explicamos.</em></h2></div><p>Pregunta por la fórmula concreta: composición y propiedades varían entre productos.</p></div>'
              f'<div class="brand-row reveal"><span>Arkhē</span><span>Olaplex</span><span>OPI</span><span>Masglo</span><span>Plástica</span><span>GHD</span></div>'
              f'<div class="prod-row"><figure class="reveal-img">{img("arkhe-producto", "Productos Arkhē con una planta")}<figcaption>Arkhē</figcaption></figure><figure class="reveal-img" style="--d:.1s">{img("olaplex", "Línea Olaplex")}<figcaption>Olaplex</figcaption></figure><figure class="reveal-img" style="--d:.2s">{img("plastica", "Línea Plástica de cuidado capilar")}<figcaption>Plástica</figcaption></figure><figure class="reveal-img" style="--d:.3s">{img("opi-jelly", "Esmaltes OPI Make Em Jelly")}<figcaption>OPI</figcaption></figure></div>'
              f'<div class="actions" style="justify-content:center">{link("cuidados", "Descubre el cuidado en casa")}</div></div></section>')
    team = (f'<section class="section pearl"><div class="wrap team-grid"><div class="team-photo reveal"><div class="frame">{img("equipo", "Anabel y las dos profesionales del equipo de AURA")}</div><div class="small">{img("aniversario-anabel", "Anabel junto a un arco de globos en el aniversario")}</div></div>'
            f'<div class="reveal" style="--d:.15s">{kicker("Las manos detrás de AURA")}<h2>Buenas manos.<br><em>Mejor energía.</em></h2><p style="margin-top:26px">Anabel y sus compañeras comparten un compromiso: que cada persona se sienta acompañada desde la primera conversación. Más de veinte años de oficio y la misma ilusión que el primer día.</p>'
            f'<blockquote class="quote-big">«Ya van 2 años de cumplir un sueño.»<br><small style="font:500 .8rem var(--sans);letter-spacing:.14em;color:var(--mute)">— Del Instagram de AURA</small></blockquote><div class="actions">{link("salon", "Entra en nuestro mundo", "btn btn--dark")}</div></div></div></section>')
    finder = (f'<section class="section"><div class="wrap finder-grid"><div class="reveal">{kicker("Empieza por una sensación")}<h2>Hoy me<br><em>apetece…</em></h2><p style="margin-top:22px">Un poco de luz. Más suavidad. O, simplemente, un rato para ti.</p></div>'
              f'<div class="reveal" style="--d:.15s"><div class="finder-options" role="group" aria-label="Elige tu objetivo"><button data-find="color" aria-pressed="true" class="active">Dar luz a mi melena</button><button data-find="soft" aria-pressed="false">Más suavidad</button><button data-find="event" aria-pressed="false">Un día especial</button><button data-find="care" aria-pressed="false">Un rato para mí</button></div>'
              f'<div id="finder-result" aria-live="polite"><h3>La luz empieza en un buen diagnóstico.</h3><p>Explora el color personalizado y el cuidado de rubios. Te ayudamos a elegir el tono y el proceso que encajen con tu cabello.</p>{link("rubios", "Explorar rubios y matices")}</div></div></div></section>')
    faq = faqs([('¿Cómo puedo reservar mi primera visita?', 'Prepara tu mensaje de WhatsApp desde el botón de cita o llama al 642 63 69 70. El equipo confirmará contigo la disponibilidad y el servicio.'),
                ('¿Dónde está el salón?', 'En la avenida Inmaculada Concepción, 42, en El Sauzal, Tenerife. En Contacto encontrarás el enlace para preparar tu ruta.'),
                ('¿Qué cuidado me recomendáis?', 'Antes de elegir el servicio escuchamos lo que buscas y valoramos tu cabello o tus necesidades. Así podemos recomendarte una propuesta personalizada.'),
                ('¿Puedo consultar el presupuesto antes de ir?', 'Sí. Cuéntanos qué necesitas. Algunos trabajos requieren ver el cabello para concretar el importe y el tiempo de la cita.')])
    return h + ticker + manifesto + services + tf + space + story + bridal + brands + team + reviews() + ig_wall() + finder + faq


page('index', 'Belleza con raíces', 'Peluquería y estética orgánica en El Sauzal. Color, keratina, novias y bienestar con el cuidado cercano de AURA.', home())


# ───────────── páginas de servicio ─────────────
for slug, d in SERVICES.items():
    m = PAGE_MEDIA[slug]
    h = hero(slug, d['eyebrow'], d['heading'], d['intro'], crumb=d['short'], chips=('Con cita', 'Diagnóstico personalizado', 'El Sauzal'))
    nav = ('<nav class="page-index page-nav" aria-label="En esta página"><div class="wrap"><a href="#filosofia">El cuidado</a><a href="#opciones">Tu propuesta</a>'
           + ('<a href="#transformaciones">Antes y después</a>' if m['pairs'] else '') + '<a href="#trabajos">Trabajos reales</a><a href="#preguntas">Tus dudas</a>' + book('Consultar este servicio', d['title'], '') + '</div></nav>')
    quote = f'<section class="quote-band emerald grain" id="filosofia"><div class="wrap reveal">{kicker("Nuestra forma de hacerlo")}<p>«{d["quote"]}»</p></div></section>'
    secs = ''
    for i, (title, p1, p2) in enumerate(d['sections']):
        nr = f'<span class="nr">0{i + 1}</span>'
        if i % 2 == 0:
            ph = m['sec'][i // 2]
            rev = ' reverse' if i == 2 else ''
            secs += (f'<section class="section{" pearl" if i == 0 else ""}" id="{"descubrir" if i == 0 else f"s{i}"}"><div class="wrap editorial{rev}"><div class="photo reveal"><div class="frame">{img(ph, d["title"] + ": fotografía real de AURA")}</div></div>'
                     f'<div class="reveal" style="--d:.12s">{nr}<h2>{title}</h2><p>{p1}</p><p>{p2}</p></div></div></section>')
        else:
            secs += f'<section class="section dark grain"><div class="wrap text-two"><div class="reveal">{nr}<h2>{title}</h2></div><div class="reveal" style="--d:.12s"><p>{p1}</p><p>{p2}</p></div></div></section>'
    opts = ''.join(f'<article class="option reveal" style="--d:{i * .1}s"><span class="nr">0{i + 1}</span><h3>{t}</h3><p>{p}</p><div class="row">{link(s, "Conocer más")}{book("Consultar mi caso", d["title"], "link")}</div></article>' for i, (t, p, s) in enumerate(d['options']))
    options = f'<section class="section" id="opciones"><div class="wrap"><div class="section-head reveal"><div>{kicker("A tu medida")}<h2>¿Por dónde<br><em>empezamos?</em></h2></div></div><div class="options">{opts}</div><p class="budget-note">Cada propuesta se valora de forma personal. Consulta el tiempo y el presupuesto antes de confirmar tu cita.</p></div></section>'
    tf = transform(m['pairs']) if m['pairs'] else ''
    wk = (f'<section class="section {"" if m["pairs"] else "pearl"}" id="trabajos"><div class="wrap"><div class="section-head reveal"><div>{kicker("Hecho en AURA")}<h2>El cuidado<br><em>toma forma.</em></h2></div>{link("galeria", "Ver todos los trabajos")}</div>{works(m["works"], five=len(m["works"]) == 5)}</div></section>')
    others = [s for s in SERVICES if s != slug][:3]
    rel = f'<section class="section pearl"><div class="wrap"><div class="section-head reveal"><div>{kicker("Sigue explorando")}<h2>También te<br><em>puede gustar.</em></h2></div></div>{svc_cards(others)}</div></section>'
    page(slug, d['title'], d['intro'], h + nav + quote + secs + options + tf + wk + faqs(d['faq'], dark=True) + rel)


# ───────────── servicios ─────────────
extra = [('Corte y peinado', 'Forma, movimiento y un acabado adaptado a tu día a día.'), ('Manicura y pedicura', 'Cuidado de manos y pies, forma y color para las uñas.'), ('Maquillaje', 'Una propuesta personal para tu próxima celebración.'), ('Depilación con hilo', 'Trabajo de precisión para zonas del rostro.'),
         ('Depilación láser', 'Consulta zonas, valoración previa y preparación.'), ('Presoterapia', 'Un servicio de bienestar cuya idoneidad se valora antes de la sesión.'), ('Facial y corporal', 'Cuidados de la piel según las opciones disponibles en el salón.'), ('Cuidado en casa', 'Orientación sobre productos profesionales para tu rutina.')]
page('servicios', 'La carta de cuidados', 'Todos los servicios de AURA: peluquería orgánica, color, rubios, keratina, estética, bienestar, novias y maquillaje.',
     hero('servicios', 'La carta AURA', 'Tu próximo\nritual.', 'Hay días para cambiar. Otros, para mantener lo que te gusta. Y otros, simplemente, para dedicarte tiempo. Encuentra aquí tu próximo momento AURA.', crumb='Servicios')
     + f'<section class="section" id="descubrir"><div class="wrap"><div class="section-head reveal"><div>{kicker("Explora por cuidado")}<h2>Una carta.<br><em>Muchas formas de ser tú.</em></h2></div><p>Selecciona una especialidad para descubrir el proceso, los trabajos y las preguntas frecuentes.</p></div>{svc_cards(list(SERVICES))}</div></section>'
     + f'<section class="section dark grain"><div class="wrap"><div class="section-head reveal"><div>{kicker("También en AURA")}<h2>El detalle<br><em>lo cambia todo.</em></h2></div><p>Pregunta al equipo por estas opciones y combina tu visita según disponibilidad.</p></div><div class="options four">'
     + ''.join(f'<article class="option reveal" style="--d:{(i % 4) * .08}s;background:rgba(248,242,230,.05);color:var(--ivory)"><span class="nr">0{i + 1}</span><h3>{t}</h3><p style="color:rgba(248,242,230,.75)">{p}</p><div class="row">{book("Consultar", t, "link")}</div></article>' for i, (t, p) in enumerate(extra))
     + '</div></div></section>'
     + faqs([('¿Qué servicio elijo si no lo tengo claro?', 'Elige asesoramiento personalizado. El equipo te escuchará y valorará contigo las opciones según tus necesidades.'), ('¿Cuánto tiempo dura una cita?', 'Depende del servicio y del trabajo acordado. Indica si tienes una hora límite al consultar disponibilidad para que el equipo pueda orientarte.'), ('¿Puedo conocer el presupuesto antes?', 'Sí. Cuéntanos qué necesitas y consulta el importe. Algunos trabajos requieren valorar el cabello o la zona antes de cerrar el presupuesto.')]))


# ───────────── el salón ─────────────
page('salon', 'El salón y su equipo', 'Conoce a las tres profesionales de AURA Organic Salón en El Sauzal y su filosofía de cuidado cercano y personalizado.',
     hero('salon', 'Bienvenida a nuestro espacio', 'Buenas manos.\nMejor energía.', 'Tres profesionales, más de veinte años de experiencia y una forma de entender la belleza que empieza por escucharte. Esto es AURA.', crumb='El salón')
     + f'<section class="section" id="descubrir"><div class="wrap text-two"><div class="reveal">{kicker("Lo que nos une")}<h2>Manos expertas.<br><em>Trato de siempre.</em></h2></div><div class="reveal" style="--d:.12s"><p>Detrás de AURA hay un equipo de tres mujeres apasionadas por la peluquería y el cuidado del cabello. Anabel y sus compañeras comparten un compromiso: que cada persona se sienta acompañada desde la primera conversación.</p><p>La experiencia nos ayuda a mirar con criterio; la cercanía, a entender lo que necesitas. No queremos que elijas un servicio por inercia, sino que comprendas la propuesta y te sientas a gusto con ella.</p><p>Nos encontrarás en El Sauzal, en el norte de Tenerife. Un salón unisex donde puedes venir con una idea muy clara o con ganas de descubrir algo nuevo.</p></div></div>'
       f'<div class="wrap"><div class="stats"><div><strong data-count="20">0<small>+</small></strong><span>Años de experiencia</span></div><div><strong data-count="3">0</strong><span>Profesionales</span></div><div><strong data-count="2">0</strong><span>Años en El Sauzal</span></div><div><strong>Tú</strong><span>En el centro de cada decisión</span></div></div></div></section>'
     + f'<section class="section pearl"><div class="wrap team-grid"><div class="team-photo reveal"><div class="frame">{img("equipo", "Las tres profesionales de AURA")}</div><div class="small">{img("aniversario-anabel", "Anabel en el aniversario del salón")}</div></div><div class="reveal" style="--d:.15s">{kicker("Las tres de AURA")}<h2>Un equipo,<br><em>una misma mirada.</em></h2><p style="margin-top:26px">Escuchar, asesorar y atender de forma personal: esa es nuestra forma de trabajar. El equipo sigue formándose y participa en eventos de marcas profesionales, como el Experience Day de Arkhē Cosmetics que acogimos en el salón.</p><p>Cuando celebramos los dos años del salón lo hicimos como más nos gusta: con quienes nos acompañan.</p><div class="actions">{book("Quiero conocerlas")}</div></div></div></section>'
     + f'<section class="section dark grain"><div class="wrap"><div class="section-head reveal"><div>{kicker("Un espacio con raíces")}<h2>Madera, verde<br><em>y buenas conversaciones.</em></h2></div><p>Los listones de nogal, las plantas y los detalles de AURA acompañan cada visita.</p></div><div class="mosaic"><figure class="m1 reveal-img">{img("arkhe-expositor", "Expositor Arkhē entre listones de madera y plantas")}<figcaption>Listones de nogal</figcaption></figure><figure class="m2 reveal-img" style="--d:.1s">{img("letrero-2", "Letrero de AURA")}<figcaption>El letrero AURA</figcaption></figure><figure class="m3 reveal-img" style="--d:.2s">{img("salon-estanteria", "Estantería")}<figcaption>Producto profesional</figcaption></figure><figure class="m4 reveal-img" style="--d:.15s">{img("planta-1", "Planta del salón")}<figcaption>Un rincón verde</figcaption></figure><figure class="m5 reveal-img" style="--d:.25s">{img("lavado", "Una clienta en el lavacabezas con el espejo del salón al fondo")}<figcaption>Un momento de calma</figcaption></figure><figure class="m6 reveal-img" style="--d:.3s">{img("fachada-clienta", "Entrada del salón", style="object-position:50% 35%")}<figcaption>La puerta de AURA</figcaption></figure></div></div></section>'
     + f'<section class="section"><div class="wrap"><div class="section-head reveal"><div>{kicker("Nuestros imprescindibles")}<h2>Una manera<br><em>de hacer las cosas.</em></h2></div></div><div class="options">'
     + ''.join(f'<article class="option reveal" style="--d:{i * .1}s"><span class="nr">0{i + 1}</span><h3>{t}</h3><p>{p}</p></article>' for i, (t, p) in enumerate([('Escuchar de verdad', 'Tu rutina, tus gustos y tus dudas tienen sitio. Empezamos por entender qué quieres cambiar y qué quieres conservar.'), ('Elegir con criterio', 'Valoramos el cabello y explicamos las opciones. Puedes preguntar por los productos y las características de cada fórmula.'), ('Acogerte como eres', 'Somos un salón unisex para todas las personas, identidades y edades. Un trato respetuoso y cercano, donde cada persona pueda expresarse con tranquilidad.')]))
     + '</div></div></section>' + reviews()
     + f'<section class="section pearl"><div class="wrap team-grid"><div class="reveal"><h2>El cuidado no termina<br><em>en el salón.</em></h2><p style="margin-top:26px">Una buena recomendación también puede simplificar tus mañanas. Te orientamos sobre el lavado, el acabado y los productos profesionales adecuados a tu cabello.</p><div class="actions">{link("cuidados", "Descubre el cuidado en casa", "btn btn--dark")}</div></div><div class="team-photo reveal" style="--d:.15s"><div class="frame">{img("arkhe-expositor", "Expositor de cuidado capilar en AURA")}</div></div></div></section>')


# ───────────── galería ─────────────
page('galeria', 'Trabajos reales de AURA', 'Explora fotografías reales de color, recogidos, manicuras, productos y del equipo de AURA. Filtra y amplía cada trabajo.',
     hero('galeria', 'El álbum AURA', 'El álbum\nde AURA.', 'Melenas con movimiento, recogidos que cuentan historias y pequeños detalles hechos con cariño. Aquí puedes mirar de cerca nuestro trabajo.', crumb='Galería')
     + f'<section class="section" id="descubrir"><div class="wrap"><div class="section-head reveal"><div>{kicker("Fotografías reales del salón")}<h2>Explora.<br><em>Encuentra tu inspiración.</em></h2></div><p>Pulsa una foto para verla de cerca y acceder a su publicación original.</p></div>{gallery(GALLERY)}<p class="gallery-disclaimer">Selección de fotografías publicadas por AURA en Instagram y en su ficha pública. El color puede variar según la luz y la pantalla.</p></div></section>'
     + transform(list(PAIRS))
     + f'<section class="section dark grain"><div class="wrap" style="text-align:center;max-width:820px">{kicker("Siempre hay algo nuevo")}<h2>La vida de AURA<br><em>sigue en nuestras redes.</em></h2><p style="margin-top:22px">Para ver los últimos trabajos, historias y novedades, visita nuestros perfiles.</p><div class="actions" style="justify-content:center">{ext(INSTAGRAM, "Ver Instagram", "btn")}{ext(FACEBOOK, "Ver Facebook", "btn btn--ghost")}</div></div></section>')


# ───────────── cuidados ─────────────
page('cuidados', 'Cuidado en casa', 'Productos profesionales y una rutina capilar personalizada con el asesoramiento de AURA Organic Salón.',
     hero('cuidados', 'Cuidarte, también en casa', 'El cuidado\nva contigo.', 'Tu cabello sigue contigo después de la cita. Te ayudamos a elegir una rutina coherente, sencilla y adaptada a lo que necesita.', crumb='Cuidado en casa')
     + f'<section class="section" id="descubrir"><div class="wrap editorial"><div class="photo reveal"><div class="frame">{img("arkhe-expositor", "Expositor de productos de cuidado capilar en AURA")}</div></div><div class="reveal" style="--d:.12s">{kicker("Menos improvisar, más entender")}<h2>Lo que le va bien<br><em>a tu cabello.</em></h2><p>Una rutina útil no tiene por qué ser larga. El tipo de cabello, el color y la frecuencia de lavado ayudan a elegir qué productos tienen sentido y cómo utilizarlos.</p><p>En el salón encontrarás líneas profesionales como Arkhē (por ejemplo, Full Recovery para fortalecer y nutrir), Organic Care, Olaplex o Plástica. Consulta al equipo la gama disponible y el producto concreto recomendado para tu caso: la composición y las propiedades varían entre fórmulas.</p><p>No todas las líneas ni todos los productos tienen las mismas características de origen natural. Puedes pedir información sobre ingredientes, indicaciones y modo de uso antes de comprar.</p><div class="actions">{book("Quiero una recomendación", "Asesoramiento personalizado")}</div></div></div></section>'
     + f'<section class="section dark grain"><div class="wrap"><div class="section-head reveal"><div>{kicker("Tu rutina, con intención")}<h2>Cuatro gestos<br><em>para empezar.</em></h2></div></div><div class="care-grid">'
     + ''.join(f'<article class="reveal" style="--d:{i * .1}s"><span>{a}</span><h3>{b}</h3><p>{c}</p></article>' for i, (a, b, c) in enumerate([('Lavar', 'Elige según tu cuero cabelludo.', 'La frecuencia y el champú deben encajar con tus necesidades. Aplica el producto como indique su fabricante y aclara bien.'), ('Acondicionar', 'Atiende medios y puntas.', 'Pregunta qué cuidado utilizar y cuánto tiempo dejarlo actuar. Más cantidad no siempre significa un mejor resultado.'), ('Proteger', 'Cuida el acabado al peinar.', 'Te orientamos sobre el uso de calor y el producto de protección adecuado. Evita concentrar calor de forma innecesaria.'), ('Revisar', 'Escucha cómo cambia tu cabello.', 'Si notas que la rutina deja de funcionar o has cambiado de color, coméntalo. Una recomendación puede necesitar ajustes.')]))
     + f'</div></div></section><section class="section"><div class="wrap"><div class="brand-row reveal"><span>Arkhē</span><span>Organic Care</span><span>Olaplex</span><span>Plástica</span><span>GHD</span></div><div class="prod-row"><figure class="reveal-img">{img("arkhe-producto", "Productos Arkhē")}<figcaption>Arkhē</figcaption></figure><figure class="reveal-img" style="--d:.1s">{img("real-08", "Productos Organic Care")}<figcaption>Organic Care</figcaption></figure><figure class="reveal-img" style="--d:.2s">{img("olaplex", "Línea Olaplex")}<figcaption>Olaplex</figcaption></figure><figure class="reveal-img" style="--d:.3s">{img("plastica", "Línea Plástica")}<figcaption>Plástica</figcaption></figure></div></div></section>'
     + f'<section class="section pearl"><div class="wrap text-two"><div class="reveal"><h2>Tu color también<br><em>tiene su rutina.</em></h2></div><div class="reveal" style="--d:.12s"><p>El cuidado después de una coloración, un trabajo de rubio o una keratina debe seguir las instrucciones del servicio realizado. Pregunta antes de utilizar productos con pigmento o tratamientos intensivos por tu cuenta.</p><p>El equipo puede indicarte cómo espaciar las revisiones y qué señales conviene observar. Trae a tu cita el nombre de los productos que usas: entender tu rutina nos ayuda a orientarte mejor.</p>{link("coloracion", "Conocer el cuidado del color")}</div></div></section>'
     + faqs([('¿Puedo comprar productos en el salón?', 'Consulta al equipo las líneas y referencias disponibles. Te orientarán sobre precio, uso y disponibilidad; esta web no procesa compras.'), ('¿Cómo sé si un producto es de origen natural?', 'Revisa la información del producto concreto. El porcentaje y las certificaciones, si existen, deben corresponder a esa fórmula; no se pueden extender a una marca completa.'), ('¿Necesito una mascarilla en cada lavado?', 'Depende de tu cabello y del producto. Sigue la recomendación personalizada y el modo de empleo del fabricante.'), ('¿Puedo pedir asesoramiento por WhatsApp?', 'Sí. Cuéntanos qué servicio te has realizado y qué te preocupa de tu rutina. El equipo te dirá si necesita ver tu cabello para orientarte.')], dark=True))


# ───────────── contacto ─────────────
page('contacto', 'Contacto y citas', 'Pide cita en AURA Organic Salón: 642 63 69 70. Av. Inmaculada Concepción 42, El Sauzal, Tenerife.',
     hero('contacto', 'El Sauzal, Tenerife', 'Hagamos\nun hueco.', 'Estamos al otro lado para escucharte, resolver tus dudas y encontrar un hueco para ti. Llámanos o prepara tu solicitud por WhatsApp.', crumb='Contacto')
     + f'<section class="section" id="descubrir"><div class="wrap contact-grid"><div class="reveal">{kicker("Hablemos")}<h2>Una conversación<br><em>lo pone todo en marcha.</em></h2><a class="contact-phone" href="tel:{TEL}">642 63 69 70</a><p>Para pedir cita, consultar un servicio o preparar tu primera visita.</p><div class="actions">{book("Preparar mi solicitud")}<a class="link" href="tel:{TEL}">Prefiero llamar <span>→</span></a></div><p style="margin-top:34px"><a class="link" href="mailto:auraesteticasauzal@gmail.com">auraesteticasauzal@gmail.com</a></p><div class="contact-social">{ext(INSTAGRAM, "Instagram")}{ext(FACEBOOK, "Facebook")}</div></div>'
       f'<div class="visit-card reveal" style="--d:.15s"><h3>Ven a vernos</h3><address>Av. Inmaculada Concepción, 42<br>38360 El Sauzal<br>Santa Cruz de Tenerife</address><h4>Horario de verano publicado</h4><ul class="hours"><li><span>Lunes a viernes</span><b>9:00 – 17:30</b></li><li><span>Sábados</span><b>9:00 – 14:00</b></li></ul><p style="margin-top:14px">Horario publicado por el salón en Instagram para la temporada de verano. Confirma el horario actual y la disponibilidad con el equipo; atendemos con cita.</p><div class="actions">{ext(GOOGLE, "Preparar mi ruta", "btn")}</div></div></div></section>'
     + f'<section class="section pearl"><div class="wrap"><div class="section-head reveal"><div>{kicker("Así nos reconocerás")}<h2>Busca el letrero<br><em>de AURA.</em></h2></div><p>El rótulo «Peluquería y Estética Unisex» y el logo de AURA te indican la entrada, en la avenida Inmaculada Concepción.</p></div><div class="facade"><div class="reveal-img">{img("fachada-clienta-2", "Clienta en la entrada del salón, con el rótulo Peluquería y Estética Unisex")}</div><div class="reveal-img" style="--d:.12s">{img("real-13", "Fachada de AURA Organic Salón")}</div><div class="reveal-img" style="--d:.24s">{img("aniversario-arco", "Arco de globos en la puerta de AURA")}</div></div></div></section>'
     + f'<section class="section"><div class="wrap contact-grid"><div class="reveal">{kicker("Aquí estamos")}<h2>En el corazón<br><em>de El Sauzal.</em></h2><p style="margin-top:22px">Una visita para cuidarte en el norte de Tenerife. Consulta la ruta desde tu ubicación y organiza tu llegada con tiempo.</p><p>Si necesitas información sobre acceso, aparcamiento o alguna adaptación para tu visita, cuéntanoslo al reservar. Te ayudaremos a prepararla.</p></div><div class="map-card reveal" style="--d:.15s"><span class="pin">AURA</span><h3>Av. Inmaculada Concepción, 42</h3><p>38360 El Sauzal · Tenerife</p><div class="actions" style="margin-top:20px">{ext(GOOGLE, "Abrir en Google Maps", "btn")}</div></div></div></section>'
     + f'<section class="section dark grain"><div class="wrap"><div class="section-head reveal"><div>{kicker("Tu primera visita")}<h2>Todo empieza<br><em>con una idea.</em></h2></div></div><div class="options">'
     + ''.join(f'<article class="option reveal" style="--d:{i * .1}s;background:rgba(248,242,230,.05);color:var(--ivory)"><span class="nr">0{i + 1}</span><h3>{t}</h3><p style="color:rgba(248,242,230,.78)">{p}</p></article>' for i, (t, p) in enumerate([('Cuéntanos qué necesitas', 'Indica el servicio o la duda. Si se trata de color o keratina, menciona los trabajos anteriores que lleve tu cabello.'), ('Acordamos los detalles', 'El equipo confirma disponibilidad, duración orientativa y presupuesto. La solicitud web prepara el mensaje; no cierra una reserva por sí sola.'), ('Ven a tu momento', 'Trae tus referencias si las tienes. Si necesitas cambiar o cancelar tu cita, avisa al salón con la mayor antelación posible.')]))
     + '</div></div></section>'
     + faqs([('¿Se confirma la cita al rellenar el formulario?', 'No. El formulario prepara un mensaje que tú envías desde WhatsApp. La cita solo queda acordada cuando el equipo confirma día y hora.'), ('¿Puedo reservar por teléfono?', 'Sí. Llama al 642 63 69 70 para consultar disponibilidad y organizar tu visita.'), ('¿Hay aparcamiento y acceso adaptado?', 'La información aportada menciona aparcamiento cercano y acceso adaptado. Confirma con el salón las condiciones actuales y cualquier necesidad específica antes de desplazarte.'), ('¿Qué métodos de pago aceptáis?', 'El directorio del negocio indica pago con tarjeta. Para confirmar modalidades actuales u otras opciones, consulta al equipo al reservar.')]))


# ───────────── información y 404 ─────────────
page('informacion', 'Información y privacidad', 'Información de la propuesta web de AURA, fuentes de imágenes y funcionamiento de la solicitud por WhatsApp.',
     hero('informacion', 'Información de la web', 'Todo\nen su sitio.', 'Conoce cómo funciona esta demostración, de dónde viene el material y qué ocurre cuando preparas una solicitud de cita.', crumb='Información', cta=False)
     + f'<section class="section" id="descubrir"><div class="wrap legal"><h2>Sobre este proyecto</h2><p>Esta web es una propuesta de diseño para AURA Organic Salón. La identidad y las imágenes de marca han sido aportadas para el proyecto. Las fotografías de trabajos, equipo y salón se han seleccionado de las publicaciones públicas del salón.</p><h2>Fuentes y fotografías</h2><p>Se han consultado <a href="{INSTAGRAM}">Instagram</a>, <a href="{FACEBOOK}">Facebook</a>, la <a href="{GOOGLE}">ficha de Google</a> y <a href="{PA}">Páginas Amarillas</a>. La galería permite acceder a las fuentes originales. Las reseñas mostradas son extractos visibles en Google en la consulta del 20 de noviembre de 2026; no son opiniones inventadas. Las comparaciones de antes y después proceden de composiciones publicadas por el salón, separadas sin retoque.</p><h2>Solicitudes de cita</h2><p>El formulario funciona en tu navegador. No almacena tus datos ni los envía a una base de datos. Al preparar el mensaje verás su contenido y podrás abrir WhatsApp para revisarlo y enviarlo al teléfono del salón. WhatsApp aplica sus propias condiciones y política de privacidad.</p><h2>Servicios externos</h2><p>Esta web no incorpora analítica ni publicidad. Los enlaces a Google, Instagram, Facebook y WhatsApp se abren cuando tú los seleccionas. No se cargan sus reproductores, mapas ni herramientas de seguimiento dentro de esta página.</p><h2>Información comercial</h2><p>Los servicios, productos, horarios y precios deben confirmarse con el salón antes de reservar. Las descripciones ayudan a conocer la oferta; no garantizan un resultado idéntico para todas las personas. Antes de la publicación comercial definitiva deben incorporarse los datos legales completos del titular y validarse los contenidos con el negocio.</p><h2>Contacto</h2><p>AURA Organic Salón · Av. Inmaculada Concepción, 42, 38360 El Sauzal, Santa Cruz de Tenerife. Teléfono: <a href="tel:{TEL}">642 63 69 70</a>. Email de contacto publicado por el salón: <a href="mailto:auraesteticasauzal@gmail.com">auraesteticasauzal@gmail.com</a>.</p></div></section>')

page('404', 'No encontramos esta página', 'Vuelve a explorar los cuidados de AURA Organic Salón.',
     hero('404', 'Volvamos a encontrarnos', 'Sigue\ntu aura.', 'La página que buscas no está disponible. Vuelve al inicio o explora nuestra carta de cuidados.', cta=False,
          extra=f'<div class="actions">{link("index", "Volver al inicio", "btn")}{link("servicios", "Ver los servicios", "btn btn--ghost")}</div>')
     + '<div id="descubrir"></div>')

(OUT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf8')
print(f'Generadas {len(list(OUT.glob("*.html")))} páginas HTML.')
