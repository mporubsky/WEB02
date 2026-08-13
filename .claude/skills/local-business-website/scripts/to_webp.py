#!/usr/bin/env python3
"""
to_webp.py — doplní k JPEG/PNG fotkám úspornú WebP verziu a obalí <img> do
<picture>, takže moderné prehliadače stiahnu WebP a staršie dostanú pôvodný
súbor. Reálna úspora býva 30–40 % objemu obrázkov.

Spúšťaj AŽ po `optimize_photos.py` (najprv sprav poriadok v rozmeroch a EXIF,
až potom kóduj) a vždy až vtedy, keď sú fotky finálne — WebP je odvodenina.

DÔLEŽITÉ: `<picture>` je v HTML nový obal okolo `<img>`, ktorý by mohol pokaziť
rozloženie (napr. `height:100%` obrázka by sa počítalo voči nemu). Preto do CSS
patrí `picture { display: contents; }` — v priloženom engine styles.css už je.

Použitie:
  # 1) vygenerovať .webp ku všetkým fotkám
  python to_webp.py --dir assets/img

  # 2) obaliť <img> v HTML do <picture> (idempotentné, dá sa spustiť opakovane)
  python to_webp.py --dir assets/img --wrap-html .

  # iná kvalita (default 80 – vizuálne nerozoznateľné od JPEG q82)
  python to_webp.py --dir assets/img --quality 85
"""
import os, re, glob, argparse, sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Chýba Pillow:  pip install pillow")

ap = argparse.ArgumentParser()
ap.add_argument("--dir", default="assets/img", help="priečinok s fotkami")
ap.add_argument("--quality", type=int, default=80)
ap.add_argument("--wrap-html", metavar="ROOT", help="obalí <img> v .html súboroch v tomto priečinku")
ap.add_argument("--ext", default="jpg,jpeg",
                help="PNG zámerne nie je v predvolenom nastavení – og-image.png a ikony\n"
                     "musia zostať raster PNG (siete WebP náhľady neberú).")
a = ap.parse_args()

exts = [e.strip().lstrip(".").lower() for e in a.ext.split(",")]
srcs = sorted(f for e in exts for f in glob.glob(os.path.join(a.dir, f"*.{e}")))
if not srcs:
    sys.exit(f"V {a.dir} som nenašiel obrázky ({a.ext}).")

src_tot = webp_tot = 0
made = 0
for f in srcs:
    out = os.path.splitext(f)[0] + ".webp"
    im = Image.open(f)
    # WebP nezvláda niektoré režimy (P s priehľadnosťou, CMYK) → zjednoť
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") and "transparency" in im.info else "RGB")
    im.save(out, "WEBP", quality=a.quality, method=6)
    src_tot += os.path.getsize(f); webp_tot += os.path.getsize(out); made += 1

saved = 100 * (src_tot - webp_tot) / src_tot if src_tot else 0
print(f"WebP: {made} súborov   {src_tot/1048576:.2f} MB → {webp_tot/1048576:.2f} MB   (úspora {saved:.0f} %)")

if not a.wrap_html:
    print("\nĎalší krok: python to_webp.py --dir %s --wrap-html ." % a.dir)
    sys.exit(0)

# --- obalenie <img> do <picture> -------------------------------------------
pat = re.compile(r'<img\b[^>]*?src="([^"]+\.(?:%s))"[^>]*>' % "|".join(exts), re.I | re.S)
total = 0
for page in sorted(glob.glob(os.path.join(a.wrap_html, "*.html"))):
    s = open(page, encoding="utf-8").read()
    orig = s

    def inside_picture(text, pos):
        """Je pozícia už vnútri <picture>…</picture>? (ochrana pred dvojitým obalením
        — pred <img> stojí <source>, takže samotný lookbehind na <picture> nestačí)"""
        before = text[:pos]
        return before.rfind("<picture>") > before.rfind("</picture>")

    def repl(m):
        tag, src = m.group(0), m.group(1)
        if inside_picture(s, m.start()):
            return tag                      # už obalené skorším behom
        webp = os.path.splitext(src)[0] + ".webp"
        if not os.path.exists(os.path.join(a.wrap_html, webp)):
            return tag                      # nemá WebP náprotivok → nechaj tak
        return f'<picture><source srcset="{webp}" type="image/webp">{tag}</picture>'

    s = pat.sub(repl, s)
    n = s.count("<picture>") - orig.count("<picture>")
    if s != orig:
        open(page, "w", encoding="utf-8").write(s)
        total += n
        print(f"  {os.path.basename(page)}: obalených {n}")

print(f"Obalených <img> spolu: {total}")
print("\nSkontroluj, že v css/styles.css je:  picture { display: contents; }")
