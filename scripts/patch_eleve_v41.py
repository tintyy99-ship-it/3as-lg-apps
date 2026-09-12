# -*- coding: utf-8 -*-
"""Élève v4.1 : viewList détail, burger caché au login, entrée directe, anim matière."""
import pathlib

p = pathlib.Path('/root/3as-lg-apps/eleve-app/web/index.html')
h = p.read_text(encoding='utf-8')
assert h.count('<!DOCTYPE') == 1

# ---------- CSS : anim ouverture matière + burger caché ----------
old = "#drawer.hidden{transform:translateX(105%)}"
assert old in h, "drawer css"
h = h.replace(old, """#drawer.hidden{transform:translateX(105%)}
#drawer{transition:transform .38s cubic-bezier(.2,.9,.25,1.05)}
#drawerOv{transition:opacity .3s}
#burger{display:none}
@keyframes slideBlur{0%{opacity:0;transform:translateY(26px);filter:blur(10px)}60%{opacity:1;filter:blur(2px)}100%{opacity:1;transform:none;filter:blur(0)}}
.anim-in{animation:slideBlur .45s ease}
.crow{transition:transform .15s}
.crow:active{transform:scale(.98)}""", 1)

# ---------- viewList ----------
old = "let curM='', curT=0, curQ='', curD=-1;"
assert old in h, "cur decl"
h = h.replace(old, "let curM='', curT=0, curQ='', curD=-1, viewList=[];", 1)

old = """function renderCourses(){
 const list=filtered();"""
assert old in h, "render head"
h = h.replace(old, """function renderCourses(){
 const list=filtered();viewList=list;
 animCourses();""", 1)

old = """function showDetail(){
 const item=allCourses[curD];
 if(!item){go('#/');return}"""
assert old in h, "detail head"
h = h.replace(old, """function animCourses(){const c=$('courses');if(!c)return;c.classList.remove('anim-in');void c.offsetWidth;c.classList.add('anim-in')}
function showDetail(){
 const item=((viewList[curD]||{}).c)||allCourses[curD];
 if(!item){go('#/');return}""", 1)

# ---------- setM/setT rejouent l'anim ----------
old = "function setM(m){curM=m;buildChips();renderCourses()}"
assert old in h, "setM"
# renderCourses appelle déjà animCourses -> rien à faire
assert "animCourses();" in h

# ---------- burger visible après login seulement ----------
old = " $('login').classList.add('hidden');$('app').classList.remove('hidden');$('navbar').classList.remove('hidden');"
assert old in h, "boot show"
h = h.replace(old, old + "$('burger').style.display='block';", 1)

# ---------- entrée directe : boot d'abord, portes par-dessus ----------
old = " me=data;localStorage.setItem('3as_student',JSON.stringify(me));playDoors(boot);"
assert old in h, "login doors"
h = h.replace(old, " me=data;localStorage.setItem('3as_student',JSON.stringify(me));boot();playDoors(null);", 1)

old = "function playDoors(next){const d=$('doors');d.classList.remove('hidden');requestAnimationFrame(()=>requestAnimationFrame(()=>d.classList.add('open')));setTimeout(()=>{d.classList.add('hidden');d.classList.remove('open');next()},1150)}"
assert old in h, "playDoors"
h = h.replace(old, "function playDoors(next){const d=$('doors');if(!d){if(next)next();return}d.onclick=()=>{d.classList.add('hidden');d.classList.remove('open')};d.classList.remove('hidden');requestAnimationFrame(()=>requestAnimationFrame(()=>d.classList.add('open')));setTimeout(()=>{d.classList.add('hidden');d.classList.remove('open');if(next)next()},850)}", 1)

p.write_text(h, encoding='utf-8')
print('eleve v4.1 patched')
