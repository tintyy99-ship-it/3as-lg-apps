# 3AS LG v1.11 — Apps signées (clé upload) + infos signature

## Les apps (install direct / Play Store)
| Fichier | Usage | Taille |
|---|---|---|
| `3AS-LG-Eleve-v1.11.apk` | Install directe téléphone (Élève) | ~262 Ko |
| `3AS-LG-Admin-v1.11.apk` | Install directe téléphone (Admin) | ~195 Ko |
| `3AS-LG-Eleve-v1.11.aab` | Envoi Play Console (Élève) | ~262 Ko |
| `3AS-LG-Admin-v1.11.aab` | Envoi Play Console (Admin) | ~195 Ko |
| `CHECKSUMS.sha256` | Vérifier l'intégrité après téléchargement | — |

Vérification : `sha256sum -c CHECKSUMS.sha256`

Nouveau v1.11 : menu hamburger ☰ dans l'Admin — catégories
Accueil / Élèves / Cours & Matières / Messagerie, chaque catégorie
s'affiche toute seule (petites cartes comme avant). Élèves : créer,
+30/+90j, suspendre, réactiver, 💬, 🗑️ supprimer. Cours : ajouter,
liste, 🗑️ par cours / section / matière. versionCode 11.

## Signature (infos publiques)
- Keystore : `3as-upload.keystore`, alias `3as-upload`, RSA 2048, PKCS12
- Valide jusqu'en 2056 (10 950 jours depuis 2026-09-12)
- Empreinte SHA-256 : `E1:C9:FE:10:FB:45:27:67:05:0B:C3:1E:4D:AC:3D:49:66:02:0A:88:46:09:67:93:69:52:C4:3F:38:C6:15:7B`
- La Play Console affichera cette empreinte comme "clé d'upload" : compare-la avant d'envoyer.

## Où est la clé privée ? (NE JAMAIS la mettre ici)
- GitHub > repo > Settings > Secrets and variables > Actions :
  `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`
- + ta sauvegarde hors ligne `3as-upload.keystore` (USB).
- Chaque push sur `main` rebuild des APK/AAB signés automatiquement.
