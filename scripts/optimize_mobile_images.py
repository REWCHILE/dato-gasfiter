import os
import re
import gzip
from PIL import Image

def generate_optimized_images():
    services = [
        'servicio-reparacion-calefont-sec',
        'servicio-deteccion-fugas-agua-geofono',
        'servicio-fugas-gas-instalacion-sec',
        'servicio-destape-alcantarillado-maquina',
        'servicio-gasfiter-emergencia-urgencias',
        'servicio-informe-tecnico-seguros-sec'
    ]
    
    for name in services:
        src = f'assets/images/{name}.webp'
        if not os.path.exists(src):
            continue
        img = Image.open(src)
        
        # 400w version for mobile
        w_400 = 400
        h_400 = int(img.height * (400 / img.width))
        i_400 = img.resize((w_400, h_400), Image.Resampling.LANCZOS)
        p_400 = f'assets/images/{name}-400.webp'
        i_400.save(p_400, 'WEBP', quality=74, method=6)
        
        # 600w version
        w_600 = 600
        h_600 = int(img.height * (600 / img.width))
        i_600 = img.resize((w_600, h_600), Image.Resampling.LANCZOS)
        p_600 = f'assets/images/{name}-600.webp'
        i_600.save(p_600, 'WEBP', quality=76, method=6)
        
        print(f"[IMG] {name}: 400w={os.path.getsize(p_400)/1024:.1f}K, 600w={os.path.getsize(p_600)/1024:.1f}K")

def update_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update CSS in index.html
    old_css = '.service-image-wrap img{width:100%;height:100%;object-fit:cover;transition:transform 0.5s ease}'
    new_css = '.service-image-wrap picture{display:block;width:100%;height:100%}.service-image-wrap img,.service-image-wrap picture img{width:100%;height:100%;object-fit:cover;transition:transform 0.5s ease}'
    if old_css in html and '.service-image-wrap picture' not in html:
        html = html.replace(old_css, new_css)
        print("[CSS] index.html: added .service-image-wrap picture styling")

    # 2. Wrap the 6 service cards in <picture>
    services = [
        'servicio-reparacion-calefont-sec',
        'servicio-deteccion-fugas-agua-geofono',
        'servicio-fugas-gas-instalacion-sec',
        'servicio-destape-alcantarillado-maquina',
        'servicio-gasfiter-emergencia-urgencias',
        'servicio-informe-tecnico-seguros-sec'
    ]

    for s in services:
        pattern = re.compile(r'(<div class="service-image-wrap">\s*)(<img src="assets/images/' + s + r'\.webp"[^>]+>)')
        match = pattern.search(html)
        if match:
            wrap_open = match.group(1)
            img_tag = match.group(2)
            # Avoid double picture
            if '<picture>' not in wrap_open:
                picture_block = f"""<picture>\n                <source media="(max-width: 768px)" srcset="assets/images/{s}-400.webp" width="400" height="300">\n                {img_tag}\n              </picture>"""
                html = html.replace(match.group(0), wrap_open + picture_block)
                print(f"[HTML] index.html: wrapped {s} in <picture>")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

def update_external_css():
    rule = '\n.service-image-wrap picture{display:block;width:100%;height:100%}\n.service-image-wrap picture img{width:100%;height:100%;object-fit:cover;transition:transform 0.5s ease}\n'
    for css_file in ['css/styles.css', 'css/styles.min.css']:
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if '.service-image-wrap picture' not in content:
                content += rule
                with open(css_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[CSS] Updated {css_file}")

def recompress_all_gz():
    import glob
    targets = glob.glob('*.html') + [
        'robots.txt',
        'js/main.js',
        'css/styles.css',
        'css/styles.min.css'
    ]
    for target in targets:
        if os.path.exists(target):
            with open(target, 'rb') as f_in:
                data = f_in.read()
            gz_path = target + '.gz'
            with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
                f_out.write(data)
            print(f"[GZIP] Recompressed: {gz_path}")

if __name__ == '__main__':
    generate_optimized_images()
    update_index_html()
    update_external_css()
    recompress_all_gz()
