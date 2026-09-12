from pathlib import Path
import re, json, sys

ROOT = Path(__file__).resolve().parents[1]
SCHEDULE = {
    'enfermeria-salud-mental': ('21/11/2026','13:30','Aulario Las Nieves','Vitoria-Gasteiz'),
    'matrona': ('21/11/2026','13:30','Aulario Las Nieves','Vitoria-Gasteiz'),
    'auxiliar-farmacia': ('06/11/2026','17:30','Aulario Las Nieves','Vitoria-Gasteiz'),
    'psicologia-clinica': ('07/11/2026','09:30','Aulario Las Nieves','Vitoria-Gasteiz'),
    'tecnico-especialista-informatica': ('07/11/2026','13:30','Aulario Las Nieves','Vitoria-Gasteiz'),
    'oficial-mantenimiento-instalaciones': ('08/11/2026','09:30','Aulario Las Nieves','Vitoria-Gasteiz'),
    'tecnico-superior-juridico': ('22/11/2026','09:30','Aulario Las Nieves','Vitoria-Gasteiz'),
    'tecnico-medio-administracion-gestion': ('27/11/2026','09:00','BEC','Barakaldo'),
    'tecnico-superior-organizacion': ('27/11/2026','12:00','BEC','Barakaldo'),
    'trabajador-social': ('27/11/2026','15:00','BEC','Barakaldo'),
    'tecnico-superior-economico': ('27/11/2026','15:00','BEC','Barakaldo'),
    'cocinero': ('07/11/2026','17:30','Aulario Las Nieves','Vitoria-Gasteiz'),
    'anatomia-patologica-citologia': ('08/11/2026','17:30','Aulario Las Nieves','Vitoria-Gasteiz'),
    'enfermeria-salud-laboral': ('07/11/2026','13:30','Aulario Las Nieves','Vitoria-Gasteiz'),
    'medico-emergencias': ('22/11/2026','13:30','Aulario Las Nieves','Vitoria-Gasteiz'),
}
EXPECTED = {
    'enfermeria-salud-mental': ('Enfermería Salud Mental Osakidetza 2026 | 95 plazas','Enfermero/a Salud Mental Osakidetza 2026: 95 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/enfermeria-salud-mental/'),
    'matrona': ('Matrón/a Osakidetza 2026 | 85 plazas y batería','Matrón/a Osakidetza 2026: 85 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/matrona/'),
    'auxiliar-farmacia': ('Auxiliar de Farmacia Osakidetza 2026 | 40 plazas','Auxiliar de Farmacia Osakidetza 2026: 40 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/auxiliar-farmacia/'),
    'psicologia-clinica': ('Psicología Clínica Osakidetza 2026 | 35 plazas','Psicología Clínica Osakidetza 2026: 35 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/psicologia-clinica/'),
    'tecnico-especialista-informatica': ('Técnico/a Especialista Informática Osakidetza 2026 | 35 plazas','Técnico/a Especialista Informática Osakidetza 2026: 35 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/tecnico-especialista-informatica/'),
    'oficial-mantenimiento-instalaciones': ('Oficial/a Mantenimiento Instalaciones Osakidetza 2026 | 28 plazas','Oficial/a Mantenimiento Instalaciones Osakidetza 2026: 28 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/oficial-mantenimiento-instalaciones/'),
    'tecnico-superior-juridico': ('Técnico/a Superior Jurídico/a Osakidetza 2026 | 29 plazas','Técnico/a Superior Jurídico/a Osakidetza 2026: 29 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/tecnico-superior-juridico/'),
    'tecnico-medio-administracion-gestion': ('Técnico Medio Administración Osakidetza 2026 | 8 plazas','Técnico/a Medio Administración y Gestión Osakidetza 2026','https://euskadioposiciones.com/opeosakidetza/tecnico-medio-administracion-gestion/'),
    'tecnico-superior-organizacion': ('Técnico/a Superior Organización Osakidetza 2026 | 25 plazas','Técnico/a Superior Organización Osakidetza 2026: 25 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/tecnico-superior-organizacion/'),
    'trabajador-social': ('Trabajo Social Osakidetza 2026 | 33 plazas y batería','Trabajador/a Social Osakidetza 2026: 33 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/trabajador-social/'),
    'tecnico-superior-economico': ('Técnico/a Superior Económico/a Osakidetza 2026 | 31 plazas','Técnico/a Superior Económico/a Osakidetza 2026: 31 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/tecnico-superior-economico/'),
    'cocinero': ('Cocinero/a Osakidetza 2026 | 15 plazas','Cocinero/a Osakidetza 2026: 15 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/cocinero/'),
    'anatomia-patologica-citologia': ('Anatomía Patológica Osakidetza 2026 | 10 plazas','Técnico/a Anatomía Patológica y Citología Osakidetza 2026: 10 plazas','https://euskadioposiciones.com/opeosakidetza/anatomia-patologica-citologia/'),
    'enfermeria-salud-laboral': ('Enfermería Salud Laboral Osakidetza 2026 | 9 plazas','Enfermero/a Salud Laboral Osakidetza 2026: 9 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/enfermeria-salud-laboral/'),
    'medico-emergencias': ('Médico/a Emergencias Osakidetza 2026 | 15 plazas','Médico/a Emergencias Osakidetza 2026: 15 plazas y Fase II','https://euskadioposiciones.com/opeosakidetza/medico-emergencias/'),
}

errors=[]
for slug,(date,time,venue,city) in SCHEDULE.items():
    p=ROOT/slug/'index.html'
    if not p.exists():
        errors.append(f'{slug}: missing index.html')
        continue
    s=p.read_text(encoding='utf-8')
    title,h1,canonical=EXPECTED[slug]
    if f'<title>{title}</title>' not in s: errors.append(f'{slug}: title changed')
    if f'<h1>{h1}</h1>' not in s: errors.append(f'{slug}: H1 changed')
    if f'href="{canonical}" rel="canonical"' not in s: errors.append(f'{slug}: canonical changed')
    if '"dateModified":"2026-09-12"' not in s: errors.append(f'{slug}: dateModified not 2026-09-12')
    if date not in s: errors.append(f'{slug}: missing date {date}')
    if time not in s: errors.append(f'{slug}: missing time {time}')
    if venue not in s or city not in s: errors.append(f'{slug}: missing venue/city')
    if 'octubre y noviembre de 2026' in s or 'octubre o noviembre de 2026' in s:
        errors.append(f'{slug}: stale vague exam window remains')
    if 'día, hora y sede' in s.lower() and 'cuando se publi' in s.lower():
        errors.append(f'{slug}: stale pending-calendar language remains')
    if '112592-osakidetza-anuncia-las-fechas-horarios' not in s:
        errors.append(f'{slug}: missing 10/09 official calendar source')

if errors:
    print('FAIL')
    for e in errors: print(' -',e)
    sys.exit(1)
print(f'PASS: {len(SCHEDULE)} fichas Fase II con calendario exacto y SEO principal congelado')
