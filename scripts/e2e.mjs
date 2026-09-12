// Test E2E 3AS LG — tourne en CI (Playwright + Chromium) AVANT le build APK.
// Vérifie : pas d'erreur JS, login par code, liste cours, DÉTAIL cours, envoi message, unlock admin.
import { chromium } from 'playwright';
import { createClient } from '@supabase/supabase-js';

const SB_URL = process.env.SB_URL;
const SB_ANON = process.env.SB_ANON;
const ADMIN_PW = process.env.ADMIN_PW;
const E_URL = process.env.E_URL || 'http://localhost:8091/';
const A_URL = process.env.A_URL || 'http://localhost:8092/';
if (!SB_URL || !SB_ANON || !ADMIN_PW) { console.error('E2E: secrets manquants'); process.exit(2); }

const sb = createClient(SB_URL, SB_ANON);
const errors = [];
let failed = false;
function ok(name, cond, extra = '') {
  console.log((cond ? 'PASS ' : 'FAIL ') + name + (extra ? ` (${extra})` : ''));
  if (!cond) failed = true;
}
const CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const rand = (n) => Array.from({ length: n }, () => CHARS[Math.floor(Math.random() * CHARS.length)]).join('');
const CODE = '3AS-E2E' + rand(3);
let studentId = null;

const browser = await chromium.launch();
try {
  // ---------- préparation : crée un élève de test via l'API ----------
  const exp = new Date(Date.now() + 30 * 864e5).toISOString();
  const { data: created, error: cErr } = await sb.from('students')
    .insert({ nom: 'E2E', prenom: 'Test', code_reference: CODE, date_expiration_code: exp, statut_actif: true })
    .select();
  ok('setup: élève test créé', !cErr && created && created.length === 1, cErr?.message || CODE);
  studentId = created[0].id;

  // ---------- APP ÉLÈVE ----------
  const page = await browser.newPage();
  page.on('pageerror', (e) => errors.push('eleve pageerror: ' + e.message + ' || ' + (e.stack || '').split('\n').slice(0, 4).join(' <- ')));
  page.on('console', (m) => { if (m.type() === 'error') errors.push('eleve console: ' + m.text().slice(0, 200)); });
  await page.goto(E_URL, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('#splash.hide', { timeout: 15000 });
  ok('eleve: splash disparaît', true);
  await page.fill('#code', CODE);
  await page.click('#lg-go');
  await page.waitForSelector('#app:not(.hidden)', { timeout: 20000 });
  ok('eleve: login par code', true);
  await page.waitForSelector('.crow', { timeout: 20000 });
  const n = await page.locator('.crow').count();
  ok('eleve: cours listés (120 attendus)', n >= 100, String(n));
  await page.locator('.crow', { hasText: 'الألمانية' }).first().click();
  await page.waitForSelector('#tab-detail:not(.hidden)', { timeout: 10000 });
  const detailLen = (await page.locator('#tab-detail .detail').innerText()).length;
  ok('eleve: DÉTAIL du cours affiché (complet)', detailLen > 300, detailLen + ' cars');
  // burger : ouvre et choisit un trimestre
  await page.click('#b1');
  await page.click('#burger');
  await page.waitForSelector('#drawer:not(.hidden)', { timeout: 5000 });
  ok('eleve: burger s\'ouvre', true);
  await page.locator('#dMats .drow').nth(1).click();
  const n2 = await page.locator('.crow').count();
  ok('eleve: filtre matière (pas d\'anarchie)', n2 > 0 && n2 < n, `${n2}/${n}`);
  // messagerie : envoi
  await page.click('#b2');
  await page.fill('#txt', 'Bonjour E2E ' + Date.now());
  await page.locator('.sendbar button').click();
  await page.waitForSelector('.msg.me', { timeout: 15000 });
  ok('eleve: message envoyé', true);
  await page.close();

  // ---------- APP ADMIN ----------
  const pa = await browser.newPage();
  pa.on('pageerror', (e) => errors.push('admin pageerror: ' + e.message + ' || ' + (e.stack || '').split('\n').slice(0, 4).join(' <- ')));
  pa.on('console', (m) => { if (m.type() === 'error') errors.push('admin console: ' + m.text().slice(0, 200)); });
  await pa.goto(A_URL, { waitUntil: 'domcontentloaded' });
  await pa.waitForSelector('#splash.hide', { timeout: 15000 });
  ok('admin: splash disparaît', true);
  await pa.fill('#pw', ADMIN_PW);
  await pa.locator('#lock button').click();
  await pa.waitForFunction(() => document.getElementById('lock').style.display === 'none', null, { timeout: 15000 });
  ok('admin: unlock mot de passe', true);
  await pa.waitForSelector('#inbox', { timeout: 15000 });
  const inboxCount = await pa.locator('#inbox .conv').count();
  ok('admin: inbox chargée', inboxCount >= 1, String(inboxCount));
  // suspendre / réactiver l'élève test depuis le tableau
  await pa.fill('#q', 'E2ETest');
  await pa.waitForTimeout(500);
  const suspBtn = pa.locator('button:has-text("Suspendre")').first();
  if (await suspBtn.count()) {
    await suspBtn.click();
    await pa.locator('#mok').click();
    await pa.waitForTimeout(1500);
    const { data: s1 } = await sb.from('students').select('statut_actif').eq('id', studentId).single();
    ok('admin: ⛔ suspendre fonctionne', s1 && s1.statut_actif === false);
    const reactBtn = pa.locator('button:has-text("Réactiver")').first();
    await reactBtn.click();
    await pa.waitForTimeout(1500);
    const { data: s2 } = await sb.from('students').select('statut_actif').eq('id', studentId).single();
    ok('admin: ✅ réactiver fonctionne', s2 && s2.statut_actif === true);
  } else {
    ok('admin: bouton suspendre présent', false);
  }
  await pa.close();
} catch (e) {
  console.error('E2E EXCEPTION:', e.message);
  failed = true;
} finally {
  // ---------- nettoyage ----------
  if (studentId) {
    await sb.from('messages').delete().eq('student_id', studentId);
    await sb.from('students').delete().eq('id', studentId);
    console.log('cleanup: élève test supprimé');
  }
  await browser.close();
}
if (errors.length) { console.error('ERREURS JS:', errors); failed = true; }
else console.log('PASS aucune erreur JS');
process.exit(failed ? 1 : 0);
