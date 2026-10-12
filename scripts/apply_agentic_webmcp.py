import os
import re
import gzip

def apply_agentic():
    # 1. Actualizar index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Enlaces de descubrimiento de catálogo de IA
    old_link = '<link rel="prefetch" href="/css/styles.min.css?v=4.0" as="style">'
    new_discovery_links = old_link + """\n
  <!-- Descubrimiento Agéntico y Protocolo de Modelos de IA (WebMCP / ARD 4/4) -->
  <link rel="ai-catalog" type="application/json" href="/.well-known/ai-catalog.json">
  <link rel="agent-manifest" type="text/markdown" href="/llms.txt">
  <link rel="model-context" type="text/plain" href="/llms.txt">"""

    if old_link in html and 'rel="ai-catalog"' not in html:
        html = html.replace(old_link, new_discovery_links)
        print("[OK] index.html: Enlaces rel='ai-catalog' y rel='agent-manifest' agregados")

    # Formulario declarativo WebMCP
    old_form = '<form class="quick-form quick-quote-form">'
    new_form = '<form class="quick-form quick-quote-form" toolname="solicitar_gasfiter" tooldescription="Formulario para solicitar presupuesto o asistencia técnica de gasfiter SEC a domicilio">'

    if old_form in html:
        html = html.replace(old_form, new_form)
        html = html.replace('id="serviceSelect" name="service" required', 'id="serviceSelect" name="service" toolparamdescription="Tipo de servicio de gasfitería" required')
        html = html.replace('id="comunaSelect" name="zone" required', 'id="comunaSelect" name="zone" toolparamdescription="Comuna o ciudad del cliente en Chile" required')
        html = html.replace('id="clientName" name="name" placeholder="Ej: Marcela González" required', 'id="clientName" name="name" placeholder="Ej: Marcela González" toolparamdescription="Nombre del cliente solicitante" required')
        html = html.replace('id="problemDetail" name="detail" placeholder="Ej: Calefont se apaga / Fuga bajo cerámica" required', 'id="problemDetail" name="detail" placeholder="Ej: Calefont se apaga / Fuga bajo cerámica" toolparamdescription="Detalle o descripción de la falla técnica" required')
        print("[OK] index.html: Atributos declarativos WebMCP agregados al formulario")

    # Cache bust de script js
    html = html.replace('js/main.js?v=3.6', 'js/main.js?v=3.7')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # 2. Actualizar los demás HTML
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']
    for fname in html_files:
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False
        if 'rel="ai-catalog"' not in content:
            # Insertar antes del cierre de head o tras el css
            target_css = '<link rel="stylesheet" href="/css/styles.min.css?v=4.0">'
            if target_css in content:
                content = content.replace(
                    target_css,
                    target_css + '\n  <link rel="ai-catalog" type="application/json" href="/.well-known/ai-catalog.json">\n  <link rel="agent-manifest" type="text/markdown" href="/llms.txt">'
                )
                changed = True

        if 'main.js?v=3.6' in content:
            content = content.replace('main.js?v=3.6', 'main.js?v=3.7')
            changed = True

        if changed:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] {fname}: Catálogo agéntico y cache bust actualizados")

    # 3. Regenerar todos los .gz (nivel 9)
    gz_targets = [f for f in os.listdir('.') if f.endswith('.html')] + [
        'js/main.js',
        'css/styles.css',
        'css/styles.min.css',
        'robots.txt'
    ]

    for target in gz_targets:
        if os.path.exists(target):
            with open(target, 'rb') as f_in:
                data = f_in.read()
            gz_path = target + '.gz'
            with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
                f_out.write(data)
            print(f"[OK] Gzip: {gz_path}")

if __name__ == '__main__':
    apply_agentic()
