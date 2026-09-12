from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PLAY = 'https://play.google.com/store/apps/details?id=com.jocyf.opeosakidetzabateria'
CAL = '112592-osakidetza-anuncia-las-fechas-horarios'

CATS = {
    'cocinero': {
        'name': 'Cocinero/a', 'plazas': '15', 'date': '07/11/2026', 'time': '17:30',
        'venue': 'Aulario Las Nieves', 'city': 'Vitoria-Gasteiz', 'battery': '300',
        'resolution': '883/2026', 'bopv': '2602344a.shtml', 'group': 'C3',
    },
    'anatomia-patologica-citologia': {
        'name': 'Técnico/a Especialista Anatomía Patológica y Citología', 'plazas': '10', 'date': '08/11/2026', 'time': '17:30',
        'venue': 'Aulario Las Nieves', 'city': 'Vitoria-Gasteiz', 'battery': '200',
        'resolution': '882/2026', 'bopv': '2602343a.shtml', 'group': 'C1',
    },
    'enfermeria-salud-laboral': {
        'name': 'Enfermero/a Salud Laboral', 'plazas': '9', 'date': '07/11/2026', 'time': '13:30',
        'venue': 'Aulario Las Nieves', 'city': 'Vitoria-Gasteiz', 'battery': '200',
        'resolution': '880/2026', 'bopv': '2602341a.shtml', 'group': 'B1',
    },
    'medico-emergencias': {
        'name': 'F.E. Médico/a Emergencias', 'plazas': '15', 'date': '22/11/2026', 'time': '13:30',
        'venue': 'Aulario Las Nieves', 'city': 'Vitoria-Gasteiz', 'battery': '200',
        'resolution': '872/2026', 'bopv': '2602333a.shtml', 'group': 'A1',
    },
}

errors = []
for slug, d in CATS.items():
    p = ROOT / slug / 'index.html'
    if not p.exists():
        errors.append(f'{slug}: missing index.html')
        continue
    s = p.read_text(encoding='utf-8')
    canonical = f'https://euskadioposiciones.com/opeosakidetza/{slug}/'
    required = [d['name'], d['plazas'], d['date'], d['time'], d['venue'], d['city'], d['battery'],
                d['resolution'], d['bopv'], d['group'], canonical, CAL, PLAY,
                'Las respuestas incorrectas no conllevan penalización', 'Parte específica']
    for token in required:
        if token not in s:
            errors.append(f'{slug}: missing {token!r}')
    if 'batería específica' in s.lower() and 'no' not in s.lower():
        errors.append(f'{slug}: may overclaim specific battery availability')
    if '"dateModified":"2026-09-12"' not in s:
        errors.append(f'{slug}: dateModified not frozen to 2026-09-12')

phase = (ROOT / 'fase-2-osakidetza-2026' / 'index.html').read_text(encoding='utf-8')
for slug, d in CATS.items():
    href = f'../{slug}/'
    if href not in phase:
        errors.append(f'phase2: missing link {href}')
    if f'>{d["name"]}</a>' not in phase:
        errors.append(f'phase2: category name not linked for {d["name"]}')

analytics = (ROOT / 'assets' / 'analytics.js').read_text(encoding='utf-8')
for slug in CATS:
    if f"'{slug}':" not in analytics:
        errors.append(f'analytics: missing category slug {slug}')

sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
for slug in CATS:
    url = f'https://euskadioposiciones.com/opeosakidetza/{slug}/'
    if url not in sitemap:
        errors.append(f'sitemap: missing {url}')

if errors:
    print('FAIL')
    for e in errors:
        print(' -', e)
    sys.exit(1)
print('PASS: 4 nuevas fichas Fase II enlazadas, medibles y en sitemap')
