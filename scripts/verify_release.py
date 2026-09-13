#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérifie un APK 3AS LG AVANT publication : icônes, manifest, JS, contenu, secrets.
Usage: python3 scripts/verify_release.py Eleve.apk Admin.apk
Sortie != 0 si un contrôle échoue.
"""
import re
import struct
import subprocess
import sys
import tempfile
import zipfile

FAIL = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" ({detail})" if detail else ""))
    if not cond:
        FAIL.append(name)


def inline_scripts(html):
    return re.findall(r"<script>(.*?)</script>", html, re.S)


def main():
    if len(sys.argv) != 3:
        print("Usage: verify_release.py Eleve.apk Admin.apk")
        sys.exit(2)
    eleve_apk, admin_apk = sys.argv[1], sys.argv[2]

    for apk, tag in [(eleve_apk, "eleve"), (admin_apk, "admin")]:
        z = zipfile.ZipFile(apk)
        names = z.namelist()

        # --- icônes : PNG legacy + foreground + XML adaptatifs ---
        legacy = [n for n in names if re.match(r"res/mipmap-(mdpi|hdpi|xhdpi|xxhdpi|xxxhdpi)-v4/ic_launcher\.png$", n)]
        fg = [n for n in names if "ic_launcher_foreground.png" in n]
        anydpi = [n for n in names if "mipmap-anydpi-v26/ic_launcher" in n]
        check(f"{tag}: 5 icônes legacy", len(legacy) == 5, str(len(legacy)))
        check(f"{tag}: 5 foregrounds", len(fg) == 5, str(len(fg)))
        check(f"{tag}: XML adaptatifs", len(anydpi) == 2, str(len(anydpi)))
        for n in legacy + fg:
            d = z.read(n)
            ok = d[:8] == b"\x89PNG\r\n\x1a\n" and len(d) > 100
            w, hh = struct.unpack(">II", d[16:24])
            check(f"{tag}: PNG valide {n.split('/')[1]}", ok, f"{w}x{hh}")

        # --- manifest binaire : attr icon + roundIcon présents ---
        man = z.read("AndroidManifest.xml")
        pool = man.decode("utf-16-le", errors="ignore")
        check(f"{tag}: manifest icon=", "icon" in pool)
        check(f"{tag}: manifest roundIcon=", "roundIcon" in pool)

        html = z.read("assets/www/index.html").decode("utf-8")
        check(f"{tag}: 1 seul DOCTYPE", html.count("<!DOCTYPE") == 1)
        scripts = inline_scripts(html)
        check(f"{tag}: scripts inline", len(scripts) >= 1, str(len(scripts)))
        for k, s in enumerate(scripts):
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
                f.write(s)
                fp = f.name
            r = subprocess.run(["node", "--check", fp], capture_output=True, text=True)
            check(f"{tag}: JS valide #{k}", r.returncode == 0, r.stderr.strip()[:120])

        # --- pas de mot de passe admin en clair ---
        check(f"{tag}: aucun secret en clair", "Roqaya-Admin-3AS-2026" not in html)

        if tag == "eleve":
            i = html.find("const FALLBACK=") + len("const FALLBACK=")
            j = html.find("</script>", i)
            import json as J
            fb = J.loads(html[i:j].replace("\nwindow.__booted=true;", "").rstrip().rstrip(";"))
            check("eleve: 100+ cours embarqués", len(fb) >= 100, str(len(fb)))
            for feat in ["viewList", "playDoors", "setLang", "toggleDrawer", "MAT_COEF",
                         "slideBlur", "slideBlur".lower(), "__booted", "lg-out", "1.12"]:
                check(f"eleve: feature {feat}", feat.lower() in html.lower(), "")
        else:
            for feat in ["suspendre", "supprimerEleve", "deleteCourse", "deleteSectionUI", "deleteMatiereUI", "toggleMenu", "showView", "deleteChat", "askDeleteAll", "__booted",
                         "toast", "1.12", "5db4f9e3587a9752"]:
                check(f"admin: feature {feat}", feat in html, "")

    print()
    if FAIL:
        print(f"ECHEC ({len(FAIL)}):", FAIL)
        sys.exit(1)
    print("TOUT EST VERT ✔ — Release autorisée.")


if __name__ == "__main__":
    main()
