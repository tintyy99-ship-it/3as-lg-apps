#!/usr/bin/env bash
# Genere le keystore d'upload Play Store (A FAIRE SUR TON PC, pas dans le repo).
# Un seul keystore partage pour les 2 apps (pratique standard).
# Usage: bash scripts/make_upload_keystore.sh
# NE COMMITTE JAMAIS le .keystore ni les mots de passe. Sauvegarde-les hors Git
# (cle USB + copie papier). Si tu perds cette cle, tu ne pourras plus mettre a jour tes apps.
set -euo pipefail
OUT="3as-upload.keystore"
ALIAS="3as-upload"
[ -f "$OUT" ] && { echo "REFUS: $OUT existe deja (ne jamais ecraser une cle d'upload)"; exit 1; }
STOREPW="$(openssl rand -base64 24 | tr -d '/+=' | cut -c1-20)"
KEYPW="$(openssl rand -base64 24 | tr -d '/+=' | cut -c1-20)"
keytool -genkeypair -keystore "$OUT" -alias "$ALIAS" -keyalg RSA -keysize 2048 \
  -validity 10950 -storepass "$STOREPW" -keypass "$KEYPW" \
  -dname "CN=3AS LG, OU=Mobile, O=3AS LG, C=DZ"
B64="$(base64 -w0 "$OUT" 2>/dev/null || base64 "$OUT" | tr -d '\n')"
echo "===== keystore genere ====="
echo "Fichier (A SAUVEGARDER hors Git): $OUT"
echo "KEYSTORE_PASSWORD=$STOREPW"
echo "KEY_ALIAS=$ALIAS"
echo "KEY_PASSWORD=$KEYPW"
echo ""
echo "KEYSTORE_BASE64 (1 seule ligne, a coller en secret GitHub):"
echo "$B64"
echo ""
echo "--- commandes (colle-les une par une) ---"
echo "gh secret set KEYSTORE_PASSWORD --body '$STOREPW' --repo tintyy99-ship-it/3as-lg-apps"
echo "gh secret set KEY_ALIAS --body '$ALIAS' --repo tintyy99-ship-it/3as-lg-apps"
echo "gh secret set KEY_PASSWORD --body '$KEYPW' --repo tintyy99-ship-it/3as-lg-apps"
echo "gh secret set KEYSTORE_BASE64 --body '$B64' --repo tintyy99-ship-it/3as-lg-apps"
echo ""
echo "Ensuite : push sur main -> le workflow signe les 2 AAB en release, prets pour la Play Console."
