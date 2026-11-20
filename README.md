# AURA Organic Salón

Web estática con 14 HTML, estilos y JavaScript compartidos, imágenes y tipografías locales. No requiere instalación para abrir `dist/index.html`.

Para servirla en local: `python -m http.server 5180 --bind 127.0.0.1 --directory dist` desde esta carpeta.

## Edición
- Textos de servicios y selección de galería: `content.py`.
- Composición de las páginas: `build.py`; regenerar con `python build.py`.
- Diseño: `dist/assets/site.css`.
- Interacciones: `dist/assets/site.js`.
- Comprobación de archivos, enlaces y anclas: `python verify.py`.

## Páginas
Inicio, servicios, peluquería, coloración, rubios, keratina, estética, novias, salón, galería, cuidados en casa, contacto, información y 404.

## Diseño e interacciones
Verde profundo, marfil, latón y nogal a partir de la identidad aportada. Fotografías reales del negocio. Cabeceras editoriales con foto propia en cada página, madera y vegetación, cinta en movimiento, entradas suaves al aparecer, menú de servicios con miniaturas, menú móvil, barra de contacto móvil, recomendaciones por objetivo, comparador, galería filtrable y visor con navegación de teclado, reseñas navegables y preguntas desplegables.

La solicitud prepara un mensaje de WhatsApp revisable, sin enviar nada automáticamente ni almacenar datos. El salón confirma disponibilidad y presupuesto. Se respeta la preferencia de reducir movimiento. No hay analítica, publicidad ni recursos de redes sociales incrustados.

## Estado de contenidos
Revisar `FUENTES-Y-CONTENIDOS.md`. Los horarios completos y datos legales del titular están pendientes de validación del negocio. La propuesta permanece sin indexación (`robots.txt`) y se entrega en acceso privado para revisión. No se ha modificado ningún perfil social del salón.
