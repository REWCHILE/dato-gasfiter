import os
import glob
import re
import gzip

def update_logos():
    html_files = sorted(glob.glob('*.html'))
    print(f"Updating logos across {len(html_files)} HTML files...")
    
    for fname in html_files:
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig = content
        
        # Replace header brand-logo
        # Match <img ... alt="Logotipo DATO GASFITER" ...>
        content = re.sub(
            r'<img\s+src="[^"]*dato-gasfiter-logotipo[^"]*"\s+(?:srcset="[^"]*"\s+sizes="[^"]*"\s+)?alt="Logotipo DATO GASFITER"\s+width="52"\s+height="52">',
            r'<img src="/assets/images/logo.webp" alt="Logotipo DATO GASFITER" width="52" height="52">',
            content
        )
        
        # Replace drawer brand logo
        content = re.sub(
            r'<img\s+src="[^"]*dato-gasfiter-logotipo[^"]*"\s+alt="DATO GASFITER"\s+width="40"\s+height="40"\s+decoding="async">',
            r'<img src="/assets/images/logo.webp" alt="DATO GASFITER" width="40" height="40" decoding="async">',
            content
        )

        # Replace footer brand logo
        content = re.sub(
            r'<img\s+src="[^"]*dato-gasfiter-logotipo[^"]*"\s+alt="DATO GASFITER"\s+width="48"\s+height="48"\s+loading="lazy"\s+decoding="async">',
            r'<img src="/assets/images/logo.webp" alt="DATO GASFITER" width="48" height="48" loading="lazy" decoding="async">',
            content
        )
        
        # General replacement for any remaining old logo img src
        content = re.sub(
            r'src="/assets/images/dato-gasfiter-logotipo-(?:96|104|2025-150-150)\.webp"',
            r'src="/assets/images/logo.webp"',
            content
        )

        if content != orig:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Logos updated in {fname}")
        else:
            print(f"[NOOP] No logo changes in {fname}")

def update_index_lcp():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Change font-display:swap to font-display:optional for zero font-swap delay
    html = html.replace("font-display:swap;", "font-display:optional;")

    # Ensure font preloads are at top of head with fetchpriority="high"
    # and fix hero preload slash
    html = html.replace('href="assets/images/hero-bg-poster-mobile.webp"', 'href="/assets/images/hero-bg-poster-mobile.webp"')
    html = html.replace('href="assets/images/hero-bg-poster.webp"', 'href="/assets/images/hero-bg-poster.webp"')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("[OK] index.html LCP font-display:optional and preloads updated")

def recompress_gz():
    import glob
    targets = glob.glob('*.html') + [
        'robots.txt',
        'js/main.js',
        'css/styles.css',
        'css/styles.min.css',
        'assets/images/logo.webp'
    ]
    for target in targets:
        if os.path.exists(target):
            with open(target, 'rb') as f_in:
                data = f_in.read()
            gz_path = target + '.gz'
            with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
                f_out.write(data)
            print(f"[GZIP] {gz_path}")

if __name__ == '__main__':
    update_logos()
    update_index_lcp()
    recompress_gz()
