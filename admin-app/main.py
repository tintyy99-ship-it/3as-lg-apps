"""
3AS LG - App Admin (Kivy + Supabase REST)
Fonctions: créer élève + code auto, prolonger, modifier, messagerie, dashboard.
"""
import os, json, secrets, string, datetime, urllib.request, urllib.parse

CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

def env(k, d=""):
    v = os.environ.get(k, d)
    if not v and os.path.exists(".env"):
        for line in open(".env"):
            if "=" in line and not line.strip().startswith("#"):
                kk, vv = line.strip().split("=", 1)
                if kk.strip() == k:
                    return vv.strip()
    return v

SB_URL = env("SUPABASE_URL")
SB_KEY = env("SUPABASE_ANON_KEY")

def api(path, method="GET", body=None, params=None):
    if not SB_URL or not SB_KEY:
        raise RuntimeError("Configure SUPABASE_URL / SUPABASE_ANON_KEY")
    url = SB_URL.rstrip("/") + "/rest/v1/" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("apikey", SB_KEY)
    req.add_header("Authorization", "Bearer " + SB_KEY)
    req.add_header("Content-Type", "application/json")
    if method in ("POST", "PATCH"):
        req.add_header("Prefer", "return=representation")
    with urllib.request.urlopen(req, timeout=20) as r:
        txt = r.read().decode()
        return json.loads(txt) if txt else []

def gen_code():
    return "3AS-" + "".join(secrets.choice(CHARS) for _ in range(6))

def create_student(nom, prenom, email="", jours=90):
    code = gen_code()
    exp = (datetime.datetime.utcnow() + datetime.timedelta(days=jours)).isoformat()
    rows = api("students", method="POST",
               body={"nom": nom, "prenom": prenom, "email": email,
                     "code_reference": code, "date_expiration_code": exp,
                     "statut_actif": True})
    return rows[0] if rows else {"code_reference": code}

def prolonger(student_id, jours=30):
    """Prolonge la validité du code de ref de `jours` jours."""
    cur = api("students", params={"id": f"eq.{student_id}", "select": "date_expiration_code"})[0]
    base_str = cur.get("date_expiration_code") or datetime.datetime.now(datetime.timezone.utc).isoformat()
    base = datetime.datetime.fromisoformat(base_str.replace("Z", "+00:00"))
    now = datetime.datetime.now(datetime.timezone.utc)
    if base < now:
        base = now
    new_exp = (base + datetime.timedelta(days=jours)).isoformat()
    return api("students", method="PATCH", body={"date_expiration_code": new_exp},
               params={"id": f"eq.{student_id}"})

def suspendre(student_id):
    """Suspend le code de ref : l'élève ne peut plus se connecter."""
    return api("students", method="PATCH", body={"statut_actif": False},
               params={"id": f"eq.{student_id}"})

def reprendre(student_id):
    """Réactive un code suspendu."""
    return api("students", method="PATCH", body={"statut_actif": True},
               params={"id": f"eq.{student_id}"})

def regen_auto(student_id):
    """Régénère automatiquement un nouveau code (jamais de saisie manuelle)."""
    return api("students", method="PATCH", body={"code_reference": gen_code()},
               params={"id": f"eq.{student_id}"})

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button

    class AdminApp(App):
        def build(self):
            self.title = "3AS LG Admin"
            root = BoxLayout(orientation="vertical", padding=10, spacing=8)
            root.add_widget(Label(text="🛠️ 3AS LG — Admin"))
            self.nom = TextInput(hint_text="Nom", size_hint_y=None, height=45)
            self.prenom = TextInput(hint_text="Prénom", size_hint_y=None, height=45)
            self.info = Label(text="")
            btn = Button(text="Créer élève + code auto", size_hint_y=None, height=50)
            btn.bind(on_press=self.do_create)
            root.add_widget(self.nom); root.add_widget(self.prenom)
            root.add_widget(btn); root.add_widget(self.info)
            return root
        def do_create(self, *_):
            try:
                s = create_student(self.nom.text, self.prenom.text)
                self.info.text = "Code: " + s.get("code_reference", "?")
            except Exception as e:
                self.info.text = "Erreur: " + str(e)[:200]

    if __name__ == "__main__":
        AdminApp().run()
except ImportError:
    if __name__ == "__main__":
        print("Kivy non installé. Logique OK, SB configuré:", bool(SB_URL))
        print("Exemple code:", gen_code())
