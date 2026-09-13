from pathlib import Path
import xml.etree.ElementTree as ET, sys
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'sitemap.xml'
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
categories={
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
'https://euskadioposiciones.com/opeosakidetza/cocinero/',
'https://euskadioposiciones.com/opeosakidetza/anatomia-patologica-citologia/',
'https://euskadioposiciones.com/opeosakidetza/enfermeria-salud-laboral/',
'https://euskadioposiciones.com/opeosakidetza/medico-emergencias/',
}
root=ET.parse(P).getroot(); got={}
for u in root.findall('s:url',ns):
    loc=u.findtext('s:loc',namespaces=ns); lm=u.findtext('s:lastmod',namespaces=ns); got[loc]=lm
errors=[]
for url in categories:
    if got.get(url)!='2026-09-13': errors.append(f'{url}: lastmod={got.get(url)}')
if len(got)!=31: errors.append(f'expected 31 URLs, found {len(got)}')
if errors:
    print('FAIL'); [print(' -',e) for e in errors]; sys.exit(1)
print('PASS: sitemap válido; 15 fichas actualizadas con lastmod 2026-09-13; 31 URLs totales')
