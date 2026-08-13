#!/usr/bin/env python3
"""
bump_assets_version.py — zosúladí `?v=` pri odkazoch na CSS/JS s ich obsahom.

Prečo to existuje: prehliadače a hostingy držia JS/CSS v cache celé dni. Keď
upravíš `config.js` alebo `styles.css` a zabudneš zvýšiť verziu, používateľ
dostane NOVÉ HTML so STARÝM štýlom či starými údajmi — stránka sa rozsype alebo
ukazuje staré telefónne číslo. „Nezabudni zvýšiť verziu" ako pravidlo nestačí;
tento skript to spraví za teba.

Verzia je krátky hash obsahu všetkých lokálnych CSS/JS súborov, takže sa zmení
práve vtedy, keď sa niečo naozaj zmenilo — a pri opakovanom behu bez zmien
neurobí nič.

Použitie:
  python bump_assets_version.py [--root .] [--check]
  --check : nič nezapíše, len oznámi, či je verzia zastaraná (návratový kód 1)

Zaraď to do postupu pred každým pushom, ktorý sa dotkol css/ alebo js/.
"""
import re, os, sys, glob, hashlib, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=".")
ap.add_argument("--check", action="store_true", help="len skontroluj, nezapisuj")
a = ap.parse_args()
os.chdir(a.root)

assets = sorted(glob.glob("css/*.css") + glob.glob("js/*.js"))
if not assets:
    sys.exit("Nenašiel som css/*.css ani js/*.js — si v koreni projektu?")

h = hashlib.sha256()
for f in assets:
    h.update(f.encode())
    h.update(open(f, "rb").read())
ver = h.hexdigest()[:8]

pages = sorted(glob.glob("*.html"))
if not pages:
    sys.exit("Nenašiel som .html súbory.")

# nájdi verzie, ktoré sú v HTML teraz
sucasne = set()
for p in pages:
    sucasne |= set(re.findall(r'(?:css|js)/[^"?]+\?v=([^"]*)', open(p, encoding="utf-8").read()))

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
    # už verzované odkazy prepíš
    s = re.sub(r'((?:css|js)/[^"?]+)\?v=[^"]*', rf'\1?v={ver}', s)
    # neverzované doplň
    s = re.sub(r'((?:href|src)=")((?:css|js)/[^"?]+)(")', rf'\1\2?v={ver}\3', s)
    if s != o:
        open(p, "w", encoding="utf-8").write(s)
        zmenene += 1

print(f"✅ Verzia nastavená na ?v={ver} v {zmenene} stránkach.")
