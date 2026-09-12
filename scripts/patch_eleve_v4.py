# -*- coding: utf-8 -*-
"""Élève v4 : splash + portes login + login 2026 + drawer burger + i18n AR/FR/EN + coefs."""
import pathlib

p = pathlib.Path('/root/3as-lg-apps/eleve-app/web/index.html')
h = p.read_text(encoding='utf-8')

# ---------- 1. CSS : splash + portes + login 2026 + drawer ----------
old_style_tail = ".themegrid button.active{outline:3px solid var(--me)}\n</style>"
assert old_style_tail in h, "css tail"
new_css = """.themegrid button.active{outline:3px solid var(--me)}
#splash{position:fixed;inset:0;z-index:400;background:linear-gradient(140deg,#1e1b4b 0%,#4c1d95 35%,#2563eb 70%,#06b6d4 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;transition:opacity .5s}
#splash.hide{opacity:0;pointer-events:none}
.slogo{font-size:64px;font-weight:900;color:#fff;letter-spacing:4px;animation:pop 1.2s ease infinite alternate;text-shadow:0 6px 30px rgba(0,0,0,.5)}
.slogo span{background:linear-gradient(180deg,#fde68a,#f59e0b);-webkit-background-clip:text;background-clip:text;color:transparent}
@keyframes pop{from{transform:scale(1)}to{transform:scale(1.07)}}
.ssub{color:#e0e7ff;font-size:15px}
.sbar{width:180px;height:8px;border-radius:6px;background:rgba(255,255,255,.25);overflow:hidden}
.sbar i{display:block;height:100%;width:40%;border-radius:6px;background:#fff;animation:load 1.1s linear infinite}
@keyframes load{from{transform:translateX(220%)}to{transform:translateX(-320%)}}
#doors{position:fixed;inset:0;z-index:300}
#doors.hidden{display:none}
.dp{position:absolute;top:0;bottom:0;width:51%;transition:transform .95s ease}
#dpR{right:0;background:linear-gradient(160deg,#1e1b4b,#4c1d95)}
#dpL{left:0;background:linear-gradient(200deg,#1e40af,#06b6d4)}
#doors.open #dpR{transform:translateX(110%)}
#doors.open #dpL{transform:translateX(-110%)}
.dlogo{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-size:44px;font-weight:900;transition:opacity .4s;text-shadow:0 4px 20px rgba(0,0,0,.5)}
#doors.open .dlogo{opacity:0}
.authWrap{position:relative;overflow:hidden;border-radius:20px;padding:26px 18px;margin:14px 12px;background:linear-gradient(150deg,#1e1b4b,#4c1d95 55%,#2563eb);box-shadow:0 16px 40px rgba(0,0,0,.45)}
.blob{position:absolute;border-radius:50%;filter:blur(40px);opacity:.55;animation:float 7s ease-in-out infinite alternate}
.b1{width:180px;height:180px;background:#06b6d4;top:-50px;left:-50px}
.b2{width:220px;height:220px;background:#f472b6;bottom:-70px;right:-60px;animation-delay:2s}
@keyframes float{from{transform:translateY(0)}to{transform:translateY(26px)}}
.authCard{position:relative;background:rgba(255,255,255,.12);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.35);border-radius:18px;padding:20px;text-align:center;color:#fff}
.authCard .small{color:#e0e7ff}
.alogo{font-size:52px;font-weight:900;letter-spacing:3px}
.alogo span{background:linear-gradient(180deg,#fde68a,#f59e0b);-webkit-background-clip:text;background-clip:text;color:transparent}
.asub{color:#e0e7ff;margin-bottom:8px;font-size:14px}
#code{background:rgba(255,255,255,.95);border:2px solid #fff;text-align:center;letter-spacing:3px;font-weight:800;font-size:19px;color:#1e1b4b;box-shadow:0 0 0 4px rgba(255,255,255,.25),0 8px 22px rgba(0,0,0,.35)}
.cta{font-size:18px !important;padding:14px !important;background:linear-gradient(180deg,#fbbf24,#d97706) !important;border-bottom-color:#92400e !important;box-shadow:0 5px 0 rgba(120,53,15,.8),0 10px 26px rgba(217,119,6,.55) !important}
#burger{position:absolute;top:8px;inset-inline-start:10px;width:44px;font-size:20px;padding:8px;box-shadow:none;border-bottom-width:2px}
header{position:sticky}
#drawerOv{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:150}
#drawer{position:fixed;top:0;bottom:0;right:0;width:285px;max-width:85vw;background:var(--card);z-index:151;transition:transform .3s ease;overflow-y:auto;box-shadow:-8px 0 24px rgba(0,0,0,.35);padding:12px}
#drawer.hidden{transform:translateX(105%)}
[dir="ltr"] #drawer{right:auto;left:0}
[dir="ltr"] #drawer.hidden{transform:translateX(-105%)}
.dhead{display:flex;justify-content:space-between;align-items:center;font-weight:800;margin-bottom:6px}
.dhead span{cursor:pointer;font-size:18px}
.dsec{font-weight:800;color:var(--me);margin:10px 2px 4px;font-size:14px}
.drow{display:flex;align-items:center;gap:8px;padding:9px 10px;border-radius:10px;cursor:pointer;font-size:14px}
.drow:hover{background:var(--them)}
.drow.active{background:var(--them);outline:2px solid var(--me);font-weight:800}
.drow .cnt{margin-inline-start:auto;font-size:12px;color:var(--mut)}
.dcoef{font-size:11px;background:var(--me);color:#fff;border-radius:8px;padding:1px 7px}
.archnote{background:var(--them);border-radius:8px;padding:6px 10px;font-size:12px;color:var(--mut);margin:4px 0}
</style>"""
h = h.replace(old_style_tail, new_css)

