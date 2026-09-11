# 3AS LG — Apps Admin + Élève (Supabase gratuit)

## ⚠️ PyInstaller vs APK
**PyInstaller = PC (.exe) uniquement, PAS pour APK.**
Pour APK Android : **Buildozer + python-for-android (p4a)** avec les `main.py` Kivy fournis.

## Structure
```
supabase/schema.sql       → à exécuter dans Supabase SQL Editor
supabase/seed_courses.sql → cours 3AS LG
admin-app/web/index.html  → App Admin (PWA, utilisable direct sur tel)
eleve-app/web/index.html  → App Élève (PWA)
admin-app/main.py         → version native APK (Kivy)
eleve-app/main.py         → version native APK (Kivy)
```

## 1. Supabase (gratuit)
1. Crée projet sur supabase.com
2. SQL Editor → colle `supabase/schema.sql` → Run
3. Puis `supabase/seed_courses.sql` → Run
4. Database > Replication → active `students, messages, courses`
5. Project Settings > API → copie URL + anon key

## 2. Tester sans build (immédiat sur téléphone)
```bash
cd eleve-app/web && python3 -m http.server 8001
# ouvre http://localhost:8001 dans Chrome → Installer comme app
cd ../../admin-app/web && python3 -m http.server 8002
```
Dans chaque app : ⚙️ → colle URL + anon key (stocké local, jamais commité).

Flux :
1. Admin crée élève → code `3AS-XXXXXX` auto
2. Élève reçoit code (admin ou Telegram https://t.me/Roqaya_2328)
3. Élève entre code → accès cours + messagerie
4. Admin prolonge (+30/+90j), régénère, active/désactive
5. Messages temps réel (Realtime)

## 3. Build APK (PC Linux / Termux proot)
```bash
cd eleve-app && buildozer android debug
# APK dans bin/
cd ../admin-app && buildozer android debug
```
Sur Termux natif : buildozer nécessite `pkg install python` + SDK ; plus fiable via proot Ubuntu ou PC.
Ne PAS utiliser `pyinstaller --onefile` pour APK.

## 4. GitHub
```bash
git init && git add . && git commit -m "3AS LG apps"
gh repo create 3as-lg-apps --private --source=. --push
# ou avec token: git remote add origin https://Tinty99:TOKEN@github.com/Tinty99/3as-lg-apps.git
```

## Sécurité
- Ne committe JAMAIS `.env` ni tokens. Utilise `.env.example`.
- RLS actuelles = permissives pour MVP (auth custom par code). Durcir ensuite via Edge Function.
- **Si tu as partagé tes tokens en clair, révoque-les** (GitHub Settings > Tokens, Supabase > Access Tokens) et régénère.
