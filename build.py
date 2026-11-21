"""Generador de la web de AURA Organic Salón (v3). Ejecutar: python build.py"""
from pathlib import Path
from html import escape as e
import json
from urllib.parse import quote as urlquote
import re
from content import SERVICES, PA, GOOGLE, INSTAGRAM, FACEBOOK

ROOT = Path(__file__).parent
OUT = ROOT / 'dist'
ORIGIN = 'https://sefiro888.github.io/aura-organic-web'
TEL = '+34642636970'


def ig(code, kind='p'):
    return f'https://www.instagram.com/{kind}/{code}/'


# ───────────── imágenes ─────────────
_DIMS = {}


def dims(name):
    if name not in _DIMS:
        try:
            from PIL import Image
            with Image.open(OUT / 'assets' / 'img' / f'{name}.webp') as im:
                _DIMS[name] = im.size
        except Exception:
            _DIMS[name] = None
    return _DIMS[name]


def img(name, alt, cls='', eager=False, style=''):
    a = f' class="{cls}"' if cls else ''
    s = f' style="{style}"' if style else ''
    load = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"'
    d = dims(name)
    wh = f' width="{d[0]}" height="{d[1]}"' if d else ''
    return f'<img{a}{s} src="assets/img/{name}.webp" alt="{e(alt)}"{wh}{load} decoding="async">'


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
    'index': ('62% 40%', 'letrero-ondas', 'balayage'),
    'servicios': ('50% 40%', 'ritual-color', 'real-12'),
    'peluqueria': ('40% 50%', 'largo-reflejos', 'bob-miel'),
    'coloracion': ('58% 40%', 'ritual-color', 'cobrizo'),
    'rubios': ('70% 30%', 'rubio-rizos', 'balayage'),
    'keratina': ('30% 50%', 'liso-oscuro', 'letrero-liso'),
    'estetica': ('80% 60%', 'unas-puesto', 'real-12'),
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