# ---------- 2. header + burger + drawer + splash + portes ----------
old = '<header><h2>📚 الثالثة ثانوي لغات — فضاء التلميذ</h2></header>'
assert old in h, "header"
h = h.replace(old, '''<header><button id="burger" onclick="toggleDrawer(true)">☰</button><h2 id="hdr">📚 الثالثة ثانوي لغات — فضاء التلميذ</h2></header>
<div id="splash"><div class="slogo">3AS <span>LG</span></div><div class="ssub" id="splashsub">دروس • شروح • مراسلة</div><div class="sbar"><i></i></div></div>
<div id="doors" class="hidden"><div class="dp" id="dpR"></div><div class="dp" id="dpL"></div><div class="dlogo">3AS LG<br><small style="font-size:18px">👋</small></div></div>
<div id="drawerOv" class="hidden" onclick="toggleDrawer(false)"></div>
<aside id="drawer" class="hidden"><div class="dhead"><span id="dr-h">📚 المواد والفصول</span><span onclick="toggleDrawer(false)">✕</span></div>
<div class="dsec" id="dr-m">المواد</div><div id="dMats"></div>
<div class="dsec" id="dr-t">الفصول</div><div id="dTrims"></div></aside>''')

# ---------- 3. login 2026 ----------
i = h.find('<div id="login" class="card">')
assert i >= 0, "login div"
j = h.find('</div>', h.find('loginErr', i)) + len('</div>')
new_login = '''<div id="login" class="authWrap"><div class="blob b1"></div><div class="blob b2"></div>
<div class="authCard"><div class="alogo">3AS <span>LG</span></div><div class="asub" id="lg-sub">دروس • شروح • مراسلة</div>
<h3 id="lg-h">🔑 الدخول</h3>
<p class="small" id="lg-p">رمز الدخول الخاص بك يعطيه لك الأستاذ المشرف.<br>للدروس والشروحات أو لطلب رمز، راسل الدعم :</p>
<a href="https://t.me/Roqaya_2328" target="_blank"><button class="telegram" id="lg-tg">💬 دعم تيليغرام : @Roqaya_2328</button></a>
<input id="code" placeholder="3AS-XXXXXX">
<button class="cta" onclick="login()" id="lg-go">دخول ✨</button>
<p id="loginErr" class="small" style="color:#fecaca"></p>
</div></div>'''
h = h[:i] + new_login + h[j:]

