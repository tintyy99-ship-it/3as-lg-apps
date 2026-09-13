# 3AS LG v1.15 — Apps signées (clé upload) + infos signature

## Les apps (install direct / Play Store)
| Fichier | Usage | Taille |
|---|---|---|
| `3AS-LG-Eleve-v1.15.apk` | Install directe téléphone (Élève) | ~265 Ko |
| `3AS-LG-Admin-v1.15.apk` | Install directe téléphone (Admin) | ~197 Ko |
| `3AS-LG-Eleve-v1.15.aab` | Envoi Play Console (Élève) | ~265 Ko |
| `3AS-LG-Admin-v1.15.aab` | Envoi Play Console (Admin) | ~197 Ko |
| `CHECKSUMS.sha256` | Vérifier l'intégrité après téléchargement | — |

Vérification : `cd dist/v1.15 && sha256sum -c CHECKSUMS.sha256`

Nouveau v1.15 : burger caché sur l'écran code côté élève (plus de
menu avant login), suspension DIRECTE côté admin (1 clic, sans
modale, mise à jour optimiste) + déconnexion instantanée côté élève
(Realtime `students` + re-validation session + polling 10s + contrôle
au retour premier plan). E2E aligné. versionCode 15.

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
