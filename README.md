# AURA Organic Salón

Web estática con 14 HTML, estilos y JavaScript compartidos, imágenes y tipografías locales. No requiere instalación para abrir `dist/index.html`.

Para servirla en local: `python -m http.server 5180 --bind 127.0.0.1 --directory dist` desde esta carpeta.

## Edición
- Textos de servicios y selección de galería: `content.py`.
- Composición de las páginas: `build.py`; regenerar con `python build.py`.
- Diseño: `dist/assets/direction.css`.
- Interacciones: `dist/assets/site.js` y `dist/assets/art.js`.
- Composición de portada y ornamentos: `art_direction.py`.
- Comprobación de archivos, enlaces y anclas: `python verify.py`.

## Páginas
Inicio, servicios, peluquería, coloración, rubios, keratina, estética, novias, salón, galería, cuidados en casa, contacto, información y 404.

## Rediseño visual v2

La primera propuesta fue rechazada por el usuario por resultar demasiado genérica. Esta versión sustituye completamente su dirección visual, sin acumular correcciones sobre la hoja de estilos anterior.

- Bricolage Grotesque, DM Sans y Caveat variables y locales; sustituyen Cormorant y Manrope.
- Portada escénica, madera oscura, fotografía real a gran escala, firma manuscrita, verde bosque, latón y verde luminoso.
- Explorador de servicios con paneles fotográficos y navegación de teclado.
- Ornamentos botánicos dibujados en SVG, flor geométrica, sello de pétalos animado y textura de grano.
- Novias como composición de fotografías impresas; equipo sobre madera, álbum asimétrico y nuevas cabeceras en todos los HTML.
- Botones metálicos con barrido de luz, movimiento suave al cursor y onda de pulsación. Fotos con iluminación al cursor, desplazamiento leve y entradas al aparecer.
- Capas decorativas fuera del texto, efectos desactivados con reducción de movimiento y adaptados a pantallas táctiles.
- La ilustración de depilación con hilo se identifica como tal y reemplaza la fotografía de manos que no correspondía al texto.

## Diseño e interacciones
Verde profundo, marfil, latón y nogal a partir de la identidad aportada. Fotografías reales del negocio. Cabeceras editoriales con foto propia en cada página, madera y vegetación, cinta en movimiento, entradas suaves al aparecer, menú de servicios con miniaturas, menú móvil, barra de contacto móvil, recomendaciones por objetivo, comparador, galería filtrable y visor con navegación de teclado, reseñas navegables y preguntas desplegables.

La solicitud prepara un mensaje de WhatsApp revisable, sin enviar nada automáticamente ni almacenar datos. El salón confirma disponibilidad y presupuesto. Se respeta la preferencia de reducir movimiento. No hay analítica, publicidad ni recursos de redes sociales incrustados.

## Estado de contenidos
Revisar `FUENTES-Y-CONTENIDOS.md`. Los horarios completos y datos legales del titular están pendientes de validación del negocio. La propuesta permanece sin indexación (`robots.txt`) y se entrega en acceso privado para revisión. No se ha modificado ningún perfil social del salón.
