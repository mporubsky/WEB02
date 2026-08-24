#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepíše sitemap.xml — zoznam stránok pre vyhľadávače.

Spustenie (z koreňa projektu):

    python3 scripts/aktualizuj_sitemap.py

Dátum poslednej zmeny (`lastmod`) sa berie z histórie repozitára, nie ručne —
ručne písaný dátum si nikto nepamätá prepísať a Google potom dostáva nepravdivý
údaj o tom, kedy sa stránka menila.

**Po pridaní novej stránky** doplňte riadok do zoznamu PAGES nižšie a skript
spustite. Priorita hovorí vyhľadávaču, ktoré stránky sú dôležitejšie: 1.0 je
úvod, 0.4 najmenej dôležitá stránka. Sú to len relatívne váhy v rámci tohto
webu, nie hodnotenie voči iným webom.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://www.babyland-centrum.sk/"

# (súbor, priorita) — poradie sa zachová vo výslednom súbore
PAGES = [
    ("index.html", "1.0"),
    ("ponuka.html", "0.9"),
    ("kurzy.html", "0.9"),
    ("filozofia.html", "0.8"),
    ("kontakt.html", "0.8"),
    ("na-navsteve.html", "0.7"),
    ("en/index.html", "0.6"),
    ("en/offer.html", "0.6"),
    ("en/courses.html", "0.6"),
    ("en/philosophy.html", "0.5"),
    ("en/contact.html", "0.5"),
    ("en/visit.html", "0.4"),
]

# 404 do mapy stránok nepatrí — nemá sa indexovať


def last_modified(name):
    """Vráti dátum poslednej zmeny súboru podľa histórie repozitára.

    :param name: cesta od koreňa webu, napr. "ponuka.html"
    :returns:    dátum ako "2026-08-14"; keď súbor ešte nie je v histórii,
                 vráti dnešný dátum
    """
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ad", "--date=short", "--", name],
        cwd=ROOT, capture_output=True, text=True,
    )
    date = result.stdout.strip()
    if date:
        return date
    return subprocess.run(["date", "+%F"], capture_output=True, text=True).stdout.strip()


def main():
    missing = [name for name, _ in PAGES if not (ROOT / name).exists()]
    if missing:
        print("Tieto stránky zo zoznamu PAGES neexistujú: " + ", ".join(missing))
        return 1

    rows = []
    for name, priority in PAGES:
        date = last_modified(name)
        loc = DOMAIN + ("" if name == "index.html" else name)
        rows.append(
            f"  <url>\n"
            f"    <loc>{loc}</loc>\n"
            f"    <lastmod>{date}</lastmod>\n"
            f"    <priority>{priority}</priority>\n"
            f"  </url>"
        )
        print(f"  {name:<20} {date}")

    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<!-- Zoznam stránok pre vyhľadávače. Negenerujte ho ručne —\n"
        "     spustite: python3 scripts/aktualizuj_sitemap.py -->\n"
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n",
        encoding="utf-8",
    )
    print(f"\n✅ sitemap.xml prepísaný — {len(PAGES)} stránok.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
