import os
import glob
import gzip

def main():
    count = 0
    old_tag = '<link rel="ai-catalog" type="application/json" href="/.well-known/ai-catalog.json">'
    new_tag = '<link rel="ai-catalog" type="application/ai-catalog+json" href="/.well-known/ai-catalog.json">'
    
    html_files = glob.glob('*.html')
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_tag in content:
            content = content.replace(old_tag, new_tag)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            print(f"[OK] Updated: {filepath}")
    
    print(f"Total HTML files updated: {count}")

    # Regenerar todos los .gz relevantes
    gz_targets = html_files + [
        'robots.txt',
        'js/main.js',
        'css/styles.css',
        'css/styles.min.css',
        'ai-catalog.json',
        'ard.json'
    ]
    
    for target in gz_targets:
        if os.path.exists(target):
            with open(target, 'rb') as f_in:
                data = f_in.read()
            gz_path = target + '.gz'
            with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
                f_out.write(data)
            print(f"[GZIP] Recompressed: {gz_path}")

    # Gzip for .well-known
    for wk in ['.well-known/ai-catalog.json', '.well-known/ard.json', '.well-known/mcp.json']:
        if os.path.exists(wk):
            with open(wk, 'rb') as f_in:
                data = f_in.read()
            gz_path = wk + '.gz'
            with gzip.open(gz_path, 'wb', compresslevel=9) as f_out:
                f_out.write(data)
            print(f"[GZIP] Recompressed: {gz_path}")

if __name__ == '__main__':
    main()
