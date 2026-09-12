from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')

def require(text, needle, label):
    assert needle in text, f'FALTA {label}: {needle}'

def forbid(text, needle, label):
    assert needle not in text, f'SOBRA {label}: {needle}'

home = read('index.html')
phase2 = read('fase-2-osakidetza-2026/index.html')
radiodiag = read('radiodiagnostico/index.html')
analytics = read('assets/analytics.js')

# SEO estructural protegido.
require(home, '<title>Test Osakidetza 2026 | Baterías oficiales, fechas y categorías</title>', 'title home')
require(home, '<h1>OPE Osakidetza 2026: baterías, fechas y test por categoría</h1>', 'H1 home')
require(home, '<link href="https://euskadioposiciones.com/opeosakidetza/" rel="canonical"/>', 'canonical home')
require(phase2, '<title>Fase II OPE Osakidetza 2026 | 41 categorías y fechas de examen</title>', 'title fase II')
require(phase2, '<h1>Fase II OPE Osakidetza 2026</h1>', 'H1 fase II')
require(phase2, '<link href="https://euskadioposiciones.com/opeosakidetza/fase-2-osakidetza-2026/" rel="canonical"/>', 'canonical fase II')
require(radiodiag, '<title>Test Radiodiagnóstico Osakidetza 2026 | 500 preguntas</title>', 'title radiodiagnóstico')
require(radiodiag, '<h1>Test Radiodiagnóstico Osakidetza 2026: batería de 500 preguntas</h1>', 'H1 radiodiagnóstico')
require(radiodiag, '<link href="https://euskadioposiciones.com/opeosakidetza/radiodiagnostico/" rel="canonical"/>', 'canonical radiodiagnóstico')

# Frescura oficial de Fase II / Bloque 2.
for text, label in [(home, 'home'), (phase2, 'fase II')]:
    require(text, '6, 7, 8, 21, 22 y 27 de noviembre', f'calendario definitivo {label}')
    require(text, '9 al 29 de septiembre de 2026', f'plazo méritos {label}')

require(phase2, '<th>Fecha</th><th>Hora</th><th>Sede</th>', 'columnas calendario en directorio')
assert phase2.count('data-exam-date="') == 41, f'Se esperaban 41 filas con fecha; hay {phase2.count("data-exam-date=\"")}.'
require(phase2, 'data-phase2-category="Técnico/a Especialista Radiodiagnóstico"', 'fila radiodiagnóstico')
require(phase2, 'data-exam-date="27/11/2026"', 'fecha de radiodiagnóstico en directorio')
require(phase2, 'data-exam-time="18:00"', 'hora de radiodiagnóstico en directorio')
forbid(phase2, 'fecha, hora y lugar concretos se publicarán en septiembre', 'texto desactualizado fase II')
forbid(phase2, 'Pendiente: día, hora y sede', 'estado pendiente ya resuelto')
forbid(phase2, 'Octubre y noviembre de 2026', 'calendario antiguo fase II')

# Radiodiagnóstico: cita exacta publicada.
require(radiodiag, '27 de noviembre de 2026', 'fecha radiodiagnóstico')
require(radiodiag, '18:00', 'hora radiodiagnóstico')
require(radiodiag, 'BEC', 'sede radiodiagnóstico')
forbid(radiodiag, 'día, hora y sede concretos pendientes de publicación', 'texto desactualizado radiodiagnóstico')
forbid(radiodiag, 'fecha exacta de examen debe consultarse cuando Osakidetza la publique', 'texto desactualizado radiodiagnóstico 2')

# Analítica: atribución por host real + impresiones de CTA + contexto de página.
forbid(analytics, "referrer.set('utm_source', 'github_pages')", 'UTM fija antigua')
require(analytics, 'window.location.hostname', 'host real para atribución')
require(analytics, 'play_cta_viewed', 'impresiones de CTA')
require(analytics, 'page_slug', 'slug de página en referrer')
require(analytics, 'tecnico-medio-administracion-gestion', 'taxonomía Fase II')
require(analytics, 'IntersectionObserver', 'observación de impresiones CTA')

print('PASS: frescura Fase II, Radiodiagnóstico, SEO protegido y atribución analítica verificadas')
