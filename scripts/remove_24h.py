import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# 1. Update footer in all HTML files
footer_old = '<p style="margin-bottom: 0.35rem;">⏱ <strong>Horario:</strong> Turno Continuo 24 Horas</p>'
footer_new = '<p style="margin-bottom: 0.35rem;">⏱ <strong>Horario:</strong> Lunes a Domingo • Turnos de Emergencia</p>'

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if footer_old in content:
        content = content.replace(footer_old, footer_new)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Updated footer in {f}')

# 2. Update gasfiter-emergencia-urgencias.html and gasfiter-emergencia-24-7.html
target_files = ['gasfiter-emergencia-urgencias.html', 'gasfiter-emergencia-24-7.html']
for tf in target_files:
    if os.path.exists(tf):
        with open(tf, 'r', encoding='utf-8') as file:
            content = file.read()
        
        content = content.replace(
            'Turno de Urgencia 24 Horas • Respuesta en 30-45 Minutos',
            'Atención de Emergencias y Urgencias • Respuesta en 30-45 Minutos'
        )
        content = content.replace(
            'Móviles taller en terreno las 24 horas en <strong>Santiago y la V Región Costa</strong>.',
            'Móviles taller en terreno disponibles de inmediato en <strong>Santiago y la V Región Costa</strong>.'
        )
        content = content.replace(
            'Sí. Nuestra central técnica opera las 24 horas del día, los 7 días de la semana y los 365 días del año de forma ininterrumpida',
            'Sí. Nuestra central técnica atiende de lunes a domingo y días festivos de forma ininterrumpida. Contamos con técnicos de guardia para emergencias de agua y gas'
        )
        
        with open(tf, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Updated emergency content in {tf}')

# 3. Update informes-tecnicos-sec.html
if os.path.exists('informes-tecnicos-sec.html'):
    with open('informes-tecnicos-sec.html', 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace(
        'dentro de las 12 a 24 horas hábiles siguientes.',
        'dentro del mismo día hábil.'
    )
    with open('informes-tecnicos-sec.html', 'w', encoding='utf-8') as file:
        file.write(content)
    print('Updated informes-tecnicos-sec.html')

# 4. Update index.html comments
if os.path.exists('index.html'):
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('BANNER DE EMERGENCIA 24 HORAS', 'BANNER DE EMERGENCIAS Y URGENCIAS')
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(content)
    print('Updated index.html comments')

# 5. Update fullllm.txt
if os.path.exists('fullllm.txt'):
    with open('fullllm.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('las 24 horas y peritajes', 'atención de urgencias y peritajes')
    content = content.replace('24 horas al día, 365 días del año', 'Lunes a domingo, festivos y fines de semana con servicio de urgencia inmediata')
    with open('fullllm.txt', 'w', encoding='utf-8') as file:
        file.write(content)
    print('Updated fullllm.txt')