# ---------- 4. IDs statiques + sélecteur langue ----------
subs = [
    ('<h3>📖 مواد السنة الثالثة لغات</h3>', '<h3 id="ch">📖 مواد السنة الثالثة لغات</h3>'),
    ('<input id="q" placeholder="🔍 ابحث في الدروس…" oninput="renderCourses()">',
     '<input id="q" placeholder="🔍 ابحث في الدروس…" oninput="renderCourses()">'),
    ('<button class="ghost backbtn" onclick="go(\'#/\')">→ رجوع للدروس</button>',
     '<button class="ghost backbtn" onclick="go(\'#/\')" id="bkbtn">→ رجوع للدروس</button>'),
    ('<div><b>الأستاذ المشرف</b><br><span class="small">دائما معك 🤝</span></div>',
     '<div><b id="chn">الأستاذ المشرف</b><br><span class="small" id="chs">دائما معك 🤝</span></div>'),
    ('<div id="ephlbl" class="eph hidden">🕐 الرسائل مؤقتة وتُحذف تلقائيا</div>',
     '<div id="ephlbl" class="eph hidden">🕐 الرسائل مؤقتة وتُحذف تلقائيا</div>'),
    ('<input id="txt" placeholder="اكتب للأستاذ…" onkeydown="if(event.key===\'Enter\')send()">',
     '<input id="txt" placeholder="اكتب للأستاذ…" onkeydown="if(event.key===\'Enter\')send()">'),
    ('<div class="card"><h3>👤 حسابي</h3><div id="profil"></div>',
     '<div class="card"><h3 id="cph">👤 حسابي</h3><div id="profil"></div><h3 id="lngh" style="margin-top:10px">🌍 اللغة</h3><div class="themegrid"><button id="ln-ar" onclick="setLang(\'ar\')">🇩🇿 عربية</button><button id="ln-fr" onclick="setLang(\'fr\')">🇫🇷 Français</button><button id="ln-en" onclick="setLang(\'en\')">🇬🇧 English</button></div>'),
    ('<h3 style="margin-top:10px">🎨 المظهر</h3>', '<h3 id="thh" style="margin-top:10px">🎨 المظهر</h3>'),
    ('<button id="th-l" onclick="setTheme(\'light\')">☀️ فاتح</button>', '<button id="th-l" onclick="setTheme(\'light\')">☀️ فاتح</button>'),
    ('<button id="th-d" onclick="setTheme(\'dark\')">🌙 داكن</button>', '<button id="th-d" onclick="setTheme(\'dark\')">🌙 داكن</button>'),
    ('<button id="th-a" onclick="setTheme(\'auto\')">📱 النظام</button>', '<button id="th-a" onclick="setTheme(\'auto\')">📱 النظام</button>'),
    ('<button id="b1" onclick="go(\'#/\')">📖 الدروس</button>', '<button id="b1" onclick="go(\'#/\')">📖 الدروس</button>'),
    ('<a href="https://t.me/Roqaya_2328" target="_blank"><button class="telegram">مراسلة الدعم تيليغرام</button></a>',
     '<a href="https://t.me/Roqaya_2328" target="_blank"><button class="telegram" id="cptg">مراسلة الدعم تيليغرام</button></a>'),
]
for old, new in subs:
    assert old in h, "missing: " + old[:40]
    h = h.replace(old, new)

