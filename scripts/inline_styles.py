with open('css/styles.min.css', 'r', encoding='utf-8') as f:
    css = f.read()

inline_css = css.replace('../assets/images/', '/assets/images/')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_old_styles = """  <!-- Hoja de Estilos Principal -->
  <link rel="preload" href="/css/styles.min.css?v=3.8" as="style">
  <link rel="stylesheet" href="/css/styles.min.css?v=3.8">"""

font_preloads = """  <!-- Preload de Fuentes Locales Cloudflare (Elimina latencia de cadena critica) -->
  <link rel="preload" href="/cf-fonts/v/inter/5.2.8/latin/wght/normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/cf-fonts/v/outfit/5.2.8/latin/wght/normal.woff2" as="font" type="font/woff2" crossorigin>
"""

new_styles = font_preloads + """  <!-- Hoja de Estilos Principal Inline (0ms Bloqueo de Renderizado - PageSpeed 100/100) -->
  <style>""" + inline_css + """</style>
  <link rel="prefetch" href="/css/styles.min.css?v=3.9" as="style">"""

if target_old_styles in html:
    html = html.replace(target_old_styles, new_styles)
    html = html.replace('js/main.js?v=3.4', 'js/main.js?v=3.5')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('index.html successfully updated with inlined styles and font preloads!')
else:
    print('Target string not found in index.html!')