ICONS = {'people': '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3.5 19c.5-3.5 3-5.5 5.5-5.5s5 2 5.5 5.5"/><path d="M15 14c3 0 5 1.8 5.5 5"/>', 'search': '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/><path d="M8.5 11h5"/>', 'bottle': '<path d="M10 3h4v3h-4z"/><path d="M9 6h6l1 3v10a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2V9z"/><path d="M9 13h6"/>', 'sparkle': '<path d="M12 3c.8 4.5 2.5 6.2 7 7-4.5.8-6.2 2.5-7 7-.8-4.5-2.5-6.2-7-7 4.5-.8 6.2-2.5 7-7Z"/><path d="M19 17v4M17 19h4"/>', 'leaf': '<path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14"/><path d="M5 19c3-4 6-7 10-9"/>', 'palette': '<path d="M12 3a9 9 0 1 0 0 18c1.5 0 2-1 1.5-2s0-2 1.5-2h2a3 3 0 0 0 3-3c0-5-4-11-8-11Z"/><circle cx="8" cy="11" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="16" cy="10" r="1"/>', 'strand': '<path d="M3 9c3-4 6 4 9 0s6 4 9 0"/><path d="M3 15c3-4 6 4 9 0s6 4 9 0"/>', 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6 7 7M17 17l1.4 1.4M18.4 5.6 17 7M7 17l-1.4 1.4"/>', 'layers': '<path d="M12 4 3 9l9 5 9-5z"/><path d="M3 14l9 5 9-5"/>', 'steps': '<path d="M4 20h4v-4h4v-4h4V8h4"/><path d="M17 5l3 3-3 3"/>', 'shield': '<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/><path d="m9 12 2 2 4-4"/>', 'calendar': '<rect x="4" y="5" width="16" height="15" rx="3"/><path d="M4 10h16M9 3v4M15 3v4"/>', 'smooth': '<path d="M3 8c6-2 12 2 18 0M3 12c6-2 12 2 18 0M3 16c6-2 12 2 18 0"/>', 'check': '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.8 2.8L16 9.5"/>', 'hand': '<path d="M8 12V6a1.5 1.5 0 0 1 3 0v5"/><path d="M11 11V4.5a1.5 1.5 0 0 1 3 0V11"/><path d="M14 11V6a1.5 1.5 0 0 1 3 0v8c0 4-2.5 6-6 6-3 0-4.5-1.5-6-4l-1.5-3a1.5 1.5 0 0 1 2.5-1.5L8 14"/>', 'brush': '<path d="M20 4c-5 2-9 6-10.5 10"/><path d="M9.5 14c-2.5 0-3.5 2-3.5 4-1 0-2 .5-2 1.5C6 21 11 21 11 17c0-1.5-.5-2.5-1.5-3Z"/>', 'thread': '<path d="M3 18c4-13 14-13 18 0"/><path d="M8 11.5 6 8m10 3.500L18 8"/><circle cx="12" cy="9" r="1.2"/>', 'lotus': '<path d="M12 20c-4-2-6-6-6-10 3 1 5 3 6 6 1-3 3-5 6-6 0 4-2 8-6 10Z"/><path d="M12 16c-1-4 0-8 0-11 1 3 1 7 0 11Z"/>', 'mirror': '<circle cx="12" cy="10" r="6"/><path d="M12 16v5M9 21h6"/>', 'comb': '<path d="M4 8h16v3H4z"/><path d="M6 11v8M9 11v8M12 11v8M15 11v8M18 11v8"/>'}
TITLE_ICON = {'Unisex': 'people', 'Diagnóstico': 'search', 'Producto profesional': 'bottle', 'Rutina clara': 'sparkle', 'Sin amoniaco': 'leaf', 'Tono a medida': 'palette', 'Raíz y canas': 'strand', 'Mantenimiento': 'sun', 'Matices': 'layers', 'Por etapas': 'steps', 'Fibra cuidada': 'shield', 'Revisiones': 'calendar', 'Menos encrespamiento': 'smooth', 'Sin promesas vacías': 'check', 'Rutina posterior': 'sparkle', 'Manos y pies': 'hand', 'Maquillaje': 'brush', 'Hilo y láser': 'thread', 'Bienestar': 'lotus', 'La prueba': 'mirror', 'Peinado': 'comb', 'Invitadas': 'people'}


def ico(title):
    body = ICONS[TITLE_ICON.get(title, 'sparkle')]
    body = re.sub(r'<(path|circle|rect) ', r'<\1 pathLength="1" ', body)
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'


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
    parts = [(x[:1] + x[1:].lower() if i == 0 else x.lower()) if x.isupper() else x for i, x in enumerate(title.split('\n'))]
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
    chip_html = ('<div class="hero-chips">' + (open_badge() if cta else '') + ''.join(f'<span>{c}</span>' for c in chips) + '</div>') if (chips or cta) else ''
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
    chev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
    in_services = active in SERVICES or active in ('servicios', 'cuidados')
    sub = ''.join(f'<a href="{k}.html"' + (' aria-current="page"' if active == k else '') + f'><span class="n">0{i + 1}</span><span class="t">{v["title"]}</span><small>{v["short"]}</small></a>' for i, (k, v) in enumerate(SERVICES.items()))
    macc = (f'<div class="m-acc{" open" if in_services else ""}"><button type="button" class="m-acc-btn" aria-expanded="{"true" if in_services else "false"}" aria-controls="m-services"><span>Servicios</span>{chev}</button>'
            f'<div class="m-sub" id="m-services"><div class="m-sub-in"><a class="all" href="servicios.html"' + (' aria-current="page"' if active == 'servicios' else '') + f'>Toda la carta de cuidados <span aria-hidden="true">→</span></a>{sub}'
            f'<a class="more" href="cuidados.html"' + (' aria-current="page"' if active == 'cuidados' else '') + '>Cuidado en casa <span aria-hidden="true">→</span></a></div></div></div>')
    mitems = ''.join(macc if s == 'servicios' else f'<a href="{s}.html"' + (' aria-current="page"' if active == s else '') + f'>{t}</a>' for s, t in nav)
    phone = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>'
    return (f'<a class="skip" href="#contenido">Saltar al contenido</a>'
            f'<header class="header"><div class="header-in"><a href="index.html" class="brand" aria-label="AURA Organic Salón, inicio"><img src="assets/img/logo.webp" alt="" width="56" height="56"><span>AURA<small>ORGANIC SALÓN</small></span></a>'
            f'<nav class="desktop-nav" aria-label="Navegación principal">{items}</nav>'
            f'<div class="header-actions"><a class="header-phone" href="tel:{TEL}">{phone}642 63 69 70</a>{book("Tu momento AURA")}<button class="menu-toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span></button></div></div></header>'
            f'<div class="mobile-menu" id="mobile-menu" hidden><nav aria-label="Navegación móvil">{mitems}</nav>{social(labels=True)}<a class="btn" href="tel:{TEL}">Llamar · 642 63 69 70</a></div>'
            f'<div class="service-menu" id="service-menu"><div class="wrap"><div>{kicker("Elige cómo cuidarte")}<h2>Un cuidado<br><em>muy tuyo.</em></h2>{link("servicios", "Todos los servicios")}</div><div class="mega-grid">{mega}</div></div></div><div class="reading-progress" aria-hidden="true"></div>')


def closing():
    return (f'<section class="closing"><img src="assets/img/ambiente-logo.webp" alt="" loading="lazy"><div class="wrap"><div class="closing-copy reveal">{kicker("Hay un momento que es solo tuyo")}'
            f'<h2>Hazte<br><em>un hueco.</em></h2><p>Cuéntanos qué necesitas. Nosotras ponemos el tiempo, las manos y el cuidado.</p><div class="actions">{book("Encontrar mi momento")}'
            f'<a class="btn btn--ghost" href="https://wa.me/34642636970" target="_blank" rel="noopener">WhatsApp</a></div></div></div></section>')


def dock_html():
    phone = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>'
    cal = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="5" width="16" height="15" rx="3"/><path d="M4 10h16M9 3v4M15 3v4"/></svg>'

    def g(k):
        return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="' + SOC_PATHS[k] + '"/></svg>'
    wa_url = 'https://wa.me/34642636970?text=Hola%20AURA%2C%20me%20gustar%C3%ADa%20pedir%20cita.'
    return ('<nav class="mobile-dock" aria-label="Acciones rápidas">'
            + f'<a class="dk call" href="tel:{TEL}">{phone}<span>Llamar</span></a>'
            + f'<a class="dk wa" href="{wa_url}" target="_blank" rel="noopener">{g("whatsapp")}<span>WhatsApp</span></a>'
            + f'<button class="dock-fab" type="button" data-book="">{cal}<span>Pedir cita</span></button>'
            + f'<a class="dk gm" href="{GOOGLE}" target="_blank" rel="noopener">{g("maps")}<span>Ruta</span></a>'
            + f'<a class="dk ig" href="{INSTAGRAM}" target="_blank" rel="noopener">{g("instagram")}<span>Instagram</span></a></nav>')


def footer():
    wa = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'
    opts = ''.join('<option>' + v['title'] + '</option>' for v in SERVICES.values())
    svc = ''.join(f'<a href="{s}.html">{v["short"]}</a>' for s, v in SERVICES.items())
    return (closing() +
            f'<footer><div class="wrap"><div class="footer-main"><div><p>Peluquería y estética unisex<br>con una mirada más natural.</p>{social()}</div>'
            f'<div><h3>Servicios</h3>{svc}</div>'
            f'<div><h3>Ven a conocernos</h3><span>Av. Inmaculada Concepción, 42<br>38360 El Sauzal · Tenerife</span><a href="{GOOGLE}" target="_blank" rel="noopener">Cómo llegar ↗</a><a href="tel:{TEL}">642 63 69 70</a><a href="mailto:auraesteticasauzal@gmail.com">Escríbenos</a></div>'
            f'<div><h3>Sigue el día a día</h3><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram ↗</a><a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook ↗</a><a href="galeria.html">Galería</a><a href="cuidados.html">Cuidado en casa</a><a href="contacto.html">Organiza tu visita</a>{share_link()}</div></div>'
            f'<div class="footer-mark" aria-hidden="true">AURA</div>'
            f'<div class="footer-bottom"><span>© 2026 AURA Organic Salón</span><span>BELLEZA CON RAÍCES · EL SAUZAL</span><a href="informacion.html">Información y privacidad</a></div></div></footer>'
            f'<script type="application/json" id="hours-data">{hours_json()}</script>'
            f'<div class="social-rail" aria-label="Redes sociales">{social()}</div>'
            f'<a class="whatsapp-float" href="https://wa.me/34642636970?text=Hola%20AURA%2C%20me%20gustar%C3%ADa%20pedir%20cita." target="_blank" rel="noopener" aria-label="Pedir cita por WhatsApp">{wa}<span>Hablemos</span></a>'
            f'{dock_html()}'
            f'<dialog id="booking" aria-labelledby="booking-title"><button class="dialog-close" data-close aria-label="Cerrar solicitud">×</button><div class="booking-head">{kicker("Tu momento empieza aquí")}<h2 id="booking-title">¿Qué te apetece<br><em>hacer por ti?</em></h2><p>Prepara tu mensaje. El equipo confirmará disponibilidad, hora y presupuesto por WhatsApp.</p></div>'
            f'<form id="booking-form"><label>Me gustaría…<select name="service" required><option value="">Elegir un servicio</option><option>Asesoramiento personalizado</option>{opts}<option>Corte y peinado</option><option>Manicura y pedicura</option><option>Maquillaje</option><option>Depilación con hilo</option><option>Depilación láser</option><option>Presoterapia</option><option>Cuidado facial o corporal</option></select></label>'
            f'<div class="form-row"><label>Tu nombre<input name="name" autocomplete="given-name" maxlength="70" placeholder="¿Cómo te llamas?" required></label><label>Día preferido<input type="date" name="date"></label></div>'
            f'<label>Te viene mejor<select name="time"><option>Cualquier franja</option><option>Por la mañana</option><option>Por la tarde</option></select></label>'
            f'<label>Algo que quieras contarnos<textarea name="notes" rows="2" maxlength="600" placeholder="Tu idea, la fecha del evento, una duda…"></textarea></label>'
            f'<p class="form-note">Esta solicitud no reserva automáticamente. Los datos se incorporan al mensaje de WhatsApp y no se guardan en esta web.</p><button class="btn" type="submit">Preparar mi mensaje</button>'
            f'<div class="message-preview" hidden><p>Tu mensaje está listo:</p><pre id="message-text"></pre><a class="btn" id="send-whatsapp" target="_blank" rel="noopener">Abrir WhatsApp</a><p class="form-note">Revisa el texto y envíalo tú desde WhatsApp.</p></div></form></dialog>'
            f'<dialog id="lightbox" class="lightbox" aria-label="Fotografía ampliada"><button class="dialog-close" data-close aria-label="Cerrar fotografía">×</button><button class="lightbox-prev" aria-label="Foto anterior">‹</button><figure><img src="assets/img/equipo.webp" alt=""><figcaption><span id="lightbox-caption"></span><a id="lightbox-source" target="_blank" rel="noopener">Ver publicación original</a></figcaption></figure><button class="lightbox-next" aria-label="Foto siguiente">›</button></dialog>')


SHARE_IMG = ORIGIN + '/assets/img/og-share.jpg'
SHARE_ALT = 'Logotipo de AURA Organic Salón sobre madera de nogal y flores'
SHARE_HOME = {'t': 'AURA Organic Salón · Peluquería y estética en El Sauzal',
              'd': 'Peluquería y estética unisex en El Sauzal (Tenerife). Color sin amoniaco, rubios, keratina y novias. Más de 20 años de oficio y 4,8 ★ en Google. Pide tu cita.'}
SHARE_MSG = 'Mira AURA Organic Salón: peluquería y estética en El Sauzal 💚'


def share_meta(slug, title, desc):
    url = ORIGIN + '/' + ('' if slug == 'index' else f'{slug}.html')
    if slug == 'index':
        t, d = SHARE_HOME['t'], SHARE_HOME['d']
    else:
        t, d = f'{title} · AURA Organic Salón', desc
    t, d = e(t), e(d)
    return (f'<link rel="canonical" href="{url}"><meta name="robots" content="noindex,follow">'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="AURA Organic Salón"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}">'
            f'<meta property="og:url" content="{url}"><meta property="og:locale" content="es_ES">'
            f'<meta property="og:image" content="{SHARE_IMG}"><meta property="og:image:secure_url" content="{SHARE_IMG}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{SHARE_ALT}">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{SHARE_IMG}">'
            f'<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">')


def share_link(label='Compartir por WhatsApp', cls='share'):
    href = 'https://wa.me/?text=' + urlquote(SHARE_MSG + ' ' + ORIGIN + '/')
    return f'<a class="{cls}" data-share data-msg="{e(SHARE_MSG)}" href="{href}" target="_blank" rel="noopener">{label}</a>'


