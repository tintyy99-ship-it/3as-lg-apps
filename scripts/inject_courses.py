# -*- coding: utf-8 -*-
"""Injecte le programme complet dans Supabase + génère seed SQL + MAJ FALLBACK élève."""
import json, os, urllib.request, urllib.error
from courses_data import COURSES
import pathlib
ROOT = pathlib.Path('/root/3as-lg-apps')
SB_TOKEN = os.environ.get('SB_TOKEN', '')  # export SB_TOKEN='sbp_...' (jamais commité)
REF = os.environ.get('SB_REF', 'xvbswwlphdjtviufwcsx')
if not SB_TOKEN:
    raise SystemExit("Manquant: export SB_TOKEN='sbp_...'")

def q(sql, label='Q'):
    data = json.dumps({'query': sql}).encode()
    req = urllib.request.Request(
        f'https://api.supabase.com/v1/projects/{REF}/database/query',
        data=data, method='POST')
    req.add_header('Authorization', f'Bearer {SB_TOKEN}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            body = r.read().decode()
            print(label, r.status, body[:800])
            return body
    except urllib.error.HTTPError as e:
        print(label, 'HTTPERR', e.code, e.read().decode()[:2500])
        raise
    except Exception as e:
        print(label, 'ERR', e)
        raise

def esc(s):
    return (s or '').replace("'", "''")

# 1. SQL seed file
lines = ["-- Seed complet 3AS LG Algérie — %d cours" % len(COURSES),
         "delete from public.courses;",
         "insert into public.courses (matiere, niveau, chapitre, contenu_cours, explications_simplifiees, ressources_associees, ordre) values"]
vals = []
for m, ch, co, ex, o in COURSES:
    vals.append("('%s','3AS LG','%s','%s','%s','[]',%d)" % (esc(m), esc(ch), esc(co), esc(ex), o))
lines.append(",\n".join(vals) + ";")
(ROOT/'supabase'/'seed_full_3aslg.sql').write_text("\n".join(lines), encoding='utf-8')
print('seed file written:', len(COURSES))

# 2. Push via API en lots de 10
q("delete from public.courses;", 'DELETE')
batch = 10
for i in range(0, len(COURSES), batch):
    chunk = COURSES[i:i+batch]
    v = ",\n".join("('%s','3AS LG','%s','%s','%s','[]',%d)" % (esc(m), esc(ch), esc(co), esc(ex), o) for m, ch, co, ex, o in chunk)
    sql = "insert into public.courses (matiere, niveau, chapitre, contenu_cours, explications_simplifiees, ressources_associees, ordre) values " + v + ";"
    q(sql, f'INSERT {i+1}-{i+len(chunk)}')
q("select count(*) as n from public.courses", 'COUNT')
q("select matiere, count(*) as n from public.courses group by 1 order by 1", 'BY_MATIERE')

# 3. MAJ FALLBACK dans eleve app (offline complet)
fb = [{"matiere": m, "niveau": "3AS LG", "chapitre": ch,
       "contenu_cours": co, "explications_simplifiees": ex} for m, ch, co, ex, o in COURSES]
p = ROOT/'eleve-app'/'web'/'index.html'
html = p.read_text(encoding='utf-8')
start = html.find('const FALLBACK=')
end = html.find('];', start) + 2
new = 'const FALLBACK=' + json.dumps(fb, ensure_ascii=False)
html = html[:start] + new + html[end:]
p.write_text(html, encoding='utf-8')
print('FALLBACK updated:', len(fb))
