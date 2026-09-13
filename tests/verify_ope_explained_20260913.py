from pathlib import Path
import re, sys

ROOT=Path(__file__).resolve().parents[1]
CATS={
'enfermeria-salud-mental': {'exam':'single','exp':'0,25','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
'matrona': {'exam':'single','exp':'0,25','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
'auxiliar-farmacia': {'exam':'single','exp':'0,25','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
'psicologia-clinica': {'exam':'65_35','exp':'0,30','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
'tecnico-especialista-informatica': {'exam':'single','exp':'0,25','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
'oficial-mantenimiento-instalaciones': {'exam':'single','exp':'0,25','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
'tecnico-superior-juridico': {'exam':'65_35','exp':'0,25','eus':['PL3: <strong>27</strong>','PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'207'},
'tecnico-medio-administracion-gestion': {'exam':'single','exp':'0,25','eus':['PL3: <strong>27</strong>','PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'207'},
'tecnico-superior-organizacion': {'exam':'65_35','exp':'0,25','eus':['PL3: <strong>27</strong>','PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'207'},
'trabajador-social': {'exam':'single','exp':'0,25','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
'tecnico-superior-economico': {'exam':'65_35','exp':'0,25','eus':['PL3: <strong>27</strong>','PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'207'},
'cocinero': {'exam':'single','exp':'0,25','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
'anatomia-patologica-citologia': {'exam':'single','exp':'0,25','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
'enfermeria-salud-laboral': {'exam':'single','exp':'0,25','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
'medico-emergencias': {'exam':'single','exp':'0,30','eus':['PL2: <strong>18</strong>','PL1: <strong>9</strong>'],'total':'198'},
}
errors=[]
for slug,cfg in CATS.items():
    p=ROOT/slug/'index.html'
    s=p.read_text(encoding='utf-8') if p.exists() else ''
    checks=[
      ('section', 'id="como-funciona-ope"'),
      ('summary', 'Tu OPE en 30 segundos'),
      ('exam', 'Cómo es el examen'),
      ('score', 'Cómo se calcula la puntuación final'),
      ('experience', 'Cómo puntúa la experiencia'),
      ('training', 'Qué formación y otros méritos dan puntos'),
      ('euskera', 'Cuánto puntúa el euskera'),
      ('after', 'Qué ocurre después del examen'),
      ('save', 'conservar la nota'),
      ('general bases', '2600514a.shtml'),
      ('pass mark', '50/100'),
      ('no penalty', 'no penalizan'),
      ('experience max', 'Hasta <strong>60 puntos</strong>'),
      ('training max', 'Hasta <strong>20 puntos</strong>'),
      ('experience rate', f'<strong>{cfg["exp"]} puntos por mes</strong>'),
      ('total max', f'<strong>{cfg["total"]} puntos</strong>'),
      ('fresh date', '"dateModified":"2026-09-13"'),
    ]
    for label,needle in checks:
        if needle.lower() not in s.lower(): errors.append(f'{slug}: missing {label}: {needle}')
    for needle in cfg['eus']:
        if needle not in s: errors.append(f'{slug}: missing euskera {needle}')
    if cfg['exam']=='65_35':
        if '65 %' not in s or '35 %' not in s: errors.append(f'{slug}: missing 65/35 weighting')
    if 'la puntuación final es 60 % oposición' in s.lower() or 'se pondera 60 % oposición' in s.lower():
        errors.append(f'{slug}: misleading 60/40 final-score wording')

if errors:
    print('FAIL')
    for e in errors[:120]: print(' -', e)
    print(f'{len(errors)} error(s)')
    sys.exit(1)
print(f'PASS: {len(CATS)} fichas explican examen + concurso-oposición + puntos + méritos con SEO semántico')