def page(slug, title, desc, body):
    schema = {'@context': 'https://schema.org', '@type': 'HairSalon', 'name': 'AURA Organic Salón', 'telephone': TEL,
              'address': {'@type': 'PostalAddress', 'streetAddress': 'Av. Inmaculada Concepción, 42', 'addressLocality': 'El Sauzal', 'postalCode': '38360', 'addressRegion': 'Santa Cruz de Tenerife', 'addressCountry': 'ES'},
              'sameAs': [INSTAGRAM, FACEBOOK], 'image': SHARE_IMG, 'url': ORIGIN + '/'}
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#150b05">'
            f'<title>{e(title)} · AURA Organic Salón · El Sauzal</title><meta name="description" content="{e(desc)}">{share_meta(slug, title, desc)}'
            f'<link rel="icon" type="image/png" href="assets/img/favicon.png">'
            f'<script>document.documentElement.classList.add("js");try{{if(sessionStorage.getItem("auraSeen"))document.documentElement.classList.add("seen")}}catch(e){{}}</script><link rel="preload" href="assets/fonts/cormorant.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/dmsans.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="assets/fonts/cormorant-italic.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script>'
            f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head><body data-page="{slug}"><svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs><linearGradient id="lotA" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#f3d3c8"/><stop offset="1" stop-color="#fdf1ec"/></linearGradient><linearGradient id="lotB" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#eba897"/><stop offset="1" stop-color="#f9d9cf"/></linearGradient><linearGradient id="lotC" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#df8f7c"/><stop offset=".55" stop-color="#eeb0a0"/><stop offset="1" stop-color="#f8d3c8"/></linearGradient><radialGradient id="lotPod" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#f6e2a8"/><stop offset="1" stop-color="#b8934b"/></radialGradient><linearGradient id="leafG" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#14613a"/><stop offset=".6" stop-color="#2f9158"/><stop offset="1" stop-color="#63c78a"/></linearGradient><linearGradient id="igG" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FEDA77"/><stop offset=".25" stop-color="#F58529"/><stop offset=".5" stop-color="#DD2A7B"/><stop offset=".75" stop-color="#8134AF"/><stop offset="1" stop-color="#515BD4"/></linearGradient><linearGradient id="calG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f9158"/><stop offset="1" stop-color="#14613a"/></linearGradient></defs></svg><div id="loader" aria-hidden="true"><div class="ring"><img src="assets/img/logo.webp" alt="" width="96" height="96"></div><span>AURA</span></div>{header(slug)}<main id="contenido">{body}</main>{footer()}</body></html>')
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


SOC_ICONS = {
    'instagram': '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".8" fill="currentColor"/>',
    'facebook': '<path d="M14 8.5h2V5.5h-2.6C11 5.5 10 7 10 9v1.5H8v3h2V20h3v-6.5h2.2l.5-3H13V9.3c0-.5.3-.8 1-.8Z"/>',
    'whatsapp': '<path d="M20 11.5a8 8 0 0 1-11.6 7.2L4 20l1.3-4.4A8 8 0 1 1 20 11.5Z"/><path d="M9 8c0 4 3 7 7 7l1-2-3-1-1 1-2-2 1-1-1-3Z"/>',
    'maps': '<path d="M12 21s-6-5.5-6-10a6 6 0 0 1 12 0c0 4.5-6 10-6 10Z"/><circle cx="12" cy="11" r="2.2"/>',
}


def social(labels=False, cls=''):
    items = [('instagram', 'Instagram', INSTAGRAM), ('facebook', 'Facebook', FACEBOOK), ('whatsapp', 'WhatsApp', 'https://wa.me/34642636970'), ('maps', 'Cómo llegar', GOOGLE)]
    out = ''
    for k, name, url in items:
        svg = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{SOC_ICONS[k]}</svg>'
        out += f'<a class="soc" href="{url}" target="_blank" rel="noopener" aria-label="{name}" title="{name}">{svg}' + (f'<span>{name}</span>' if labels else '') + '</a>'
    return f'<div class="social {cls}{" labeled" if labels else ""}">{out}</div>'


SOC_PATHS = {'instagram': 'M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558.788-.306 1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06l.045.03zm0 3.678c-3.405 0-6.162 2.76-6.162 6.162 0 3.405 2.76 6.162 6.162 6.162 3.405 0 6.162-2.76 6.162-6.162 0-3.405-2.76-6.162-6.162-6.162zM12 16c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm7.846-10.405c0 .795-.646 1.44-1.44 1.44-.795 0-1.44-.646-1.44-1.44 0-.794.646-1.439 1.44-1.439.793-.001 1.44.645 1.44 1.439z', 'facebook': 'M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z', 'whatsapp': 'M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z', 'maps': 'M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z'}
SOC_CLASS = {'instagram': 'ig', 'facebook': 'fb', 'whatsapp': 'wa', 'maps': 'gm'}


def social(labels=False, cls=''):
    items = [('instagram', 'Instagram', INSTAGRAM), ('facebook', 'Facebook', FACEBOOK), ('whatsapp', 'WhatsApp', 'https://wa.me/34642636970'), ('maps', 'Cómo llegar', GOOGLE)]
    out = ''
    for k, name, url in items:
        svg = f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{SOC_PATHS[k]}"/></svg>'
        out += f'<a class="soc {SOC_CLASS[k]}" href="{url}" target="_blank" rel="noopener" aria-label="{name}" title="{name}">{svg}' + (f'<span>{name}</span>' if labels else '') + '</a>'
    return f'<div class="social {cls}{" labeled" if labels else ""}">{out}</div>'


def ig_wall():
    wall = [('recogido-collage', ig('DffQEiTgNtk'), 'Recogido visto desde varios ángulos'), ('novia-1', ig('DezpExfjv0U'), 'Novia con peinado y maquillaje'), ('arkhe-expositor', ig('DegxbahAvfA'), 'Cuidado capilar Arkhē'), ('balayage', ig('DTylPUPjEwq'), 'Balayage con ondas'),
            ('equipo', ig('DefN9xpgI5v'), 'El equipo de AURA'), ('opi-jelly', ig('DKSFYKYIlI7'), 'Esmaltes OPI'), ('largo-reflejos', ig('DcGdB7_AtnT'), 'Melena larga con reflejos'), ('aniversario-arco', ig('DGqkEoDom6-'), 'Dos años de AURA')]
    reels = [('anabel-reel', ig('Df5ExgsA02z', 'reel'), '¡Y ahora le tocó a Anabel!'), ('lavado', ig('DegzEMiAZeC', 'reel'), 'Momento peluquería: tu pelo no es uno más'), ('ritual-color', ig('DfibHMSAcIS', 'reel'), 'Cuidarte, verte bien y apostar por la calidad')]
    play = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>'
    rl = ''.join(f'<a class="reel reveal" style="--d:{i * .1}s" href="{u}" target="_blank" rel="noopener" aria-label="Ver reel: {e(t)}">{img(n, t)}<span class="play">{play}</span><span class="cap">{t}</span><span class="tag">Reel</span></a>' for i, (n, u, t) in enumerate(reels))
    cells = ''.join(f'<a class="reveal" style="--d:{(i % 4) * .08}s" href="{u}" target="_blank" rel="noopener" aria-label="Ver en Instagram: {e(t)}">{img(n, t)}</a>' for i, (n, u, t) in enumerate(wall))
    profile = (f'<aside class="ig-profile reveal"><div class="ig-head"><img src="assets/img/logo.webp" alt="" width="84" height="84"><div><strong>aurasalonsauzal</strong><span>AURA SALON · Salud/belleza</span></div></div>'
               f'<p>Bienvenida a nuestro espacio 🌿 Aquí creemos que la belleza empieza por sentirte bien contigo.</p>'
               f'<ul class="ig-stats"><li><b>252</b><span>publicaciones</span></li><li><b>277</b><span>seguidores</span></li><li><b>315</b><span>seguidos</span></li></ul>'
               f'<div class="actions">{ext(INSTAGRAM, "Seguir en Instagram", "btn")}</div>'
               f'<div class="fb-card"><strong>AURA Organic Salón</strong><span>Facebook · Estilista de peluquería · 90 seguidores</span>{ext(FACEBOOK, "Visitar Facebook")}</div>{social()}</aside>')
    return (f'<section class="section pearl" id="redes"><div class="wrap"><div class="section-head reveal"><div>{kicker("Síguenos")}<h2>La vida en el salón,<br><em>cada día.</em></h2></div><p>Cabello, manos, recogidos y el equipo que lo hace posible. Fotografías y reels publicados por el propio salón.</p></div>'
            f'<div class="ig-layout">{profile}<div class="ig-main"><div class="reels">{rl}</div><div class="ig-grid">{cells}</div>'
            f'<p class="muted" style="margin-top:20px">Cifras de Instagram y Facebook consultadas el 20 de noviembre de 2026. Los enlaces se abren en cada red; esta web no carga sus contenidos ni rastreadores.</p></div></div></div></section>')


