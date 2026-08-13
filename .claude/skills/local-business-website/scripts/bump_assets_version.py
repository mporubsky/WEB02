#!/usr/bin/env python3
"""
bump_assets_version.py — zosúladí `?v=` pri odkazoch na CSS/JS a značkové
obrázky (SVG/PNG v assets/) s ich obsahom.

Prečo to existuje: prehliadače a hostingy držia JS/CSS v cache celé dni. Keď
upravíš `config.js` alebo `styles.css` a zabudneš zvýšiť verziu, používateľ
dostane NOVÉ HTML so STARÝM štýlom či starými údajmi — stránka sa rozsype alebo
ukazuje staré telefónne číslo. „Nezabudni zvýšiť verziu" ako pravidlo nestačí;
tento skript to spraví za teba.

Značkové obrázky sem patria rovnako ako CSS: logo a favicona sa pri prefarbení
menia, ale názov súboru ostáva — a hostingy im dávajú `Cache-Control` na rok.
Bez `?v=` by vracajúci sa návštevník videl staré logo prakticky navždy.
Fotografie (.jpg) sa neverzujú: nové fotky dostávajú nové názvy.

Verzia je krátky hash obsahu všetkých týchto súborov, takže sa zmení
práve vtedy, keď sa niečo naozaj zmenilo — a pri opakovanom behu bez zmien
neurobí nič.

Použitie:
  python bump_assets_version.py [--root .] [--check]
  --check : nič nezapíše, len oznámi, či je verzia zastaraná (návratový kód 1)

Zaraď to do postupu pred každým pushom, ktorý sa dotkol css/, js/ alebo assets/.
"""
import re, os, sys, glob, hashlib, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=".")
ap.add_argument("--check", action="store_true", help="len skontroluj, nezapisuj")
a = ap.parse_args()
os.chdir(a.root)

assets = sorted(
    glob.glob("css/*.css") + glob.glob("js/*.js")
    + glob.glob("assets/**/*.svg", recursive=True)
    + glob.glob("assets/**/*.png", recursive=True)
)
if not assets:
    sys.exit("Nenašiel som css/*.css ani js/*.js — si v koreni projektu?")

h = hashlib.sha256()
for f in assets:
    h.update(f.encode())
    h.update(open(f, "rb").read())
ver = h.hexdigest()[:8]

def _find_pages():
    """Všetky .html v projekte vrátane podadresárov (napr. jazykové mutácie /en/).
    Vynecháva skryté adresáre a priečinky nástrojov."""
    SKIP = {"node_modules", "_verify_shots", "screenshots", "__pycache__"}
    out = []
    for dirpath, dirnames, filenames in os.walk("."):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in SKIP]
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, fn), "."))
    return sorted(out)

pages = _find_pages()
if not pages:
    sys.exit("Nenašiel som .html súbory.")

# odkazy, ktoré verzujeme: css, js a značkové obrázky (nie fotky .jpg)
REF = r'((?:href|src)=")((?:\.\./)*(?:css|js|assets)/[^"?]+\.(?:css|js|svg|png))(\?v=[^"]*)?(")'

# nájdi verzie, ktoré sú v HTML teraz
sucasne = set()
for p in pages:
    for m in re.finditer(REF, open(p, encoding="utf-8").read()):
        sucasne.add(m.group(3)[3:] if m.group(3) else "")

if sucasne == {ver}:
    print(f"✅ Verzia je aktuálna (?v={ver}) — netreba nič meniť.")
    sys.exit(0)

print(f"Obsah CSS/JS zodpovedá verzii ?v={ver}; v HTML je: {', '.join(sorted(sucasne)) or '(žiadna)'}")
if a.check:
    print("❌ Verzia je zastaraná — spusti skript bez --check.")
    sys.exit(1)

zmenene = 0
for p in pages:
    s = open(p, encoding="utf-8").read()
    o = s
    # jedným prechodom: verzované prepíš, neverzované doplň
    s = re.sub(REF, rf'\1\2?v={ver}\4', s)
    if s != o:
        open(p, "w", encoding="utf-8").write(s)
        zmenene += 1

print(f"✅ Verzia nastavená na ?v={ver} v {zmenene} stránkach.")
