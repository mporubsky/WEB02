/*
 * audit_browser.js — audit hotového webu v reálnom prehliadači (mobil + desktop).
 *
 * Dopĺňa verify_site.js (chyby JS, rozbité assety) a audit_html.py (zdrojový kód).
 * Tento skript meria to, čo vznikne až po vykreslení — a čo klient nahlási ako
 * „rozbité na mobile" alebo „to sa nedá prečítať":
 *
 *   1. HORIZONTÁLNE PRETEČENIE — stránka sa dá ťahať do strán. Nájde presný
 *      vinníkovský prvok a ignoruje prvky vo vnútri scroll-kontajnerov
 *      (široká tabuľka v `overflow-x:auto` je v poriadku, nie chyba).
 *   2. KONTRAST TEXTU (WCAG AA) — počíta pomer jasu textu a pozadia.
 *      Prvky nad gradientom/fotkou nehlási ako chybu (pozadie sa nedá spoľahlivo
 *      odvodiť), ale vypíše ich zvlášť na vizuálnu kontrolu — inak by skript
 *      zahltil falošnými poplachmi a skutočné chyby by v nich zanikli.
 *   3. DOTYKOVÉ PLOCHY (WCAG 2.5.8, min. 24 px) — samostatné odkazy/tlačidlá.
 *      Odkazy vnútri vety sú podľa normy výnimka, preto sa nehlásia.
 *   4. NENAPLNENÉ ÚDAJE — prvky data-mh, v ktorých ostal zástupný text.
 *   5. Chyby konzoly, nenačítané obrázky, polia formulára bez labelu.
 *
 * Predpoklad: `playwright-core`, Chromium na /opt/pw-browsers.
 *
 * Použitie:
 *   node audit_browser.js [--root .] [--placeholders 'XX|TODO']
 *
 * Návratový kód != 0 pri nájdenom probléme.
 */
const fs = require('fs'), path = require('path');
const { chromium } = require('playwright-core');

const args = process.argv.slice(2);
if (args.includes('--help') || args.includes('-h')) {
  console.log('audit_browser.js — audit vykresleného webu (pretečenie, kontrast, dotykové plochy).\n' +
    '  node audit_browser.js [--root .] [--placeholders \'XX|TODO\']\n' +
    '  --root         : priečinok s .html súbormi (predvolene aktuálny)\n' +
    '  --placeholders : regex zástupných textov hľadaných v data-mh prvkoch\n' +
    'Návratový kód != 0 pri nájdenom probléme.');
  process.exit(0);
}
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const ROOT = path.resolve(opt('--root', '.'));
// Pozor aj na „x-kové" výplne v e-mailoch a doménach (info@xxxx.sk) – tie
// vyzerajú ako reálny údaj a prejdú aj cez kontrolu odkazov.
const PLACEHOLDER = opt('--placeholders', 'XX XXX|[Xx]{3,}|\\bTODO\\b|\\{\\{');
const CHROME = require('child_process').execSync(
  "ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1").toString().trim();

const VIEWPORTS = [{ n: 'mobil', width: 390, height: 844 }, { n: 'desktop', width: 1280, height: 900 }];

