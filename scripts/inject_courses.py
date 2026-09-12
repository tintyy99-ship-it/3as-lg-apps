# -*- coding: utf-8 -*-
"""يحقن الدروس الكاملة + الأعمدة الجديدة في Supabase + FALLBACK + seed SQL."""
import json, os, urllib.request, urllib.error, pathlib
from courses_data import COURSES

ROOT = pathlib.Path('/root/3as-lg-apps')
SB_TOKEN = os.environ.get('SB_TOKEN', '')
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
        with urllib.request.urlopen(req, timeout=120) as r:
            body = r.read().decode()
            print(label, r.status, body[:400])
            return body
    except urllib.error.HTTPError as e:
        print(label, 'HTTPERR', e.code, e.read().decode()[:2500])
        raise

def esc(s):
    return (s or '').replace("'", "''")

rows = [f"('{esc(m)}','3AS LG','{esc(ch)}','{esc(co)}','{esc(ex)}','[]',{o},{t},'{esc(sec)}')"
        for m, ch, t, sec, co, ex, o in COURSES]

# seed SQL
(ROOT / 'supabase' / 'seed_full_3aslg.sql').write_text(
    "-- Seed complet 3AS LG (78 درسا كاملا بالعربية)\ndelete from public.courses;\n"
    "insert into public.courses (matiere, niveau, chapitre, contenu_cours, explications_simplifiees, ressources_associees, ordre, trimestre, section) values\n"
    + ",\n".join(rows) + ";", encoding='utf-8')
print('seed file:', len(rows))

q("delete from public.courses;", 'DELETE')
for i in range(0, len(rows), 8):
    chunk = rows[i:i + 8]
    q("insert into public.courses (matiere, niveau, chapitre, contenu_cours, explications_simplifiees, ressources_associees, ordre, trimestre, section) values " + ",\n".join(chunk) + ";",
      f'INSERT {i + 1}-{i + len(chunk)}')
q("select count(*) as n from public.courses", 'COUNT')
q("select trimestre, count(*) as n from public.courses group by 1 order by 1", 'BY_TRIM')

# FALLBACK JSON pour l'app (offline complet)
fb = [{"matiere": m, "niveau": "3AS LG", "chapitre": ch, "trimestre": t,
       "section": sec, "contenu_cours": co, "explications_simplifiees": ex}
      for m, ch, t, sec, co, ex, o in COURSES]
(ROOT / 'shared' / 'courses_full.json').write_text(
    json.dumps(fb, ensure_ascii=False), encoding='utf-8')
print('shared/courses_full.json:', len(fb))
