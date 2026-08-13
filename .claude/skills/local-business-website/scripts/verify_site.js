/*
 * verify_site.js — automatická kontrola statického webu pred odovzdaním.
 * Spúšťaj VŽDY po zostavení webu — odhalí presne tie chyby, ktoré sa ľahko
 * prehliadnu: JS chyby, rozbité interné odkazy/assety, chýbajúcu prístupnosť,
 * nefunkčné menu. Robí aj screenshoty na vizuálnu kontrolu.
 *
 * Predpoklad: nainštalované `playwright-core`, Chromium na /opt/pw-browsers.
 *
 * Použitie:
 *   node verify_site.js [--root .] [--shots shots] [--ignore '\.jpg$']
 *   --ignore : regex na cesty, ktoré smú 404-ovať (napr. fotky s onerror fallbackom)
 *
 * Návratový kód != 0 pri reálnych problémoch (chyby JS, chýbajúce assety).
 */
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require('playwright-core');

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const ROOT = path.resolve(opt('--root', '.'));
const SHOTS = path.resolve(opt('--shots', path.join(ROOT, '_verify_shots')));
const IGNORE = opt('--ignore', null) ? new RegExp(opt('--ignore', null)) : null;
const CHROME = require('child_process').execSync(
  "ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1").toString().trim();

const MIME = { '.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml',
  '.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.json':'application/json',
  '.webmanifest':'application/manifest+json','.xml':'application/xml','.ico':'image/x-icon' };

function serve(port) {
  return new Promise(res => {
    const s = http.createServer((req, rq) => {
      let p = decodeURIComponent(req.url.split('?')[0]); if (p === '/') p = '/index.html';
      const f = path.join(ROOT, p);
      if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { rq.writeHead(404); rq.end('nf'); return; }
      rq.writeHead(200, { 'Content-Type': MIME[path.extname(f)] || 'application/octet-stream' });
      rq.end(fs.readFileSync(f));
    });
    s.listen(port, () => res(s));
  });
}

(async () => {
  fs.mkdirSync(SHOTS, { recursive: true });
  const pages = fs.readdirSync(ROOT).filter(f => f.endsWith('.html'));
  const server = await serve(8399);
  const b = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const problems = [];

  for (const name of pages) {
    const page = await b.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(`JS: ${e.message}`));
    page.on('console', m => { if (m.type() === 'error') {
      const t = m.text();
      if (/404|Failed to load resource/.test(t)) return; // rieši sa nižšie cez asset check
      errs.push(`console: ${t}`);
    }});
    // Sledujeme len SAME-ORIGIN assety. Externé embedy (Google mapa, analytics)
    // sem nepatria — ich dostupnosť nie je chyba webu (a v sandboxe bývajú blokované).
    const BASE = 'http://localhost:8399/';
    const failed = [];
    page.on('requestfailed', r => { if (r.url().startsWith(BASE)) failed.push(r.url()); });
    page.on('response', r => { if (r.status() === 404 && r.url().startsWith(BASE)) failed.push(r.url()); });

    await page.goto(`http://localhost:8399/${name}`, { waitUntil: 'networkidle' });

    // a11y & štruktúra
    const checks = await page.evaluate(() => ({
      h1: document.querySelectorAll('h1').length,
      hasSkip: !!document.querySelector('.skip-link, [href="#obsah"], [href="#content"], [href="#main"]'),
      lang: document.documentElement.getAttribute('lang'),
      title: (document.title || '').length,
      viewport: !!document.querySelector('meta[name="viewport"]'),
    }));
    if (checks.h1 !== 1) problems.push(`${name}: očakávaný 1× <h1>, nájdených ${checks.h1}`);
    if (!checks.lang) problems.push(`${name}: chýba lang na <html>`);
    if (!checks.title) problems.push(`${name}: prázdny <title>`);
    if (!checks.viewport) problems.push(`${name}: chýba meta viewport`);

    // 404 assety (okrem ignorovaných)
    for (const u of failed) {
      const rel = u.replace('http://localhost:8399/', '');
      if (IGNORE && IGNORE.test(rel)) continue;
      problems.push(`${name}: 404 → ${rel}`);
    }
    for (const e of errs) problems.push(`${name}: ${e}`);

    // mobilné menu (ak existuje)
    const hasToggle = await page.$('.nav-toggle, [aria-controls]');
    if (hasToggle) {
      await page.setViewportSize({ width: 390, height: 800 });
      await page.click('.nav-toggle').catch(() => {});
      await page.waitForTimeout(250);
      const open = await page.evaluate(() => {
        const n = document.querySelector('.main-nav, nav[id]');
        return n ? (n.classList.contains('is-open') || getComputedStyle(n).transform !== 'none') : true;
      });
      if (!open) problems.push(`${name}: mobilné menu sa neotvorilo po kliknutí na .nav-toggle`);
      await page.setViewportSize({ width: 1280, height: 900 });
    }

    // screenshot (reveal prvky zviditeľníme, aby bol screenshot úplný)
    await page.evaluate(() => document.querySelectorAll('[data-reveal]').forEach(e => e.classList.add('is-visible')));
    await page.waitForTimeout(200);
    await page.screenshot({ path: path.join(SHOTS, name.replace('.html', '') + '.png'), fullPage: true });
    await page.close();
  }

  await b.close(); server.close();

  console.log(`\nSkontrolovaných stránok: ${pages.length}`);
  console.log(`Screenshoty: ${SHOTS}`);
  if (problems.length) {
    console.log(`\n❌ PROBLÉMY (${problems.length}):`);
    problems.forEach(p => console.log('  - ' + p));
    process.exit(1);
  } else {
    console.log('\n✅ Bez problémov: žiadne JS chyby, všetky assety existujú, štruktúra OK.');
  }
})().catch(e => { console.error(e); process.exit(1); });
