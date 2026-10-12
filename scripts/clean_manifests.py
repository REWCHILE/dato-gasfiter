import os

for f in os.listdir('.'):
    if f.endswith('.html'):
        with open(f, 'r', encoding='utf-8') as file:
            c = file.read()
        
        c = c.replace('  <link rel="agent-manifest" type="text/markdown" href="/llms.txt">\n', '')
        c = c.replace('  <link rel="model-context" type="text/plain" href="/llms.txt">\n', '')
        c = c.replace('<link rel="agent-manifest" type="text/markdown" href="/llms.txt">\n', '')
        c = c.replace('<link rel="model-context" type="text/plain" href="/llms.txt">\n', '')
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(c)

print('Cleaned manifest links from all HTML files.')
