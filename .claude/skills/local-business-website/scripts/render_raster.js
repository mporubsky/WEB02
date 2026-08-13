/*
 * render_raster.js — vyrenderuje RASTROVÉ obrázky z SVG cez pre-inštalovaný
 * Chromium (playwright-core). Prečo: OG obrázky (náhľady na FB/LinkedIn/iMessage)
 * a niektoré favicony musia byť raster (PNG) — SVG mnohé platformy nezobrazia.
 *
 * Predpoklad: v tomto prostredí je Chromium v /opt/pw-browsers/chromium-<verzia>.
 * Ak treba, nájdi cestu príkazom:
 *   ls -d /opt/pw-browsers/chromium-<verzia>/chrome-linux/chrome
 * a nastav ju cez env premennú CHROME_PATH.
 *
 * Použitie (z koreňa projektu, kde je nainštalované playwright-core):
 *   node render_raster.js
 * Vyrenderuje:
 *   assets/img/og-image.png  (1200x630)  z assets/img/og-image.svg
 *   assets/favicon-32.png, apple-touch-icon.png, icon-192.png, icon-512.png
 *                                        z assets/favicon.svg
 */
const fs = require('fs');
const path = require('path');

const CHROME = process.env.CHROME_PATH ||
  (fs.existsSync('/opt/pw-browsers')
    ? require('child_process').execSync(
        "ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1"
      ).toString().trim()
    : undefined);

const { chromium } = require('playwright-core');
const ROOT = process.env.SITE_ROOT || process.cwd();

// Skript nemá prepínače – cesty sú pevné (viď hlavička). Keby ich niekto predsa
// zadal, radšej to povedz, než potichu vyrenderovať niečo iné, než čakal.
if (process.argv.length > 2) {
  const a = process.argv.slice(2);
  if (a.includes('--help') || a.includes('-h')) {
    console.log('render_raster.js — bez prepínačov. Vstup: assets/img/og-image.svg a assets/favicon.svg\n' +
      'Koreň projektu sa dá zmeniť cez SITE_ROOT, cesta k prehliadaču cez CHROME_PATH.');
    process.exit(0);
  }
  console.error('⚠  render_raster.js nepozná prepínače (dostal: ' + a.join(' ') + ').\n' +
    '   Používa pevné cesty; koreň zmeníš cez SITE_ROOT=<cesta>. Pokračujem s predvolenými.');
}

async function svgToPng(browser, svgPath, outPath, w, h, transparent) {
  let svg = fs.readFileSync(svgPath, 'utf8').replace(/<svg /, `<svg width="${w}" height="${h}" `);
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  await page.setContent(
    `<!doctype html><html><head><style>*{margin:0;padding:0}html,body{width:${w}px;height:${h}px;overflow:hidden}</style></head><body>${svg}</body></html>`,
    { waitUntil: 'networkidle' });
  await page.screenshot({ path: outPath, clip: { x: 0, y: 0, width: w, height: h }, omitBackground: !!transparent });
  await page.close();
  console.log('  ✓', path.relative(ROOT, outPath), `${w}×${h}`);
}

(async () => {
  const b = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
  const P = (...p) => path.join(ROOT, ...p);

  const og = P('assets/img/og-image.svg');
  if (fs.existsSync(og)) {
    console.log('OG obrázok:');
    await svgToPng(b, og, P('assets/img/og-image.png'), 1200, 630, false);
  }
  const fav = P('assets/favicon.svg');
  if (fs.existsSync(fav)) {
    console.log('Favicony / ikony:');
    await svgToPng(b, fav, P('assets/favicon-32.png'), 32, 32, true);
    await svgToPng(b, fav, P('assets/apple-touch-icon.png'), 180, 180, true);
    await svgToPng(b, fav, P('assets/icon-192.png'), 192, 192, true);
    await svgToPng(b, fav, P('assets/icon-512.png'), 512, 512, true);
  }
  await b.close();
  console.log('done');
})().catch(e => { console.error(e); process.exit(1); });
