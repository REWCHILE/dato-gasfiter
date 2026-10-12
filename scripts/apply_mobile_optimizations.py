import os
import re
import gzip

def optimize():
    # 1. Leer CSS minificado
    with open('css/styles.min.css', 'r', encoding='utf-8') as f:
        min_css = f.read()

    # 2. Actualizar index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Sustitución de cabecera de fuentes y estilos inline
    old_head_start = '  <!-- Preconnect y Carga Optimizada de Fuentes (PageSpeed 100/100) -->'
    old_head_end = '<link rel="prefetch" href="/css/styles.min.css?v=3.9" as="style">'

    start_idx = html.find(old_head_start)
    end_idx = html.find(old_head_end)

    if start_idx != -1 and end_idx != -1:
        end_idx += len(old_head_end)
        new_head_block = """  <!-- Preload Prioritario de Fuentes Locales (0ms Terceros, 0ms Latencia DNS) -->
  <link rel="preload" href="/assets/fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin fetchpriority="high">
  <link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>

  <!-- Hoja de Estilos Principal Inline (0ms Bloqueo de Renderizado - PageSpeed 100/100) -->
  <style>""" + min_css + """</style>
  <link rel="prefetch" href="/css/styles.min.css?v=4.0" as="style">"""
        html = html[:start_idx] + new_head_block + html[end_idx:]
        print("[OK] index.html: Cabecera y estilos inline actualizados con fuentes locales")
    else:
        print("[WARN] No se encontro el bloque de cabecera en index.html")

    # Sustitución de bloques service-features a <ul><li> para aplanar el DOM (11 -> 8 niveles)
    service_pattern = re.compile(
        r'<div class="service-features">\s*'
        r'<div class="service-feature-item">\s*'
        r'<svg[^>]*>.*?</svg>\s*'
        r'<span>(.*?)</span>\s*'
        r'</div>\s*'
        r'<div class="service-feature-item">\s*'
        r'<svg[^>]*>.*?</svg>\s*'
        r'<span>(.*?)</span>\s*'
        r'</div>\s*'
        r'</div>',
        re.DOTALL
    )

    def replace_service(m):
        item1 = m.group(1).strip()
        item2 = m.group(2).strip()
        return (
            f'<ul class="service-features">\n'
            f'                <li class="service-feature-item">{item1}</li>\n'
            f'                <li class="service-feature-item">{item2}</li>\n'
            f'              </ul>'
        )

    html, count = service_pattern.subn(replace_service, html)
    print(f"[OK] index.html: {count} bloques service-features aplanados a <ul><li>")

    # Actualizar versión de script
    html = html.replace('js/main.js?v=3.5', 'js/main.js?v=3.6')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # 3. Actualizar los demás archivos HTML (quitar fuentes externas de Google y usar locales)
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']
    google_fonts_pattern = re.compile(
        r'\s*<!-- Preconnect y Carga Optimizada de Fuentes.*?-->\s*'
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*'
        r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*'
        r'<link rel="preload" as="style" href="https://fonts\.googleapis\.com/css2\?[^"]*">\s*'
        r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*"[^>]*>\s*'
        r'<noscript>\s*<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">\s*</noscript>',
        re.DOTALL
    )

    local_fonts_block = """
  <!-- Preload Prioritario de Fuentes Locales (0ms Terceros) -->
  <link rel="preload" href="/assets/fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>"""

    for fname in html_files:
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, n = google_fonts_pattern.subn(local_fonts_block, content)
        new_content = new_content.replace('main.js?v=3.5', 'main.js?v=3.6')
        new_content = new_content.replace('styles.min.css?v=3.8', 'styles.min.css?v=4.0')
        new_content = new_content.replace('styles.min.css?v=3.9', 'styles.min.css?v=4.0')

        if new_content != content:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"[OK] {fname}: Fuentes de Google eliminadas y reemplazadas por locales")

    # 4. Comprimir a .gz (nivel 9) para Nginx gzip_static
    gz_targets = [f for f in os.listdir('.') if f.endswith('.html')] + [
        'js/main.js',
        'css/styles.css',
        'css/styles.min.css'
    ]

    for target in gz_targets:
        if os.path.exists(target):
            with open(target, 'rb') as f_in:
                data = f_in.read()
            gz_path = target + '.gz'
            with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
                f_out.write(data)
            print(f"[OK] {gz_path} ({len(data)} -> {os.path.getsize(gz_path)} bytes)")

if __name__ == '__main__':
    optimize()