# ───────────── componentes dinámicos reutilizables (v3.2) ─────────────
ICONS.update({
    'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/>',
    'mail': '<rect x="3" y="5.5" width="18" height="13" rx="3"/><path d="m4 8 8 6 8-6"/>',
    'chat': '<path d="M20 11.5a8 8 0 0 1-11.6 7.2L4 20l1.3-4.4A8 8 0 1 1 20 11.5Z"/><path d="M9 8c0 4 3 7 7 7l1-2-3-1-1 1-2-2 1-1-1-3Z"/>',
    'pin': '<path d="M12 21s-6-5.5-6-10a6 6 0 0 1 12 0c0 4.5-6 10-6 10Z"/><circle cx="12" cy="11" r="2.2"/>',
    'wifi': '<path d="M3 9.5a13 13 0 0 1 18 0"/><path d="M6 13a8.5 8.5 0 0 1 12 0"/><path d="M9 16.5a4 4 0 0 1 6 0"/><circle cx="12" cy="19.5" r=".6"/>',
    'wc': '<circle cx="7.5" cy="5" r="1.8"/><path d="M7.5 8.5V15M5 11h5M6 20l1.5-5 1.5 5"/><circle cx="16.5" cy="5" r="1.8"/><path d="M14 9h5l-1 5h-3zM15.5 14v6M17.5 14v6"/>',
    'parking': '<rect x="4" y="4" width="16" height="16" rx="4"/><path d="M10 16V8h3a2.5 2.5 0 0 1 0 5h-3"/>',
    'card': '<rect x="3" y="6" width="18" height="12" rx="3"/><path d="M3 10.5h18M7 15h4"/>',
    'smile': '<circle cx="12" cy="12" r="9"/><path d="M8.5 14c1 1.5 2 2 3.5 2s2.5-.5 3.5-2"/><circle cx="9" cy="10" r=".6"/><circle cx="15" cy="10" r=".6"/>',
    'heart': '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10Z"/>',
    'access': '<circle cx="12" cy="4.5" r="1.6"/><path d="M12 8v6h5l2.5 5M12 11h5"/><path d="M8.5 13.5a5 5 0 1 0 7 6"/>',
    'camera': '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13.5" r="3.5"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
})


def ico(title, key=None):
    body = ICONS[key or TITLE_ICON.get(title, 'sparkle')]
    body = re.sub(r'<(path|circle|rect) ', r'<\1 pathLength="1" ', body)
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'


def _sid(sid):
    return f' id="{sid}"' if sid else ''


def pillars_sec(items, kick, h2, intro='', cls='pearl', sid='', dense=False, note=''):
    cards = ''
    for i, it in enumerate(items):
        t, p, k = it[0], it[1], it[2]
        href = it[3] if len(it) > 3 else None
        inner = f'<span class="ico" aria-hidden="true">{ico(t, k)}</span><h3>{t}</h3><p>{p}</p>'
        d = f' style="--d:{(i % 4) * .1}s"'
        if href:
            tgt = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
            cards += f'<a class="pillar pillar--link reveal" href="{href}"{tgt}{d}>{inner}<span class="go" aria-hidden="true">→</span></a>'
        else:
            cards += f'<article class="pillar reveal"{d}>{inner}</article>'
    c = ' dark grain' if cls == 'dark' else (f' {cls}' if cls else '')
    n = f'<p class="muted pillars-note">{note}</p>' if note else ''
    return (f'<section class="section{c}"{_sid(sid)}><div class="wrap"><div class="section-head reveal"><div>{kicker(kick)}<h2>{h2}</h2></div><p>{intro}</p></div>'
            f'<div class="pillars{" dense" if dense else ""}">{cards}</div>{n}</div></section>')


STEP_ICONS = {
    'peluqueria': ['chat', 'search', 'comb', 'sparkle'],
    'coloracion': ['search', 'palette', 'brush', 'sun'],
    'rubios': ['search', 'steps', 'layers', 'calendar'],
    'keratina': ['chat', 'search', 'smooth', 'shield'],
    'estetica': ['chat', 'check', 'lotus', 'sparkle'],
    'novias': ['camera', 'mirror', 'calendar', 'heart'],
    'inicio': ['chat', 'calendar', 'search', 'sparkle'],
    'galeria': ['camera', 'search', 'chat', 'sparkle'],
    'contacto': ['chat', 'calendar', 'camera', 'heart'],
}


STEP_IMGS = {
    'peluqueria': ['espejo-equipo', 'lavado', 'bob-rubio', 'castano-claro'],
    'coloracion': ['cobrizo', 'ritual-color', 'ondas-castano', 'moreno-liso'],
    'rubios': ['rubio-capas', 'rubio-ondas', 'balayage', 'bob-rubio'],
    'keratina': ['espejo-equipo', 'alisado-hialuronico', 'liso-oscuro', 'moreno-liso'],
    'estetica': ['unas-puesto', 'real-05', 'real-12', 'opi-jelly'],
    'novias': ['recogido-collage', 'novia-maquillaje', 'invitada-sombrero', 'novia-1'],
    'inicio': ['espejo-equipo', 'letrero-1', 'lavado', 'largo-reflejos'],
    'galeria': ['recogido-collage', 'balayage', 'espejo-equipo', 'largo-reflejos'],
    'contacto': ['espejo-equipo', 'salon-estanteria', 'recogido-collage', 'fachada-clienta-2'],
}


_PETAL = 'M60 64C43 56 38 30 60 6c22 24 17 50 0 58Z'


def _petals():
    tiers = [('pa', (-78, -54, 54, 78), 1.0), ('pb', (-32, 0, 32), .96), ('pc', (-14, 14), .8), ('pc', (0,), .66)]
    out, k = '', 0
    for cls, angles, s in tiers:
        for a in angles:
            out += f'<g class="petal {cls}" style="--a:{a}deg;--s:{s};--k:{k}"><path d="{_PETAL}"/><path class="vein" d="M60 60V24"/></g>'
            k += 1
    return out


def _stamens():
    out = ''
    for a in (-44, -26, -9, 9, 26, 44):
        out += f'<g class="sa" style="--a:{a}deg"><path d="M60 60V45"/><circle cx="60" cy="43.5" r="1.7"/></g>'
    return out


LOTUS = ('<svg viewBox="0 0 120 120" aria-hidden="true"><path class="calyx" d="M60 66C46 66 36 72 30 83 44 83 56 77 60 66Z"/><path class="calyx" d="M60 66C74 66 84 72 90 83 76 83 64 77 60 66Z"/>'
         + _petals() + '<g class="stam">' + _stamens() + '<circle class="pod" cx="60" cy="60" r="5.5"/></g></svg>')

LEAF = ('<svg viewBox="0 0 60 40" aria-hidden="true"><path class="blade" d="M2 38C6 16 28 2 58 3 56 24 34 40 2 38Z"/>'
        '<path class="vn" d="M2 38C20 28 38 16 56 5"/><path class="vn s" d="M15 31 17 21M25 26 29 16M35 20 41 12"/></svg>')


def step_cards(items, icons, photos=None):
    out = ''
    for i, (t, p) in enumerate(items):
        k = icons[i] if i < len(icons) else 'sparkle'
        side = 'l' if i % 2 == 0 else 'r'
        out += (f'<div class="vrow {side}" style="--i:{i}"><article class="vcard"><span class="vno" aria-hidden="true">0{i + 1}</span><h3>{t}</h3><p>{p}</p></article>'
                f'<div class="vstem" aria-hidden="true"><svg class="stem track" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M50 0C8 30 92 70 50 100"/></svg>'
                f'<svg class="stem grow" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M50 0C8 30 92 70 50 100"/></svg>'
                f'<span class="leaf la" style="--k:0">{LEAF}</span><span class="leaf lb" style="--k:1">{LEAF}</span>'
                f'<div class="bloom">{LOTUS}</div></div></div>')
    return out


def steps_sec(items, kick, h2, intro='', cta=None, cls='', sid='', icons=None, photos=None):
    st = step_cards(items, icons or STEP_ICONS['inicio'], photos or STEP_IMGS['inicio'])
    act = f'<div class="actions" style="justify-content:center">{cta}<a class="link" href="tel:{TEL}">Prefiero llamar <span>→</span></a></div>' if cta else ''
    c = f' {cls}' if cls else ''
    return (f'<section class="section{c}"{_sid(sid)}><div class="wrap"><div class="section-head reveal"><div>{kicker(kick)}<h2>{h2}</h2></div><p>{intro}</p></div><div class="vine" data-vine>{st}</div>{act}</div></section>')


def xp_sec(key, tabs, kick, h2, intro='', cls='dark grain', sid=''):
    tb = ''.join(f'<button class="xp-tab" role="tab" id="tab-{key}-{i}" aria-controls="pn-{key}-{i}" aria-selected="{"true" if i == 0 else "false"}"><span class="nr">0{i + 1}</span><span class="t">{t["title"]}</span><span class="bar"></span></button>' for i, t in enumerate(tabs))
    pn = ''.join(f'<article class="xp-panel{" is-active" if i == 0 else ""}" role="tabpanel" id="pn-{key}-{i}" aria-labelledby="tab-{key}-{i}"><figure class="arch">{img(t["img"], t["alt"])}</figure><div><h3>{t["title"]}</h3><p>{t["p1"]}</p>' + (f'<p>{t["p2"]}</p>' if t.get('p2') else '') + (f'<div class="actions" style="margin-top:26px">{t["cta"]}</div>' if t.get('cta') else '') + '</div></article>' for i, t in enumerate(tabs))
    return (f'<section class="section {cls}"{_sid(sid)}><div class="wrap"><div class="section-head reveal"><div>{kicker(kick)}<h2>{h2}</h2></div><p>{intro}</p></div>'
            f'<div class="xp reveal"><div class="xp-tabs" role="tablist" aria-label="{kick}">{tb}</div><div class="xp-panels">{pn}</div></div></div></section>')


