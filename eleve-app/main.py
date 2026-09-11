"""
3AS LG - App Élève (Kivy + Supabase REST)
Build APK avec Buildozer (pas PyInstaller).
Config: variables d'env SUPABASE_URL, SUPABASE_ANON_KEY ou fichier .env
"""
import os, json, secrets, string, datetime, urllib.request, urllib.parse

TELEGRAM = "https://t.me/Roqaya_2328"

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

def login_code(code):
    code = code.strip().upper()
    rows = api("students", params={"code_reference": f"eq.{code}", "select": "*"})
    if not rows:
        return None, "Code invalide."
    s = rows[0]
    if not s.get("statut_actif"):
        return None, "Compte désactivé."
    exp = s.get("date_expiration_code")
    if exp and exp[:10] < datetime.date.today().isoformat():
        return None, "Code expiré. Contacte l'admin via " + TELEGRAM
    return s, "OK"

def get_courses():
    try:
        return api("courses", params={"select": "*", "order": "matiere,ordre"})
    except Exception as e:
        return [{"matiere": "Allemand", "chapitre": "Passiv (offline)",
                 "contenu_cours": "werden + Partizip II", "explications_simplifiees": str(e)}]

def get_messages(student_id):
    return api("messages", params={"student_id": f"eq.{student_id}", "select": "*", "order": "timestamp"})

def send_message(student_id, contenu):
    return api("messages", method="POST",
               body={"sender_id": student_id, "receiver_id": "admin",
                     "contenu": contenu, "student_id": student_id})

# ---------- UI Kivy (chargée seulement si kivy installé) ----------
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.uix.scrollview import ScrollView

    class EleveApp(App):
        def build(self):
            self.title = "3AS LG Élève"
            root = BoxLayout(orientation="vertical", padding=10, spacing=8)
            root.add_widget(Label(text="📚 3AS LG — Élève\nCode fourni par l'admin\nSupport: t.me/Roqaya_2328"))
            self.code = TextInput(hint_text="Code ex: 3AS-X7K9P2", size_hint_y=None, height=50)
            self.info = Label(text="")
            btn = Button(text="Se connecter", size_hint_y=None, height=50)
            btn.bind(on_press=self.do_login)
            self.cours = Label(text="", size_hint_y=None)
            root.add_widget(self.code); root.add_widget(btn); root.add_widget(self.info)
            return root
        def do_login(self, *_):
            try:
                s, msg = login_code(self.code.text)
                self.info.text = f"Bienvenue {s['prenom']} {s['nom']}" if s else msg
                if s:
                    cs = get_courses()
                    self.info.text += f"\n{len(cs)} cours disponibles."
            except Exception as e:
                self.info.text = "Erreur: " + str(e)[:200]

    if __name__ == "__main__":
        EleveApp().run()
except ImportError:
    if __name__ == "__main__":
        print("Kivy non installé. Test logique sans UI:")
        print("SB_URL configuré:", bool(SB_URL))