(async () => {
  const pages = fs.readdirSync(ROOT).filter(f => f.endsWith('.html')).sort();
  if (!pages.length) { console.error('Nenašiel som .html súbory v ' + ROOT); process.exit(2); }

  const browser = await chromium.launch({ executablePath: CHROME });
  const problems = [], review = [];

  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: 1 });
    for (const file of pages) {
      const pg = await ctx.newPage();
      const errs = [];
      pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
      pg.on('pageerror', e => errs.push('JS: ' + e.message));
      await pg.goto('file://' + path.join(ROOT, file), { waitUntil: 'networkidle' });
      // odhaliť reveal prvky, nech sa dajú zmerať (inak majú opacity:0)
      await pg.evaluate(() => document.querySelectorAll('[data-reveal]').forEach(e => e.classList.add('is-visible')));
      await pg.waitForTimeout(250);

      const r = await pg.evaluate((phRe) => {
        const out = { overflow: null, culprits: [], contrast: [], onImage: [], taps: [], unbound: [], broken: [], unlabeled: [] };
        const vw = document.documentElement.clientWidth;

        const inScroller = el => {
          for (let n = el.parentElement; n && n !== document.body; n = n.parentElement)
            if (/auto|scroll|hidden/.test(getComputedStyle(n).overflowX)) return true;
          return false;
        };
        if (document.documentElement.scrollWidth > vw + 1) {
          out.overflow = { scrollW: document.documentElement.scrollWidth, vw };
          document.querySelectorAll('body *').forEach(e => {
            const b = e.getBoundingClientRect();
            if (b.width > 0 && b.height > 0 && b.right > vw + 1 && !inScroller(e))
              out.culprits.push(`<${e.tagName.toLowerCase()} class="${(e.className || '').toString().slice(0, 40)}"> presahuje o ${Math.round(b.right - vw)}px`);
          });
          out.culprits = out.culprits.slice(0, 5);
        }

        // ---- kontrast ----
        const lum = c => { const [r, g, b] = c.map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return .2126 * r + .7152 * g + .0722 * b; };
        const parse = s => { const m = (s || '').match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(parseFloat); return { rgb: p.slice(0, 3), a: p.length > 3 ? p[3] : 1 }; };
        document.querySelectorAll('body *').forEach(el => {
          const ownText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
          if (!ownText) return;
          if (el.closest('[aria-hidden="true"]')) return;   // dekorácia (hviezdičky, ikony) – norma sa na ňu nevzťahuje
          const cs = getComputedStyle(el);
          if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < .5) return;
          const box = el.getBoundingClientRect(); if (box.width < 1 || box.height < 1) return;
          const fg = parse(cs.color); if (!fg) return;

          // pozadie: vystúp nahor po prvú nepriehľadnú farbu; všimni si obrázky/gradienty
          let bg = [255, 255, 255], img = false;
          for (let n = el; n && n !== document.documentElement; n = n.parentElement) {
            const ncs = getComputedStyle(n);
            if (ncs.backgroundImage && ncs.backgroundImage !== 'none') img = true;
            const c = parse(ncs.backgroundColor);
            if (c && c.a > .5) { bg = c.rgb; break; }
          }
          const size = parseFloat(cs.fontSize), large = size >= 24 || (size >= 18.66 && parseInt(cs.fontWeight) >= 700);
          const need = large ? 3 : 4.5;
          const L1 = lum(fg.rgb), L2 = lum(bg);
          const ratio = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
          if (ratio >= need) return;
          const desc = `<${el.tagName.toLowerCase()}.${(el.className || '').toString().split(' ')[0]}> „${el.textContent.trim().slice(0, 34)}" ${ratio.toFixed(2)}:1 (treba ${need}:1)`;
          // nad gradientom/fotkou sa pozadie nedá spoľahlivo zistiť → len na kontrolu
          (img ? out.onImage : out.contrast).push(desc);
        });

        // ---- dotykové plochy (mimo odkazov vo vete) ----
        document.querySelectorAll('a,button').forEach(el => {
          const b = el.getBoundingClientRect(); if (b.width < 1 || b.height < 1) return;
          if (b.height >= 24) return;
          const p = el.parentElement;
          const inSentence = p && [...p.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 2);
          if (inSentence) return;      // výnimka „Inline" podľa WCAG 2.5.8
          out.taps.push(`<a> „${(el.textContent || '').trim().slice(0, 28)}" má výšku ${Math.round(b.height)}px`);
        });

        const re = new RegExp(phRe);
        document.querySelectorAll('[data-mh]').forEach(el => {
          if (re.test(el.textContent)) out.unbound.push(`${el.getAttribute('data-mh')} → „${el.textContent.trim().slice(0, 40)}"`);
        });
        [...document.images].forEach(i => { if (i.complete && i.naturalWidth === 0) out.broken.push(i.getAttribute('src')); });
        document.querySelectorAll('input,select,textarea').forEach(f => {
          if (f.type === 'hidden') return;
          const byFor = f.id && document.querySelector(`label[for="${CSS.escape(f.id)}"]`);
          if (!byFor && !f.getAttribute('aria-label') && !f.closest('label'))
            out.unlabeled.push(f.name || f.id || f.type);
        });
        return out;
      }, PLACEHOLDER);

      const tag = `[${vp.n}] ${file}`;
      errs.forEach(e => problems.push(`${tag}: chyba konzoly – ${e}`));
      if (r.overflow) problems.push(`${tag}: horizontálne pretečenie ${r.overflow.scrollW}px > ${r.overflow.vw}px\n        ${r.culprits.join('\n        ')}`);
      r.contrast.forEach(c => problems.push(`${tag}: slabý kontrast ${c}`));
      r.taps.forEach(t => problems.push(`${tag}: malá dotyková plocha ${t}`));
      r.broken.forEach(b => problems.push(`${tag}: nenačítaný obrázok ${b}`));
      r.unlabeled.forEach(f => problems.push(`${tag}: pole formulára bez labelu: ${f}`));
      r.unbound.forEach(u => problems.push(`${tag}: nenaplnený údaj ${u}`));
      if (vp.n === 'desktop') r.onImage.forEach(c => review.push(`${file}: ${c}`));
      await pg.close();
    }
    await ctx.close();
  }
  await browser.close();

  if (review.length) {
    console.log('— Text nad gradientom/fotkou (skontroluj očami na screenshotoch) —');
    [...new Set(review)].slice(0, 12).forEach(r => console.log('   ' + r));
    console.log('');
  }
  if (problems.length) {
    console.log('❌ Nájdené problémy:\n');
    problems.forEach(p => console.log('  • ' + p));
    process.exit(1);
  }
  console.log('✅ Prehliadač: bez pretečenia, kontrast OK, dotykové plochy OK, údaje naplnené.');
})();