# ---------- 5. JS : i18n + drawer + portes + coefs ----------
old = "const TRIMN={1:\"الفصل الأول\",2:\"الفصل الثاني\",3:\"الفصل الثالث\"};"
assert old in h, "trimn"
h = h.replace(old, '''const MAT_COEF={"الألمانية":6,"الإسبانية":6,"الإيطالية":6,"الإنجليزية":4,"الفرنسية":4,"العربية":2,"التاريخ":2,"الجغرافيا":2,"العلوم الإسلامية":2,"الأمازيغية":2,"الفلسفة":0,"الرياضيات":0};
let LANG=localStorage.getItem('3as_lang')||'ar';
const STR={
ar:{hdr:"📚 الثالثة ثانوي لغات — فضاء التلميذ",sub:"دروس • شروح • مراسلة",lgh:"🔑 الدخول",lgp:"رمز الدخول الخاص بك يعطيه لك الأستاذ المشرف.",lgtg:"💬 دعم تيليغرام : @Roqaya_2328",codeph:"3AS-XXXXXX",go:"دخول ✨",e_net:"مشكلة في الاتصال، تحقق من الإنترنت وحاول مجددا.",e_empty:"أدخل الرمز من فضلك.",e_bad:"الرمز غير صحيح.",e_susp:"⛔ تم تجميد هذا الرمز. راسل الدعم.",e_exp:"انتهت صلاحية الرمز. اطلب التمديد عبر تيليغرام.",hello:"مرحبا",exp:"ينتهي: ",ch:"📖 مواد السنة الثالثة لغات",qph:"🔍 ابحث في الدروس…",all:"الكل",t1:"الفصل الأول",t2:"الفصل الثاني",t3:"الفصل الثالث",nomatch:"لا توجد دروس مطابقة.",back:"→ رجوع للدروس",full:"اضغط لعرض الدرس الكامل مع الشرح ←",tip:"الزبدة :",chn:"الأستاذ المشرف",chs:"دائما معك 🤝",eph:"🕐 الرسائل مؤقتة وتُحذف تلقائيا",nomsg:"لا رسائل بعد. اكتب للأستاذ 👋",txtph:"اكتب للأستاذ…",senderr:"مشكلة في الاتصال.",cph:"👤 حسابي",code:"الرمز:",valid:"الصلاحية:",lngh:"🌍 اللغة",thh:"🎨 المظهر",thl:"☀️ فاتح",thd:"🌙 داكن",tha:"📱 النظام",cptg:"مراسلة الدعم تيليغرام",n1:"📖 الدروس",n2:"💬 المراسلة",n3:"👤 حسابي",drm:"المواد",drt:"الفصول",coef:"المعامل",arch:"📦 محفوظ للفائدة — خارج برنامج اللغات 2026"},
fr:{hdr:"📚 3AS Langues — Espace Élève",sub:"Cours • Explications • Messagerie",lgh:"🔑 Connexion",lgp:"Ton code d'accès te donne ton professeur.",lgtg:"💬 Support Telegram : @Roqaya_2328",codeph:"3AS-XXXXXX",go:"Entrer ✨",e_net:"Problème de connexion, vérifie internet.",e_empty:"Entre ton code.",e_bad:"Code invalide.",e_susp:"⛔ Code suspendu. Contacte le support.",e_exp:"Code expiré. Demande une prolongation via Telegram.",hello:"Salut",exp:"Expire : ",ch:"📖 Matières 3AS Langues",qph:"🔍 Rechercher un cours…",all:"Toutes",t1:"Trimestre 1",t2:"Trimestre 2",t3:"Trimestre 3",nomatch:"Aucun cours trouvé.",back:"→ Retour aux cours",full:"Clique pour le cours complet ←",tip:"L'essentiel :",chn:"Professeur",chs:"Toujours avec toi 🤝",eph:"🕐 Messages éphémères (suppression auto)",nomsg:"Aucun message. Écris au prof 👋",txtph:"Écris au prof…",senderr:"Problème de connexion.",cph:"👤 Mon compte",code:"Code :",valid:"Validité :",lngh:"🌍 Langue",thh:"🎨 Thème",thl:"☀️ Clair",thd:"🌙 Sombre",tha:"📱 Système",cptg:"Contacter le support Telegram",n1:"📖 Cours",n2:"💬 Messages",n3:"👤 Compte",drm:"Matières",drt:"Trimestres",coef:"Coef",arch:"📦 Archive — hors programme langues 2026"},
en:{hdr:"📚 3AS Languages — Student Space",sub:"Lessons • Explanations • Chat",lgh:"🔑 Login",lgp:"Your access code is given by your teacher.",lgtg:"💬 Telegram support: @Roqaya_2328",codeph:"3AS-XXXXXX",go:"Enter ✨",e_net:"Connection issue, check internet.",e_empty:"Enter your code.",e_bad:"Invalid code.",e_susp:"⛔ Code suspended. Contact support.",e_exp:"Code expired. Ask for renewal via Telegram.",hello:"Hi",exp:"Expires: ",ch:"📖 3AS Languages subjects",qph:"🔍 Search lessons…",all:"All",t1:"Term 1",t2:"Term 2",t3:"Term 3",nomatch:"No lessons found.",back:"→ Back to lessons",full:"Tap for the full lesson ←",tip:"Key point:",chn:"Teacher",chs:"Always with you 🤝",eph:"🕐 Ephemeral messages (auto-delete)",nomsg:"No messages yet. Write to the teacher 👋",txtph:"Write to the teacher…",senderr:"Connection issue.",cph:"👤 My account",code:"Code:",valid:"Validity:",lngh:"🌍 Language",thh:"🎨 Theme",thl:"☀️ Light",thd:"🌙 Dark",tha:"📱 System",cptg:"Contact Telegram support",n1:"📖 Lessons",n2:"💬 Chat",n3:"👤 Account",drm:"Subjects",drt:"Terms",coef:"Coef",arch:"📦 Archive — off 2026 languages program"}};
function t(k){return (STR[LANG]&&STR[LANG][k])||STR.ar[k]||k}
function setLang(l){LANG=l;localStorage.setItem('3as_lang',l);applyLang()}
function applyLang(){document.documentElement.lang=LANG;document.documentElement.dir=(LANG==='ar')?'rtl':'ltr';
 const S={hdr:'hdr',sub:'splashsub',lgh:'lg-h',lgp:'lg-p',lgtg:'lg-tg',go:'lg-go',ch:'ch',back:'bkbtn',chn:'chn',chs:'chs',eph:'ephlbl',cph:'cph',lngh:'lngh',thh:'thh',cptg:'cptg',n1:'b1',n2:'b2',n3:'b3','drm':'dr-m','drt':'dr-t'};
 for(const k in S){const e=$(S[k]);if(e)e.textContent=t(k)}
 const cp=$('code');if(cp)cp.placeholder=t('codeph');
 const qq=$('q');if(qq)qq.placeholder=t('qph');
 const tx=$('txt');if(tx)tx.placeholder=t('txtph');
 ['ar','fr','en'].forEach(x=>{const b=$('ln-'+x);if(b)b.classList.toggle('active',LANG===x)});
 if(me){$('hello').textContent=`${t('hello')} ${me.prenom} ${me.nom} 👋`;$('exp').textContent=t('exp')+(me.date_expiration_code||'—').slice(0,10);
 $('profil').innerHTML=`<p><b>${me.prenom} ${me.nom}</b><br>${me.email||''}<br>${t('code')} <b>${me.code_reference}</b><br>${t('valid')} ${me.date_expiration_code||'—'}</p>`}
 buildChips();buildTrims();renderCourses();if(curD>=0&&allCourses[curD])showDetail();renderMsgs(msgsCache)}
function toggleDrawer(open){$('drawer').classList.toggle('hidden',!open);$('drawerOv').classList.toggle('hidden',!open)}
const TRIMLOC={1:'t1',2:'t2',3:'t3'};
function TRIMN2(x){return t(TRIMLOC[x]||'')}''')