# ───────────── horario ─────────────
# Fuente: ficha de Google del salón (consulta del 20/11/2026). Minutos desde las 0:00. 0 = domingo.
HOURS = {1: [(540, 1110)], 2: [(540, 1110)], 3: [(540, 1110)], 4: [(540, 1110)], 5: [(540, 1110)], 6: [(540, 840)], 0: []}
DAYS = [(1, 'Lunes'), (2, 'Martes'), (3, 'Miércoles'), (4, 'Jueves'), (5, 'Viernes'), (6, 'Sábado'), (0, 'Domingo')]


def hhmm(m):
    return f'{m // 60}:{m % 60:02d}'


def hours_json():
    return json.dumps({'tz': 'Atlantic/Canary', 'days': {str(k): [list(x) for x in v] for k, v in HOURS.items()}})


def open_badge():
    return '<a class="open-now" href="contacto.html#horario" data-open-badge data-state="unknown"><span class="dot" aria-hidden="true"></span><span class="txt">Horario de hoy</span></a>'


def week_card():
    s0, s1 = 7 * 60, 20 * 60
    rows = ''
    for d, name in DAYS:
        segs = HOURS[d]
        if segs:
            s, e_ = segs[0]
            bar = f'<i class="seg" style="left:{(s - s0) / (s1 - s0) * 100:.2f}%;width:{(e_ - s) / (s1 - s0) * 100:.2f}%"></i>'
            txt = f'{hhmm(s)} – {hhmm(e_)}'
        else:
            bar, txt = '', 'Cerrado'
        rows += f'<li data-day="{d}"><span class="dn">{name}<em class="today-tag">Hoy</em></span><span class="track">{bar}<b class="now" aria-hidden="true"></b></span><span class="ht">{txt}</span></li>'
    ticks = ''.join(f'<span style="left:{(h * 60 - s0) / (s1 - s0) * 100:.2f}%">{h}h</span>' for h in (8, 10, 12, 14, 16, 18))
    return (f'<div class="week" id="horario" data-s0="{s0}" data-s1="{s1}"><div class="week-status" data-open-status data-state="unknown"><span class="pulse" aria-hidden="true"></span><div><strong class="big">Consultando…</strong><span class="sub">Horario de Canarias</span></div></div>'
            f'<div class="scale" aria-hidden="true"><span></span><div class="ticks">{ticks}</div><span></span></div><ul>{rows}</ul>'
            f'<p class="muted">Horario según la ficha de Google del salón (consulta del 20 de noviembre de 2026). Se recomienda pedir cita, aunque también atienden sin cita si hay hueco. Confirma festivos y cambios con el equipo.</p></div>')


# ───────────── reseñas (10 extractos reales de Google) ─────────────
REVIEWS = [
    ('Noemí Perez diaz', 'Una tarde espectacular en Aura. Desde que llegué, el ambiente, el buen rollo y la atención hicieron que me sintiera súper cómoda y disfrutara muchísimo de la experiencia.', 'Ambiente'),
    ('Carmen Roig Sánchez', 'Estoy encantada con el tratamiento de keratina que me he hecho en Aura, el resultado es increíble, además de que me trataron como a una reina. Anabel y su equipo son unas grandes profesionales, lo recomiendo muchísimo.', 'Keratina'),
    ('Victoria Ponce', 'Servicio impecable. Me entendió a la perfección a la hora de hacerme el corte y me quedó ideal, además usa unos productos espectaculares. Ella es un encanto y una gran profesional.', 'Corte'),
    ('Asoria Toledo', 'La mejor peluquería de Tenerife. Productos de calidad y una atención y servicio 5 estrellas. La dueña, Anabel, es un encanto y ofrece siempre a sus clientes un trato inmejorable.', 'Trato'),
    ('Ithaisa Martín Bello', 'De las mejores peluquerías, trato cercano, profesionalidad y de 10 el resultado. Me llevé una mascarilla y noto el brillo que deja en el pelo con cada lavado.', 'Productos'),
    ('Atteneri Martín Bello', 'Llevé a mi hija a cortarse el pelo y el resultado fue increíble, nadie le había dejado el pelo tan bien. La recomendaré a todo el mundo sin dudarlo.', 'Corte infantil'),
    ('Ruth Avero Morales', 'Me hice la pedicura y manicura permanente para una boda y semanas después todavía estaban perfectas. Es una gran profesional y una persona encantadora.', 'Manicura'),
    ('Fany Ravelo', 'Profesionalidad, cercanía y mucho mimo en cada detalle.', 'Mimo'),
    ('kali cabrera avila', 'Muy profesionales. Puntualidad, buen trato, te aconsejan y te dejan exactamente lo que tú quieres. Sin lugar a dudas, vuelvo en breve.', 'Asesoramiento'),
    ('Conchi Cabello', 'Me encanta el trato y los productos orgánicos. Y no tardan en darte cita.', 'Productos orgánicos'),
]


def reviews():
    cards = ''.join(
        f'<article class="review"><span class="qmark" aria-hidden="true">“</span><blockquote>{t}</blockquote><div class="who"><span class="av" aria-hidden="true">{n[0].upper()}</span><div><strong>{n}</strong><span>Reseña de Google · {tag}</span></div></div></article>'
        for n, t, tag in REVIEWS)
    chips = ''.join(f'<span>{a} <b>{c}</b></span>' for a, c in [('productos', 3), ('mimo', 2), ('cita', 2), ('pelo rizado', 2), ('tratamiento', 2)])
    return (f'<section class="section dark grain reviews"><div class="wrap"><div class="section-head reveal"><div>{kicker("Lo que se siente, se cuenta")}<h2>El cariño<br><em>de quienes vuelven.</em></h2></div>'
            f'<a class="google-score" href="{GOOGLE}" target="_blank" rel="noopener"><strong>4,8<span>/5</span></strong><div><span class="stars" aria-label="Valoración de Google">★★★★★</span><br><span>32 reseñas en Google</span></div></a></div>'
            f'<div class="rev-chips reveal" aria-label="Temas que más mencionan en Google"><em>Lo que más mencionan:</em>{chips}</div>'
            f'<div class="review-track" tabindex="0" aria-label="Testimonios de Google">{cards}</div>'
            f'<div class="review-bottom"><p>Diez extractos de las 32 reseñas visibles en Google el 20 de noviembre de 2026. La valoración puede cambiar.</p><div>{ext(GOOGLE, "Leerlas todas en Google")}<button class="round-button" data-review="prev" aria-label="Reseña anterior">‹</button><button class="round-button" data-review="next" aria-label="Siguiente reseña">›</button></div></div></div></section>')


