from pathlib import Path
import xml.etree.ElementTree as ET, sys
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'sitemap.xml'
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
modified={
'https://euskadioposiciones.com/opeosakidetza/',
'https://euskadioposiciones.com/opeosakidetza/fase-2-osakidetza-2026/',
'https://euskadioposiciones.com/opeosakidetza/radiodiagnostico/',
'https://euskadioposiciones.com/opeosakidetza/enfermeria-salud-mental/',
'https://euskadioposiciones.com/opeosakidetza/matrona/',
'https://euskadioposiciones.com/opeosakidetza/auxiliar-farmacia/',
'https://euskadioposiciones.com/opeosakidetza/psicologia-clinica/',
'https://euskadioposiciones.com/opeosakidetza/tecnico-especialista-informatica/',
'https://euskadioposiciones.com/opeosakidetza/oficial-mantenimiento-instalaciones/',
'https://euskadioposiciones.com/opeosakidetza/tecnico-superior-juridico/',
'https://euskadioposiciones.com/opeosakidetza/tecnico-medio-administracion-gestion/',
'https://euskadioposiciones.com/opeosakidetza/tecnico-superior-organizacion/',
'https://euskadioposiciones.com/opeosakidetza/trabajador-social/',
'https://euskadioposiciones.com/opeosakidetza/tecnico-superior-economico/',
}
root=ET.parse(P).getroot(); got={}
for u in root.findall('s:url',ns):
    loc=u.findtext('s:loc',namespaces=ns); lm=u.findtext('s:lastmod',namespaces=ns); got[loc]=lm
errors=[]
for url in modified:
    if got.get(url)!='2026-09-12': errors.append(f'{url}: lastmod={got.get(url)}')
if len(got)!=27: errors.append(f'expected 27 URLs, found {len(got)}')
if errors:
    print('FAIL'); [print(' -',e) for e in errors]; sys.exit(1)
print('PASS: sitemap válido; 14 URLs realmente modificadas con lastmod 2026-09-12')