old = """function buildTrims(){
 $('trims').innerHTML=`<button class="${!curT?'active':''}" onclick="setT(0)">الكل</button>`+[1,2,3].map(t=>`<button class="${curT===t?'active':''}" onclick="setT(${t})">${TRIMN[t]}</button>`).join('');
}"""
assert old in h, "buildTrims"

# buildChips + drawer + coefs
old = """function buildChips(){
 const counts={};allCourses.forEach(c=>counts[c.matiere]=(counts[c.matiere]||0)+1);
 const mats=Object.keys(counts).sort();
 $('chips').innerHTML=`<button class="chip ${!curM?'active':''}" onclick="setM('')">الكل (${allCourses.length})</button>`+
  mats.map(m=>`<button class="chip ${curM===m?'active':''}" onclick="setM('${m}')"><span class="mdot" style="background:${col(m)}"></span>${m} (${counts[m]})</button>`).join('');
}"""
assert old in h, "buildChips"
h = h.replace(old, """function coefOf(m){return (typeof MAT_COEF!=='undefined'&&MAT_COEF[m]!==undefined)?MAT_COEF[m]:''}
function buildChips(){
 const counts={};allCourses.forEach(c=>counts[c.matiere]=(counts[c.matiere]||0)+1);
 const mats=Object.keys(counts).sort();
 const chip=(m,lbl)=>`<button class="chip ${curM===m?'active':''}" onclick="setM('${m}');toggleDrawer(false)">${lbl}</button>`;
 $('chips').innerHTML=chip('',`${t('all')} (${allCourses.length})`)+
  mats.map(m=>chip(m,`<span class="mdot" style="background:${col(m)}"></span>${m} (${counts[m]})${coefOf(m)!==''?` <span class="dcoef">${t('coef')} ${coefOf(m)}`:''}</span>`)).join('');
 $('dMats').innerHTML=`<div class="drow ${!curM?'active':''}" onclick="setM('');toggleDrawer(false)"><b>${t('all')}</b><span class="cnt">${allCourses.length}</span></div>`+
  mats.map(m=>`<div class="drow ${curM===m?'active':''}" onclick="setM('${m}');toggleDrawer(false)"><span class="mdot" style="background:${col(m)}"></span><b>${m}</b>${coefOf(m)!==''?`<span class="dcoef">${coefOf(m)}</span>`:''}<span class="cnt">${counts[m]}</span></div>`).join('');
}""")