# ───────────── test «¿Qué necesita tu pelo hoy?» ─────────────
def quiz_sec():
    data = {s: {'title': v['title'], 'img': CARD[s], 'url': f'{s}.html'} for s, v in SERVICES.items()}
    return (f'<section class="section" id="test"><div class="wrap"><div class="section-head reveal"><div>{kicker("Tu test AURA")}<h2>¿Qué necesita<br><em>tu pelo hoy?</em></h2></div><p>Cuatro preguntas y te orientamos hacia el cuidado que mejor encaja. Es orientativo: el equipo lo confirma al verte.</p></div>'
            f'<div class="quiz reveal" data-quiz><div class="quiz-top"><span class="qcount">Pregunta 1 de 4</span><div class="qbar"><i></i></div><button type="button" class="link qback" hidden>← Atrás</button></div><div class="qbody" aria-live="polite"></div>'
            f'<noscript><p>Activa JavaScript para hacer el test o <a href="servicios.html">explora la carta de servicios</a>.</p></noscript></div>'
            f'<script type="application/json" id="quiz-data">{json.dumps(data, ensure_ascii=False)}</script></div></section>')


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
    faq = faqs([('¿Cómo puedo reservar mi primera visita?', 'Prepara tu mensaje de WhatsApp desde el botón de cita o llama al 642 63 69 70. El equipo confirmará contigo la disponibilidad y el servicio.'),
                ('¿Dónde está el salón?', 'En la avenida Inmaculada Concepción, 42, en El Sauzal, Tenerife. En Contacto encontrarás el enlace para preparar tu ruta.'),
                ('¿Qué cuidado me recomendáis?', 'Antes de elegir el servicio escuchamos lo que buscas y valoramos tu cabello o tus necesidades. Así podemos recomendarte una propuesta personalizada.'),
                ('¿Puedo consultar el presupuesto antes de ir?', 'Sí. Cuéntanos qué necesitas. Algunos trabajos requieren ver el cabello para concretar el importe y el tiempo de la cita.')])
    pillars = pillars_sec([
        ('Escuchamos primero', 'Tu pelo no es uno más: empezamos por escucharte y mirar cómo está tu cabello.', 'people'),
        ('Producto profesional', 'Líneas como Arkhē, Olaplex u OPI, explicadas con transparencia.', 'bottle'),
        ('Para todas las personas', 'Salón unisex, amigable con la comunidad LGBTQ+ y espacio seguro para personas trans, según su ficha en Google.', 'heart'),
        ('El cuidado continúa', 'Te orientamos para llevar la rutina a casa, sin pasos de más.', 'sparkle')],
        'Por qué AURA', 'Lo que nos<br><em>hace distintas.</em>', 'Cuatro ideas que guían cada cita.', cls='pearl')
    steps = steps_sec([
        ('Escríbenos o llámanos', 'Por WhatsApp o teléfono: cuéntanos qué necesitas.'),
        ('Confirmamos contigo', 'Disponibilidad, duración orientativa y presupuesto.'),
        ('Te escuchamos', 'Miramos tu cabello y acordamos la propuesta antes de empezar.'),
        ('Disfruta y llévate tu rutina', 'Resultado, consejos y cuidado para casa.')],
        'Tu primera visita', 'Así será<br><em>tu primera vez.</em>', 'Sin sorpresas: sabrás qué pasa en cada momento.', cta=book('Pedir mi primera cita'), sid='primera-visita')
    return h + ticker + manifesto + pillars + services + tf + space + story + bridal + brands + team + steps + reviews() + ig_wall() + quiz_sec() + faq


page('index', 'Belleza con raíces', 'Peluquería y estética orgánica en El Sauzal. Color, keratina, novias y bienestar con el cuidado cercano de AURA.', home())


# ───────────── páginas de servicio ─────────────
EXTRA = {
    'peluqueria': dict(
        tabs=['largo-reflejos', 'bob-miel', 'corte-pixie', 'lavado'],
        pillars=[('Unisex', 'Un salón para todas las personas, identidades y edades.'), ('Diagnóstico', 'Miramos tu cabello antes de decidir nada.'), ('Producto profesional', 'Líneas como Arkhē u Olaplex, explicadas.'), ('Rutina clara', 'Pasos útiles, sin añadir de más.')],
        steps=[('Conversación', 'Nos cuentas qué te gusta, qué te cuesta y qué cambio tienes en mente.'), ('Diagnóstico', 'Observamos textura, fibra y trabajos anteriores.'), ('Propuesta', 'Te explicamos el corte, el color o el cuidado antes de empezar.'), ('Acabado y rutina', 'Te mostramos cómo mantenerlo en casa con gestos sencillos.')]),
    'coloracion': dict(
        tabs=['cobrizo', 'ondas-castano', 'balayage', 'rubio-capas'],
        pillars=[('Sin amoniaco', 'Una de las opciones del salón, según el diagnóstico.'), ('Tono a medida', 'Partimos de tu base natural y de tus trabajos previos.'), ('Raíz y canas', 'Valoramos cobertura, matiz y crecimiento.'), ('Mantenimiento', 'Te orientamos para que el brillo dure entre citas.')],
        steps=[('Historia de tu cabello', 'Color actual, tintes anteriores y sensibilidad del cuero cabelludo.'), ('Elegimos el tono', 'Hablamos de matices, raíz y cuánto mantenimiento quieres.'), ('Aplicación y control', 'Seguimos el proceso del fabricante y revisamos el resultado.'), ('Cuidado posterior', 'Productos y tiempos para revisar raíz o matiz.')]),
    'rubios': dict(
        tabs=['rubio-ondas', 'bob-rubio', 'rubio-rizos', 'largo-reflejos'],
        pillars=[('Matices', 'Rubios cálidos, luminosos o más fríos, según tu piel.'), ('Por etapas', 'Los cambios grandes pueden requerir varias visitas.'), ('Fibra cuidada', 'Valoramos el estado del cabello antes de aclarar.'), ('Revisiones', 'Cada melena pide su propio ritmo de retoque.')],
        steps=[('Punto de partida', 'Color actual, porosidad y tratamientos anteriores.'), ('Plan', 'Acordamos si el cambio es en una visita o por etapas.'), ('Matiz y acabado', 'Afinamos los reflejos y la luminosidad final.'), ('Mantenimiento', 'Productos con pigmento: cuáles, cuánto y cada cuánto.')]),
    'keratina': dict(
        tabs=['letrero-liso', 'liso-oscuro', 'alisado-hialuronico', 'moreno-liso'],
        pillars=[('Menos encrespamiento', 'Una melena más manejable y un acabado pulido.'), ('Diagnóstico', 'Revisamos la fibra y los servicios anteriores.'), ('Sin promesas vacías', 'El acabado depende de tu cabello y del producto.'), ('Rutina posterior', 'Instrucciones claras según la fórmula aplicada.')],
        steps=[('Tu objetivo', 'Suavizar, controlar el encrespamiento o buscar un efecto más liso.'), ('Diagnóstico de fibra', 'Preguntamos por decoloraciones, alisados y otros servicios.'), ('Protocolo', 'Aplicamos el tratamiento acordado y realizamos el acabado indicado.'), ('Cuidados', 'Cuándo lavar, qué productos usar y qué evitar.')]),
    'estetica': dict(
        tabs=['opi-repair', 'real-12', 'unas-puesto', 'real-05'],
        pillars=[('Manos y pies', 'Manicura y pedicura con esmaltes como OPI o Masglo vegano.'), ('Maquillaje', 'Una propuesta personal para tu celebración.'), ('Hilo y láser', 'Consulta zonas, valoración y preparación.'), ('Bienestar', 'Presoterapia y cuidados con valoración previa.')],
        steps=[('Elegimos el cuidado', 'Cuéntanos qué te apetece o qué notas en tu piel.'), ('Valoración previa', 'Comentamos sensibilidades, antecedentes y preparación.'), ('Tu momento', 'Un rato tranquilo, con el tiempo acordado.'), ('Recomendaciones', 'Consejos para que el resultado te acompañe en casa.')]),
    'novias': dict(
        tabs=['recogido-1', 'novia-maquillaje', 'recogido-trenza', 'invitada-sombrero'],
        pillars=[('La prueba', 'Un espacio para decidir peinado y maquillaje con calma.'), ('Peinado', 'Recogidos con textura, torsiones y melenas sueltas.'), ('Maquillaje', 'Intensidad y protagonismo elegidos juntas.'), ('Invitadas', 'También preparamos a quienes te acompañan.')],
        steps=[('Referencias', 'Vestido, escote, accesorios y la forma de celebrar.'), ('Prueba', 'Exploramos el peinado y el maquillaje y hacemos ajustes.'), ('Planificación', 'Horarios, personas y duración, acordados con el salón.'), ('Tu día', 'Disfruta: los detalles ya están pensados.')]),
}
ICON = {0: '✦', 1: '◐', 2: '❋', 3: '✺'}

