from pathlib import Path
import re, sys
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
CATEGORY_BATTERY = {
    'enfermeria-salud-mental': '200',
    'matrona': '200',
    'auxiliar-farmacia': '300',
    'psicologia-clinica': '200',
    'tecnico-especialista-informatica': '300',
    'oficial-mantenimiento-instalaciones': '300',
    'tecnico-superior-juridico': '200',
    'tecnico-medio-administracion-gestion': '200',
    'tecnico-superior-organizacion': '200',
    'trabajador-social': '200',
    'tecnico-superior-economico': '200',
    'cocinero': '300',
    'anatomia-patologica-citologia': '200',
    'enfermeria-salud-laboral': '200',
    'medico-emergencias': '200',
}
SEO = {
    'index.html': ('Test Osakidetza 2026 | Baterías oficiales, fechas y categorías', 'OPE Osakidetza 2026: baterías, fechas y test por categoría', 'https://euskadioposiciones.com/opeosakidetza/'),
    'fase-2-osakidetza-2026/index.html': ('Fase II OPE Osakidetza 2026 | 41 categorías y fechas de examen', 'Fase II OPE Osakidetza 2026', 'https://euskadioposiciones.com/opeosakidetza/fase-2-osakidetza-2026/'),
    'radiodiagnostico/index.html': ('Test Radiodiagnóstico Osakidetza 2026 | 500 preguntas', 'Test Radiodiagnóstico Osakidetza 2026: batería de 500 preguntas', 'https://euskadioposiciones.com/opeosakidetza/radiodiagnostico/'),
    'cocinero/index.html': ('Cocinero/a Osakidetza 2026 | 15 plazas', 'Cocinero/a Osakidetza 2026: 15 plazas y Fase II', 'https://euskadioposiciones.com/opeosakidetza/cocinero/'),
    'enfermeria-salud-mental/index.html': ('Enfermería Salud Mental Osakidetza 2026 | 95 plazas', 'Enfermero/a Salud Mental Osakidetza 2026: 95 plazas y Fase II', 'https://euskadioposiciones.com/opeosakidetza/enfermeria-salud-mental/'),
}
errors=[]

def text(path):
    p=ROOT/path
    if not p.exists():
        errors.append(f'missing file {path}')
        return ''
    return p.read_text(encoding='utf-8')

# SEO freeze on representative winners and entry pages.
for path, (title, h1, canonical) in SEO.items():
    s=text(path)
    soup=BeautifulSoup(s, 'html.parser')
    got_title=soup.title.get_text(strip=True) if soup.title else ''
    got_h1=soup.h1.get_text(' ', strip=True) if soup.h1 else ''
    link=soup.find('link', rel='canonical')
    got_canonical=link.get('href','') if link else ''
    if got_title != title: errors.append(f'{path}: title changed: {got_title!r}')
    if got_h1 != h1: errors.append(f'{path}: H1 changed: {got_h1!r}')
    if got_canonical != canonical: errors.append(f'{path}: canonical changed: {got_canonical!r}')

# Every current Fase II common-only page gets a practical bridge.
for slug,battery in CATEGORY_BATTERY.items():
    s=text(f'{slug}/index.html')
    low=s.lower()
    required=[
        'data-app-bridge',
        'data-cta-position="battery_bridge"',
        f'{battery} preguntas',
        '25 preguntas gratis',
        'estadísticas',
        'preguntas falladas',
        'pago único',
        'sin suscripción',
    ]
    for needle in required:
        if needle.lower() not in low:
            errors.append(f'{slug}: missing conversion/practical copy {needle!r}')
    # Truthful coverage: no claim that the specific battery is available in app.
    bad_patterns=[
        'batería específica disponible en la app',
        'parte específica disponible en la app',
        'practica la batería específica en la app',
    ]
    for bad in bad_patterns:
        if bad in low: errors.append(f'{slug}: overclaims specific coverage: {bad}')
    # Remove internally framed method copy.
    for internal in ['método de estudio para batería publicada','cómo preparar esta categoría con una batería publicada','consolidación</h3>','cobertura</h3>']:
        if internal in low: errors.append(f'{slug}: internal-language remains: {internal}')

# Radiodiagnóstico is the supported full-category exception.
radio=text('radiodiagnostico/index.html').lower()
for needle in ['data-app-bridge','data-cta-position="battery_bridge"','500 preguntas','200 comunes','300 específicas','25 preguntas gratis','estadísticas','preguntas falladas','pago único','sin suscripción']:
    if needle not in radio: errors.append(f'radiodiagnostico: missing {needle}')

# Fase II should first help the user find category/battery, then offer the app bridge.
phase=text('fase-2-osakidetza-2026/index.html')
phase_low=phase.lower()
soup=BeautifulSoup(phase,'html.parser')
hero=soup.select_one('.category-hero')
if hero and hero.select_one('a[data-play]'):
    errors.append('phase_2: hero still sends directly to Google Play')
for needle in ['id="categorias"','data-app-bridge','data-cta-position="battery_bridge"','200 preguntas','300 preguntas','25 preguntas gratis','estadísticas','preguntas falladas']:
    if needle.lower() not in phase_low: errors.append(f'phase_2: missing {needle}')

# Home copy should be practical rather than internal/method-oriented.
home=text('index.html').lower()
for needle in ['haz preguntas','repite las preguntas falladas','estadísticas','25 preguntas gratis','pago único','sin suscripción']:
    if needle not in home: errors.append(f'home: missing practical app copy {needle}')
for internal in ['método de estudio para batería publicada','estudia por capas, no por número de vueltas','consolidación</h3>','cobertura</h3>']:
    if internal in home: errors.append(f'home: internal-language remains: {internal}')

# Analytics: explicit bridge attribution + delayed sticky at 25% scroll.
analytics=text('assets/analytics.js')
for needle in ["data-cta-position", "MOBILE_STICKY_REVEAL_SCROLL = 0.25", "battery_bridge"]:
    if needle not in analytics: errors.append(f'analytics: missing {needle}')

# Sitemap true-modified dates for home / phase II / radiodiag.
sitemap=text('sitemap.xml')
for url in [
    'https://euskadioposiciones.com/opeosakidetza/',
    'https://euskadioposiciones.com/opeosakidetza/fase-2-osakidetza-2026/',
    'https://euskadioposiciones.com/opeosakidetza/radiodiagnostico/',
]:
    pat=re.compile(r'<url>\s*<loc>'+re.escape(url)+r'</loc>\s*<lastmod>2026-09-13</lastmod>',re.S)
    if not pat.search(sitemap): errors.append(f'sitemap: {url} not lastmod 2026-09-13')

if errors:
    print('FAIL')
    for e in errors[:200]: print(' -',e)
    print(f'{len(errors)} error(s)')
    sys.exit(1)
print('PASS: V13 conversion bridge + practical battery copy + analytics + SEO freeze')