old = """function buildTrims(){
 $('trims').innerHTML=`<button class="${!curT?'active':''}" onclick="setT(0)">الكل</button>`+[1,2,3].map(t=>`<button class="${curT===t?'active':''}" onclick="setT(${t})">${TRIMN[t]}</button>`).join('');
}"""
assert old in h, "buildTrims"
h = h.replace(old, """function buildTrims(){
 const tb=(v,l)=>`<button class="${curT===v?'active':''}" onclick="setT(${v});toggleDrawer(false)">${l}</button>`;
 $('trims').innerHTML=tb(0,t('all'))+[1,2,3].map(x=>tb(x,t(TRIMLOC[x]))).join('');
 const tc={};allCourses.filter(c=>!curM||c.matiere===curM).forEach(c=>tc[c.trimestre]=(tc[c.trimestre]||0)+1);
 $('dTrims').innerHTML=`<div class="drow ${!curT?'active':''}" onclick="setT(0);toggleDrawer(false)"><b>${t('all')}</b></div>`+[1,2,3].map(x=>`<div class="drow ${curT===x?'active':''}" onclick="setT(${x});toggleDrawer(false)"><b>${t(TRIMLOC[x])}</b><span class="cnt">${tc[x]||0}</span></div>`).join('');
}""")

# renderCourses : archive + i18n
old = """  h+=`<div class="crow" style="border-inline-start-color:${col(c.matiere)}" onclick="go('#/cours/${i}')">
  <span class="badge" style="background:${col(c.matiere)}">${esc(c.matiere)}</span>
  <span class="small"> — ${TRIMN[c.trimestre]||''}</span>
  <h4>${esc(c.chapitre)}</h4>
  <span class="small">اضغط لعرض الدرس الكامل مع الشرح ←</span></div>`;"""
assert old in h, "crow"
h = h.replace(old, """  h+=`<div class="crow" style="border-inline-start-color:${col(c.matiere)}" onclick="go('#/cours/${i}')">
  <span class="badge" style="background:${col(c.matiere)}">${esc(c.matiere)}</span>
  <span class="small"> — ${t(TRIMLOC[c.trimestre]||'')}</span>
  <h4>${esc(c.chapitre)}</h4>
  <span class="small">${t('full')}</span></div>`;""")

