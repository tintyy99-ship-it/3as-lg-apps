#!/usr/bin/env bash
# Copie les apps web dans les assets Android + génère supabase-config.js.
# La clé ANON vient de la variable d'env SUPABASE_ANON_KEY (secret CI).
# Sans clé : build offline (cours FALLBACK intégrés).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
URL="https://xvbswwlphdjtviufwcsx.supabase.co"
for APP in eleve admin; do
  SRC="$ROOT/${APP}-app/web"
  DST="$ROOT/android/$APP/src/main/assets/www"
  mkdir -p "$DST"
  cp "$SRC/index.html" "$DST/index.html"
  if [ -n "${SUPABASE_ANON_KEY:-}" ]; then
    printf 'window.SB_CONFIG = {\n  SUPABASE_URL: "%s",\n  SUPABASE_ANON_KEY: "%s"\n};\n' \
      "$URL" "$SUPABASE_ANON_KEY" > "$DST/supabase-config.js"
    echo "$APP: config en ligne branchée"
  else
    printf 'window.SB_CONFIG = { SUPABASE_URL: "%s", SUPABASE_ANON_KEY: "" };\n' \
      "$URL" > "$DST/supabase-config.js"
    echo "$APP: build offline (cours intégrés, colle la clé via l'app si besoin)"
  fi
done
