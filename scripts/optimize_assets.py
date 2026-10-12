import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Header logo
    content = content.replace(
        '<img src="/assets/images/dato-gasfiter-logotipo-2025-150-150.png" alt="Logotipo DATO GASFITER" width="52" height="52">',
        '<img src="/assets/images/dato-gasfiter-logotipo-2025-150-150.webp" alt="Logotipo DATO GASFITER" width="52" height="52">'
    )

    # 2. Drawer logo
    content = content.replace(
        '<img src="/assets/images/dato-gasfiter-logotipo-2025-150-150.png" alt="DATO GASFITER" width="40" height="40" decoding="async">',
        '<img src="/assets/images/dato-gasfiter-logotipo-104.webp" alt="DATO GASFITER" width="40" height="40" decoding="async">'
    )

    # 3. Footer logo
    content = content.replace(
        '<img src="/assets/images/dato-gasfiter-logotipo-2025-150-150.png" alt="DATO GASFITER" width="48" height="48">',
        '<img src="/assets/images/dato-gasfiter-logotipo-104.webp" alt="DATO GASFITER" width="48" height="48" loading="lazy" decoding="async">'
    )

    # 4. Stylesheet cache bust
    content = content.replace('styles.min.css?v=3.7', 'styles.min.css?v=3.8')

    # 5. Script cache bust
    content = content.replace('main.js?v=3.3', 'main.js?v=3.4')

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated {len(html_files)} HTML files successfully.")