for slug, d in SERVICES.items():
    m = PAGE_MEDIA[slug]
    x = EXTRA[slug]
    h = hero(slug, d['eyebrow'], d['heading'], d['intro'], crumb=d['short'], chips=('Con cita', 'Diagnóstico personalizado', 'El Sauzal'))
    nav = ('<nav class="page-index page-nav" aria-label="En esta página"><div class="wrap"><a href="#filosofia">El cuidado</a><a href="#descubrir">Qué incluye</a><a href="#cita">Tu cita</a><a href="#opciones">Tu propuesta</a>'
           + ('<a href="#transformaciones">Antes y después</a>' if m['pairs'] else '') + '<a href="#trabajos">Trabajos reales</a><a href="#preguntas">Tus dudas</a>' + book('Consultar este servicio', d['title'], '') + '</div></nav>')
    words = ''.join(f'<span>{t}</span><b>✦</b>' for t, _ in x['pillars'])
    ticker = f'<div class="ticker" aria-hidden="true"><div>{words * 6}</div></div>'
    quote = f'<section class="quote-band emerald grain" id="filosofia"><div class="wrap reveal">{kicker("Nuestra forma de hacerlo")}<p>«{d["quote"]}»</p></div></section>'
    pillars = ('<section class="section pearl"><div class="wrap"><div class="section-head reveal"><div>' + kicker('Lo esencial') + '<h2>Lo que<br><em>encontrarás.</em></h2></div><p>Cuatro ideas que guían este cuidado en AURA.</p></div><div class="pillars">'
               + ''.join(f'<article class="pillar reveal" style="--d:{i * .1}s"><span class="ico" aria-hidden="true">{ico(t)}</span><h3>{t}</h3><p>{p}</p></article>' for i, (t, p) in enumerate(x['pillars'])) + '</div></div></section>')
    tabs = ''.join(f'<button class="xp-tab" role="tab" id="tab-{slug}-{i}" aria-controls="pn-{slug}-{i}" aria-selected="{"true" if i == 0 else "false"}"><span class="nr">0{i + 1}</span><span class="t">{t}</span><span class="bar"></span></button>' for i, (t, _, _) in enumerate(d['sections']))
    panels = ''.join(f'<article class="xp-panel{" is-active" if i == 0 else ""}" role="tabpanel" id="pn-{slug}-{i}" aria-labelledby="tab-{slug}-{i}"><figure class="arch">{img(x["tabs"][i], d["title"] + ": fotografía real de AURA")}</figure><div><h3>{t}</h3><p>{p1}</p><p>{p2}</p></div></article>' for i, (t, p1, p2) in enumerate(d['sections']))
    explorer = (f'<section class="section dark grain" id="descubrir"><div class="wrap"><div class="section-head reveal"><div>{kicker("Qué incluye")}<h2>El cuidado,<br><em>paso a paso.</em></h2></div><p>Elige un apartado o déjate llevar: cambia solo.</p></div>'
                f'<div class="xp reveal"><div class="xp-tabs" role="tablist" aria-label="Apartados de {d["short"]}">{tabs}</div><div class="xp-panels">{panels}</div></div></div></section>')
    steps = (f'<section class="section" id="cita"><div class="wrap"><div class="section-head reveal"><div>{kicker("Tu cita")}<h2>Así será<br><em>tu visita.</em></h2></div><p>Sin sorpresas: sabrás qué ocurre en cada momento.</p></div><div class="vine" data-vine>'
             + step_cards(x['steps'], STEP_ICONS[slug], STEP_IMGS[slug]) + '</div>'
             f'<div class="actions" style="justify-content:center">{book("Pedir mi cita", d["title"])}<a class="link" href="tel:{TEL}">Prefiero llamar <span>→</span></a></div></div></section>')
    opts = ''.join(f'<article class="option reveal" style="--d:{i * .1}s"><span class="nr">0{i + 1}</span><h3>{t}</h3><p>{p}</p><div class="row">{link(s, "Conocer más")}{book("Consultar mi caso", d["title"], "link")}</div></article>' for i, (t, p, s) in enumerate(d['options']))
    options = f'<section class="section pearl" id="opciones"><div class="wrap"><div class="section-head reveal"><div>{kicker("A tu medida")}<h2>¿Por dónde<br><em>empezamos?</em></h2></div></div><div class="options">{opts}</div><p class="budget-note">Cada propuesta se valora de forma personal. Consulta el tiempo y el presupuesto antes de confirmar tu cita.</p></div></section>'
    tf = transform(m['pairs']) if m['pairs'] else ''
    wk = (f'<section class="section" id="trabajos"><div class="wrap"><div class="section-head reveal"><div>{kicker("Hecho en AURA")}<h2>El cuidado<br><em>toma forma.</em></h2></div>{link("galeria", "Ver todos los trabajos")}</div>{works(m["works"], five=len(m["works"]) == 5)}</div></section>')
    others = [s for s in SERVICES if s != slug][:3]
    rel = f'<section class="section pearl"><div class="wrap"><div class="section-head reveal"><div>{kicker("Sigue explorando")}<h2>También te<br><em>puede gustar.</em></h2></div></div>{svc_cards(others)}</div></section>'
    page(slug, d['title'], d['intro'], h + nav + ticker + quote + pillars + explorer + steps + options + tf + wk + faqs(d['faq'], dark=True) + rel)


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
def _gtab(title, im, alt, p1, p2, cat):
    return dict(title=title, img=im, alt=alt, p1=p1, p2=p2, cta=f'<button class="btn" type="button" data-goto="{cat}">Ver fotos de {title.lower()}</button>')