old = "if(sec!==lastSec){lastSec=sec;h+=`<div class=\"sech\">📌 ${esc(sec)}</div>`}"
assert old in h, "sech"
h = h.replace(old, "if(sec!==lastSec){lastSec=sec;const arch=(sec||'').startsWith('📦');h+=`<div class=\"sech\">${arch?'':''}📌 ${esc(sec)}</div>`+(arch?`<div class=\"archnote\">${t('arch')}</div>`:'')}")

old = "$('courses').innerHTML=h||'<p class=\"small\">لا توجد دروس مطابقة.</p>';"
assert old in h, "nomatch"
h = h.replace(old, "$('courses').innerHTML=h||`<p class=\"small\">${t('nomatch')}</p>`;")

# showDetail : tip label
old = "<div class=\"tip\" style=\"background:${cl}14\">💡 <b>الزبدة :</b> ${esc(c.explications_simplifiees||'')}</div>`;"
assert old in h, "tip"
h = h.replace(old, "<div class=\"tip\" style=\"background:${cl}14\">💡 <b>${t('tip')}</b> ${esc(c.explications_simplifiees||'')}</div>`;")

# chat : nomsg + senderr
old = "}).join('')||'<p class=\"small\">لا رسائل بعد. اكتب للأستاذ 👋</p>';"
assert old in h, "nomsg"
h = h.replace(old, "}).join('')||`<p class=\"small\">${t('nomsg')}</p>`;")
old = "if(!sb)return alert('مشكلة في الاتصال.');"
assert old in h, "senderr"
h = h.replace(old, "if(!sb)return alert(t('senderr'));")

# login : erreurs i18n + portes
for ar, key in [
    ("'مشكلة في الاتصال، تحقق من الإنترنت وحاول مجددا.'", "e_net"),
    ("'أدخل الرمز من فضلك.'", "e_empty"),
    ("'الرمز غير صحيح.'", "e_bad"),
    ("'⛔ تم تجميد هذا الرمز. راسل الدعم.'", "e_susp"),
    ("'انتهت صلاحية الرمز. اطلب التمديد عبر تيليغرام.'", "e_exp")]:
    assert ar in h, "loginerr " + key
    h = h.replace("$('loginErr').textContent=" + ar + ";", "$('loginErr').textContent=t('" + key + "');")

old = " me=data;localStorage.setItem('3as_student',JSON.stringify(me));boot();"
assert old in h, "login boot"
h = h.replace(old, """ me=data;localStorage.setItem('3as_student',JSON.stringify(me));playDoors(boot);""")

# playDoors + splash JS + MAT_COEF
old = "function logout(){"
assert old in h, "logout anchor"
h = h.replace(old, """function playDoors(next){const d=$('doors');d.classList.remove('hidden');requestAnimationFrame(()=>requestAnimationFrame(()=>d.classList.add('open')));setTimeout(()=>{d.classList.add('hidden');d.classList.remove('open');next()},1150)}
function logout(){""", 1)

old = "const MAT_COLORS={"
assert old in h, "matcolors"
if 'const MAT_COEF=' not in h:
    h = h.replace(old, "const MAT_COEF=" + open('/tmp/matcoef.txt', encoding='utf-8').read().strip() + ";\nconst MAT_COLORS={", 1)

# boot : applyLang au lieu de applyTheme seul + fermer drawer
old = " $('login').classList.add('hidden');$('app').classList.remove('hidden');$('navbar').classList.remove('hidden');\n applyTheme();"
assert old in h, "boot theme"
h = h.replace(old, " $('login').classList.add('hidden');$('app').classList.remove('hidden');$('navbar').classList.remove('hidden');\n applyTheme();applyLang();toggleDrawer(false);")

# fin : splash hide + applyLang initiale
old = "applyTheme();\nif(me)boot();else{ping()}"
assert old in h, "init fin"
h = h.replace(old, "applyTheme();applyLang();\nwindow.addEventListener('load',()=>setTimeout(()=>$('splash').classList.add('hide'),1500));\nsetTimeout(()=>{const s=$('splash');if(s)s.classList.add('hide')},3500);\nif(me)boot();else{ping()}")

p.write_text(h, encoding='utf-8')
print('eleve v4 patched')
