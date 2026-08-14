#!/usr/bin/env node
/**
 * Záťažový test rozloženia webu BABYLAND.
 *
 * Spustenie (z koreňa projektu):
 *
 *     node scripts/stress_test.js
 *
 * Potrebuje Node.js, balík `playwright-core` a Chromium. Server si spúšťa sám,
 * netreba nič naštartovať dopredu.
 *
 * Doplňuje `audit_browser.js`, ktorý kontroluje stránku tak, ako vyzerá.
 * Tento skript ju skúša ROZBIŤ — každý z troch scenárov nižšie odhalil na tomto
 * webe skutočnú chybu v čase, keď všetky ostatné kontroly hlásili zelenú:
 *
 *   1. bežné zobrazenie — pretečenie do šírky na úzkych displejoch
 *   2. zväčšené rozostupy textu podľa WCAG 1.4.12 (návštevník si ich môže
 *      zapnúť v prehliadači) — tu pretiekol zoznam na stránke Ponuka
 *   3. dlhé nezalomiteľné slovo v nadpise — napodobňuje dlhú e-mailovú adresu
 *      alebo zložené slovo; tu pretiekla chybová stránka 404
 *
 * Navyše overuje, že sa pri otvorenom mobilnom menu nedá tabulátorom prejsť
 * za prekryv na skryté odkazy.
 *
 * Vypíše nájdené problémy a skončí s kódom 1, ak niečo našiel.
 */
const { chromium } = require("playwright-core");
const http = require("http");
const fs = require("fs");
const path = require("path");
const url = require("url");

// Cesta k prehliadaču: Playwright ho hľadá na mieste, kde ho sám stiahol.
// V prostredí, kde je Chromium predinštalované, treba cestu podať ručne —
// prázdna hodnota znamená „nech si ho Playwright nájde sám".
const CHROME = require("child_process")
  .execSync("ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1")
  .toString().trim();

const ROOT = path.resolve(__dirname, "..");
const PORT = 8123;
const WIDTHS = [320, 360, 375, 390, 412, 768];

const PAGES = [
  "index.html", "ponuka.html", "kurzy.html", "filozofia.html",
  "na-navsteve.html", "kontakt.html", "404.html",
  "en/index.html", "en/program.html", "en/exclusive.html", "en/contact.html",
];

const SCENARIOS = [
  { name: "bežné zobrazenie", css: "" },
  {
    name: "WCAG 1.4.12 zväčšené rozostupy textu",
    css: "*{line-height:1.5em!important;letter-spacing:.12em!important;" +
         "word-spacing:.16em!important}p{margin-bottom:2em!important}",
  },
  { name: "dlhé nezalomiteľné slovo", css: "", injectLongWord: true },
];

const MIME = {
  ".html": "text/html", ".css": "text/css", ".js": "text/javascript",
  ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
  ".webmanifest": "application/manifest+json", ".xml": "application/xml",
};

/** Spustí jednoduchý statický server nad priečinkom projektu. */
function startServer() {
  const server = http.createServer((req, res) => {
    let p = decodeURIComponent(url.parse(req.url).pathname);
    if (p === "/") p = "/index.html";
    const file = path.join(ROOT, p);
    if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
      res.writeHead(404);
      return res.end("404");
    }
    res.writeHead(200, { "Content-Type": MIME[path.extname(file)] || "application/octet-stream" });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise((resolve) => server.listen(PORT, () => resolve(server)));
}

(async () => {
  const server = await startServer();
  const browser = await chromium.launch(CHROME ? { executablePath: CHROME } : {});
  const problems = [];

  // ── 1-3. pretečenie do šírky v troch scenároch ─────────────────────────
  for (const scenario of SCENARIOS) {
    for (const width of WIDTHS) {
      const context = await browser.newContext({
        viewport: { width, height: 720 }, isMobile: width < 700, hasTouch: width < 700,
      });
      const page = await context.newPage();

      for (const file of PAGES) {
        await page.goto(`http://localhost:${PORT}/${file}`, { waitUntil: "networkidle" });
        if (scenario.css) await page.addStyleTag({ content: scenario.css });
        if (scenario.injectLongWord) {
          await page.evaluate(() => {
            const h = document.querySelector("h1");
            if (h) h.textContent = "Neprekonatelnorozsirujucaznacka " + h.textContent;
          });
        }
        await page.waitForTimeout(120);

        const found = await page.evaluate((vw) => {
          const out = [];
          if (document.documentElement.scrollWidth <= vw + 1) return out;
          document.querySelectorAll("body *").forEach((el) => {
            const box = el.getBoundingClientRect();
            if (box.width === 0 || box.right <= vw + 1) return;
            // prvok vo vodorovne posúvateľnom kontajneri je v poriadku
            for (let p = el.parentElement; p; p = p.parentElement) {
              if (/auto|scroll/.test(getComputedStyle(p).overflowX)) return;
            }
            out.push(`${el.tagName.toLowerCase()}.${(el.className || "").toString().split(" ")[0]}` +
                     ` presahuje o ${Math.round(box.right - vw)}px`);
          });
          return out.length ? out : [`dokument má ${document.documentElement.scrollWidth}px`];
        }, width);

        if (found.length) {
          problems.push(`[${scenario.name} @ ${width}px] ${file}: ` +
                        [...new Set(found)].slice(0, 3).join(" | "));
        }
      }
      await context.close();
    }
  }

  // ── 4. zameranie nesmie utiecť za otvorené mobilné menu ────────────────
  {
    const context = await browser.newContext({
      viewport: { width: 390, height: 800 }, isMobile: true, hasTouch: true,
    });
    const page = await context.newPage();
    await page.goto(`http://localhost:${PORT}/index.html`, { waitUntil: "networkidle" });
    await page.click(".nav-toggle");
    await page.waitForTimeout(350);

    for (let i = 0; i < 10; i++) {
      await page.keyboard.press("Tab");
      const escaped = await page.evaluate(() => {
        const el = document.activeElement;
        // <body> znamená „nič nie je zamerané" — prehliadač takto prechádza
        // cez svoju vlastnú lištu s adresou. To nie je únik za menu.
        if (!el || el === document.body || el === document.documentElement) return false;
        return !el.closest("#main-nav") && !el.closest(".site-header");
      });
      if (escaped) {
        const what = await page.evaluate(() =>
          (document.activeElement.textContent || document.activeElement.tagName).trim().slice(0, 40));
        problems.push(`[zameranie] pri otvorenom menu Tab č. ${i + 1} skočil mimo menu ` +
                      `a hlavičku, na „${what}" — pozadie nie je inert`);
        break;
      }
    }
    await context.close();
  }

  await browser.close();
  server.close();

  console.log("=".repeat(72));
  if (problems.length) {
    console.log(`\n### NÁJDENÉ PROBLÉMY (${problems.length})\n`);
    problems.forEach((p) => console.log("  - " + p));
    console.log("\n" + "=".repeat(72));
    console.log(`❌ ${problems.length} problémov.`);
    process.exit(1);
  }
  console.log(`\n✅ Bez problémov — ${SCENARIOS.length} scenáre × ${WIDTHS.length} šírok ` +
              `× ${PAGES.length} stránok, plus zameranie v mobilnom menu.`);
})();