page('galeria', 'Trabajos reales de AURA', 'Explora fotografías reales de color, recogidos, manicuras, productos y del equipo de AURA. Filtra y amplía cada trabajo.',
     hero('galeria', 'El álbum AURA', 'El álbum\nde AURA.', 'Melenas con movimiento, recogidos que cuentan historias y pequeños detalles hechos con cariño. Aquí puedes mirar de cerca nuestro trabajo.', crumb='Galería')
     + xp_sec('gal', [
         _gtab('Color', 'balayage', 'Balayage con ondas suaves', 'Balayage, reflejos, rubios y cobres: los trabajos de color que el salón publica, con sus antes y después.', 'Cada cabello parte de un punto distinto: úsalo como inspiración, no como promesa de resultado.', 'Color'),
         _gtab('Peinados', 'letrero-ondas', 'Ondas junto al letrero de AURA', 'Lisos con brillo, ondas, semirrecogidos y cortes con carácter.', 'Mira cómo se mueve el pelo, no solo cómo queda de frente.', 'Peinados'),
         _gtab('Novias', 'novia-1', 'Novia con peinado y maquillaje', 'Recogidos con textura, torsiones y melenas sueltas para novias e invitadas.', 'Si te gusta alguno, guárdalo: lo llevamos a la prueba.', 'Novias'),
         _gtab('Estética', 'real-12', 'Manicura en rosa vibrante', 'Manicuras, cuidado de manos y color para las uñas.', 'Esmaltes como OPI y Masglo vegano, entre otros.', 'Estética'),
         _gtab('Salón', 'salon-estanteria', 'Estantería de producto profesional', 'El espacio, el equipo y los productos: madera, plantas y luz cálida.', 'Así es el sitio donde te esperamos.', 'Salón')],
         'Elige por dónde empezar', 'Cinco formas<br><em>de mirar el álbum.</em>', 'Elige una categoría y salta directamente a sus fotos.', sid='descubrir')
     + f'<section class="section pearl" id="album"><div class="wrap"><div class="section-head reveal"><div>{kicker("Fotografías reales del salón")}<h2>Explora.<br><em>Encuentra tu inspiración.</em></h2></div><p>Pulsa una foto para verla de cerca y acceder a su publicación original.</p></div>{gallery(GALLERY)}<p class="gallery-disclaimer">Selección de fotografías publicadas por AURA en Instagram y en su ficha pública. El color puede variar según la luz y la pantalla.</p></div></section>'
     + pillars_sec([
         ('Fotos reales', 'Trabajos del salón, no imágenes de catálogo.', 'camera'),
         ('Con su origen', 'Cada foto enlaza a su publicación original.', 'check'),
         ('Antes y después sin retoque', 'Son mitades de la misma composición publicada por el salón.', 'layers'),
         ('Cada cabello es distinto', 'El resultado depende de tu cabello de partida.', 'strand')],
         'Cómo leer estas fotos', 'Con los ojos<br><em>bien abiertos.</em>', 'Cuatro claves para que la inspiración sea útil.', cls='')
     + transform(list(PAIRS))
     + steps_sec([
         ('Guarda referencias', 'Elige dos o tres fotos que te gusten, de esta galería o tuyas.'),
         ('Fíjate en el detalle', 'Largo, color, movimiento… no solo en la foto entera.'),
         ('Compártelas con el equipo', 'Envíalas por WhatsApp al pedir cita.'),
         ('Lo adaptamos a ti', 'Ajustamos la idea a tu cabello, tu rostro y tu rutina.')],
         'De la foto a tu pelo', 'Cómo elegir<br><em>tu look.</em>', 'Un camino sencillo desde la inspiración hasta la silla.', cta=book('Pedir mi cita'), cls='pearl', icons=STEP_ICONS['galeria'], photos=STEP_IMGS['galeria'])
     + ig_wall())


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
     + f'<section class="section" id="descubrir"><div class="wrap contact-grid"><div class="reveal">{kicker("Hablemos")}<h2>Una conversación<br><em>lo pone todo en marcha.</em></h2><a class="contact-phone" href="tel:{TEL}">642 63 69 70</a><p>Para pedir cita, consultar un servicio o preparar tu primera visita.</p><div class="actions">{book("Preparar mi solicitud")}<a class="link" href="tel:{TEL}">Prefiero llamar <span>→</span></a></div><p style="margin-top:34px"><a class="link" href="mailto:auraesteticasauzal@gmail.com">auraesteticasauzal@gmail.com</a></p>{social(labels=True, cls="contact-social")}<p style="margin-top:22px">{share_link("Compartir esta web por WhatsApp", "link")}</p></div>'
       f'<div class="visit-card reveal" style="--d:.15s"><h3>Ven a vernos</h3><address>Av. Inmaculada Concepción, 42<br>38360 El Sauzal<br>Santa Cruz de Tenerife</address>{open_badge()}<p style="margin-top:18px">Consulta más abajo el horario semanal. Se recomienda pedir cita; confirma la disponibilidad con el equipo.</p><div class="actions">{ext(GOOGLE, "Preparar mi ruta", "btn")}</div></div></div></section>'
     + f'<section class="section pearl"><div class="wrap"><div class="section-head reveal"><div>{kicker("Cuándo estamos")}<h2>Tu semana<br><em>en AURA.</em></h2></div><p>Mira de un vistazo si estamos abiertas ahora y cuándo abrimos.</p></div>{week_card()}</div></section>'
     + pillars_sec([
         ('Acceso adaptado', 'Entrada, aparcamiento, asientos y aseo adaptados para sillas de ruedas, y bucle magnético.', 'access'),
         ('Aparcamiento gratuito', 'Aparcamiento en la calle y parking gratuitos.', 'parking'),
         ('Wi‑Fi gratis', 'Para esperar con calma.', 'wifi'),
         ('Aseos unisex', 'Disponibles para la clientela.', 'wc'),
         ('Pago fácil', 'Tarjetas de crédito y débito, y pago con el móvil por NFC.', 'card'),
         ('Cita flexible', 'Se recomienda pedir cita, pero atienden sin cita si hay hueco.', 'calendar'),
         ('Apto para niños', 'Un salón adecuado para venir en familia.', 'smile'),
         ('Espacio seguro', 'Amigable con la comunidad LGBTQ+ y espacio seguro para personas trans.', 'heart')],
         'Todo pensado para ti', 'Para que venir<br><em>sea fácil.</em>', 'Información de la ficha del salón en Google.', cls='', dense=True,
         note='Según la ficha de Google del salón (consulta del 20 de noviembre de 2026). Si tienes una necesidad concreta, cuéntanosla al reservar.')
     + f'<section class="section pearl"><div class="wrap"><div class="section-head reveal"><div>{kicker("Así nos reconocerás")}<h2>Busca el letrero<br><em>de AURA.</em></h2></div><p>El rótulo «Peluquería y Estética Unisex» y el logo de AURA te indican la entrada, en la avenida Inmaculada Concepción.</p></div><div class="facade"><div class="reveal-img">{img("fachada-clienta-2", "Clienta en la entrada del salón, con el rótulo Peluquería y Estética Unisex")}</div><div class="reveal-img" style="--d:.12s">{img("real-13", "Fachada de AURA Organic Salón")}</div><div class="reveal-img" style="--d:.24s">{img("aniversario-arco", "Arco de globos en la puerta de AURA")}</div></div></div></section>'
     + f'<section class="section"><div class="wrap contact-grid"><div class="reveal">{kicker("Aquí estamos")}<h2>En el corazón<br><em>de El Sauzal.</em></h2><p style="margin-top:22px">Una visita para cuidarte en el norte de Tenerife. Consulta la ruta desde tu ubicación y organiza tu llegada con tiempo.</p></div><div class="map-card reveal" style="--d:.15s"><span class="pin">AURA</span><h3>Av. Inmaculada Concepción, 42</h3><p>38360 El Sauzal · Tenerife</p><div class="actions" style="margin-top:20px">{ext(GOOGLE, "Abrir en Google Maps", "btn")}</div></div></div></section>'
     + steps_sec([
         ('Cuéntanos qué necesitas', 'Indica el servicio o la duda. Si es color o keratina, menciona los trabajos anteriores de tu cabello.'),
         ('Acordamos los detalles', 'El equipo confirma disponibilidad, duración orientativa y presupuesto. La solicitud web no cierra una reserva por sí sola.'),
         ('Trae tus referencias', 'Fotos, ideas y, si es un evento, la fecha y los accesorios.'),
         ('Ven a tu momento', 'Si necesitas cambiar o cancelar, avisa con la mayor antelación posible.')],
         'Tu primera visita', 'Todo empieza<br><em>con una idea.</em>', 'Cuatro pasos, sin complicaciones.', cta=book('Preparar mi solicitud'), icons=STEP_ICONS['contacto'], photos=STEP_IMGS['contacto'])
     + faqs([('¿Se confirma la cita al rellenar el formulario?', 'No. El formulario prepara un mensaje que tú envías desde WhatsApp. La cita solo queda acordada cuando el equipo confirma día y hora.'),
             ('¿Puedo reservar por teléfono?', 'Sí. Llama al 642 63 69 70 para consultar disponibilidad y organizar tu visita.'),
             ('¿Hay aparcamiento y acceso adaptado?', 'Según la ficha de Google del salón, hay aparcamiento gratuito (en la calle y parking) y el local cuenta con acceso, aparcamiento, asientos y aseo adaptados para sillas de ruedas. Confirma cualquier necesidad concreta al reservar.'),
             ('¿Qué métodos de pago aceptáis?', 'Según la ficha de Google del salón: tarjetas de crédito y débito y pago con el móvil por NFC. Confirma al reservar si necesitas otra modalidad.'),
             ('¿Puedo ir sin cita?', 'Se recomienda pedir cita, pero la ficha indica que también atienden sin cita previa si hay hueco. Para no esperar, escríbenos antes.')], dark=True))


# ───────────── información y 404 ─────────────
page('informacion', 'Información y privacidad', 'Información de la propuesta web de AURA, fuentes de imágenes y funcionamiento de la solicitud por WhatsApp.',
     hero('informacion', 'Información de la web', 'Todo\nen su sitio.', 'Conoce cómo funciona esta demostración, de dónde viene el material y qué ocurre cuando preparas una solicitud de cita.', crumb='Información', cta=False)
     + f'<section class="section" id="descubrir"><div class="wrap legal"><h2>Sobre este proyecto</h2><p>Esta web es una propuesta de diseño para AURA Organic Salón. La identidad y las imágenes de marca han sido aportadas para el proyecto. Las fotografías de trabajos, equipo y salón se han seleccionado de las publicaciones públicas del salón.</p><h2>Fuentes y fotografías</h2><p>Se han consultado <a href="{INSTAGRAM}">Instagram</a>, <a href="{FACEBOOK}">Facebook</a>, la <a href="{GOOGLE}">ficha de Google</a> y <a href="{PA}">Páginas Amarillas</a>. La galería permite acceder a las fuentes originales. Las reseñas mostradas son extractos visibles en Google en la consulta del 20 de noviembre de 2026; no son opiniones inventadas. Las comparaciones de antes y después proceden de composiciones publicadas por el salón, separadas sin retoque.</p><h2>Solicitudes de cita</h2><p>El formulario funciona en tu navegador. No almacena tus datos ni los envía a una base de datos. Al preparar el mensaje verás su contenido y podrás abrir WhatsApp para revisarlo y enviarlo al teléfono del salón. WhatsApp aplica sus propias condiciones y política de privacidad.</p><h2>Servicios externos</h2><p>Esta web no incorpora analítica ni publicidad. Los enlaces a Google, Instagram, Facebook y WhatsApp se abren cuando tú los seleccionas. No se cargan sus reproductores, mapas ni herramientas de seguimiento dentro de esta página.</p><h2>Información comercial</h2><p>Los servicios, productos, horarios y precios deben confirmarse con el salón antes de reservar. Las descripciones ayudan a conocer la oferta; no garantizan un resultado idéntico para todas las personas. Antes de la publicación comercial definitiva deben incorporarse los datos legales completos del titular y validarse los contenidos con el negocio.</p><h2>Contacto</h2><p>AURA Organic Salón · Av. Inmaculada Concepción, 42, 38360 El Sauzal, Santa Cruz de Tenerife. Teléfono: <a href="tel:{TEL}">642 63 69 70</a>. Email de contacto publicado por el salón: <a href="mailto:auraesteticasauzal@gmail.com">auraesteticasauzal@gmail.com</a>.</p></div></section>')

page('404', 'No encontramos esta página', 'Vuelve a explorar los cuidados de AURA Organic Salón.',
     hero('404', 'Volvamos a encontrarnos', 'Sigue\ntu aura.', 'La página que buscas no está disponible. Vuelve al inicio o explora nuestra carta de cuidados.', cta=False,
          extra=f'<div class="actions">{link("index", "Volver al inicio", "btn")}{link("servicios", "Ver los servicios", "btn btn--ghost")}</div>')
     + '<div id="descubrir"></div>')

(OUT / 'robots.txt').write_text('User-agent: WhatsApp\nAllow: /\n\nUser-agent: facebookexternalhit\nAllow: /\n\nUser-agent: Twitterbot\nAllow: /\n\nUser-agent: *\nDisallow: /\n', encoding='utf8')
print(f'Generadas {len(list(OUT.glob("*.html")))} páginas HTML.')
