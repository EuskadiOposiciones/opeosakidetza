# PostHog — activación V5

La V5 está preparada para PostHog Cloud EU en modo cookieless.

## Antes de publicar

1. Abre el proyecto de PostHog en `eu.posthog.com`.
2. En **Settings**, busca **Cookieless tracking** y actívalo para el proyecto.
   - Es obligatorio: PostHog ignora los eventos enviados con `cookieless_mode: always` si esta opción del proyecto no está habilitada.
3. No actives Session Replay para esta fase.

## Publicación

Sube todo el contenido de esta carpeta a la raíz del repositorio `opeosakidetza`, reemplazando los archivos existentes. Conserva cualquier archivo `google*.html` de verificación de Search Console que ya exista en GitHub y no forme parte de este paquete.

## Prueba

Tras desplegar GitHub Pages:

1. Abre la portada.
2. Entra en una categoría.
3. Pulsa una fuente oficial.
4. Pulsa un CTA de Google Play.

Después se pueden comprobar en PostHog: `$pageview`, `category_link_clicked`, `official_source_clicked`, `google_play_clicked` y `scroll_depth_reached`.
