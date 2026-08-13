#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kontrola webu BABYLAND — pravidlá, ktoré platia práve pre tento web.

Spustenie (z koreňa projektu, nič netreba inštalovať):

    python3 scripts/kontrola.py

Skript nič nemení, len vypíše, čo našiel, a skončí s kódom 1, ak našiel chybu.
Doplňuje skripty zo `.claude/skills/local-business-website/scripts/`, ktoré
kontrolujú všeobecné veci (odkazy, kontrast, dotykové plochy). Tento skript
stráži to, čo je vlastné tomuto projektu:

  1. slovenská typografia — pomlčka „–" namiesto „—" a nezalomiteľná medzera
     po jednopísmenových predložkách; anglické stránky sa nekontrolujú, tam
     platia iné pravidlá
  2. poradie nadpisov — nesmie preskočiť stupeň (h1 → h3), inak sa v čítačke
     obrazovky stratí štruktúra stránky
  3. dvakrát ten istý odsek na jednej stránke
  4. selektory v CSS, na ktoré v HTML nič nesedí
  5. názov živnosti („opatrovateľské centrum") mimo fakturačných údajov —
     prevádzka je súkromná materská škola
  6. obrázky bez alt, width alebo height
"""
import collections
import html as htmlmod
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SK_PAGES = sorted(ROOT.glob("*.html"))
EN_PAGES = sorted(ROOT.glob("en/*.html"))
ALL_PAGES = SK_PAGES + EN_PAGES

# jednopísmenové predložky a spojky, po ktorých nesmie riadok zalomiť
SK_ONE_LETTER = "aiouvszkAIOUVSZK"

# názov živnosti smie byť len tam, kde ide o fakturačné údaje alebo copyright
LEGAL_NAME_ALLOWED = ("business.name", "legalName")

errors = []
warnings = []


def page_text(path):
    """Vráti viditeľný text stránky bez značiek, skriptov a obrázkov SVG.

    :param path: cesta k HTML súboru
    :returns:    text tak, ako ho zhruba vidí návštevník
    """
    source = path.read_text(encoding="utf-8")
    body = source.split("<body", 1)[-1]
    body = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", body, flags=re.S)
    return htmlmod.unescape(re.sub(r"<[^>]+>", " ", body))


def check_sk_typography():
    """1. Slovenská typografia na slovenských stránkach."""
    for path in SK_PAGES:
        source = path.read_text(encoding="utf-8")
        name = path.name

        if "—" in source:
            errors.append(f"{name}: dlhá pomlčka U+2014 – v slovenčine patrí pomlčka U+2013")

        text = page_text(path)
        dangling = re.findall(r"(?:^|[\s(„])([" + SK_ONE_LETTER + r"]) [^\s]", text)
        if dangling:
            warnings.append(
                f"{name}: {len(dangling)}x jednopísmenové slovo bez nezalomiteľnej "
                f"medzery (napr. {dangling[0]} ...) – použite &nbsp;"
            )


def check_heading_order():
    """2. Nadpisy nesmú preskakovať stupne."""
    for path in ALL_PAGES:
        body = path.read_text(encoding="utf-8").split("<body", 1)[-1]
        levels = [int(m.group(1)) for m in re.finditer(r"<h([1-6])[\s>]", body)]
        if levels.count(1) != 1:
            errors.append(f"{path.name}: {levels.count(1)}x <h1>, má byť práve jeden")
        previous = 0
        for level in levels:
            if previous and level > previous + 1:
                errors.append(f"{path.name}: preskočený nadpis h{previous} → h{level}")
            previous = level


def check_duplicate_paragraphs():
    """3. Ten istý odstavec dvakrát na jednej stránke."""
    for path in ALL_PAGES:
        body = path.read_text(encoding="utf-8").split("<body", 1)[-1]
        body = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", body, flags=re.S)
        paragraphs = [
            re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", "", m))).strip()
            for m in re.findall(r"<p\b[^>]*>(.*?)</p>", body, re.S)
        ]
        # krátke odstavce (adresa, telefón) sa opakujú zámerne
        for text, count in collections.Counter(p for p in paragraphs if len(p) > 60).items():
            if count > 1:
                errors.append(f"{path.name}: rovnaký odstavec {count}x: {text[:60]}...")


def check_unused_css():
    """4. Selektory v CSS, ktoré v HTML nemajú na čo sadnúť."""
    used_classes, used_ids = set(), set()
    for path in ALL_PAGES:
        source = path.read_text(encoding="utf-8")
        for m in re.finditer(r'class="([^"]*)"', source):
            used_classes.update(m.group(1).split())
        for m in re.finditer(r'id="([^"]*)"', source):
            used_ids.add(m.group(1))

    # triedy, ktoré pridáva až JavaScript
    script = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
    used_classes.update(re.findall(r'["\']([a-z][a-z-]*)["\']', script))

    css = re.sub(r"/\*.*?\*/", "", (ROOT / "css" / "styles.css").read_text(encoding="utf-8"), flags=re.S)
    for block in re.finditer(r"([^{}]+)\{[^{}]*\}", css):
        group = block.group(1).strip()
        if group.startswith("@") or not group:
            continue
        for selector in group.split(","):
            missing = [f".{c}" for c in re.findall(r"\.([A-Za-z0-9_-]+)", selector)
                       if c not in used_classes]
            missing += [f"#{i}" for i in re.findall(r"#([A-Za-z0-9_-]+)", selector)
                        if i not in used_ids]
            if missing:
                warnings.append(f"styles.css: {selector.strip()} – v HTML niet "
                                f"{', '.join(sorted(set(missing)))}")


def check_identity():
    """5. Názov živnosti mimo fakturačných údajov a copyrightu."""
    for path in ALL_PAGES:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "opatrovateľsk" not in line.lower():
                continue
            if any(marker in line for marker in LEGAL_NAME_ALLOWED):
                continue
            errors.append(
                f"{path.name}:{line_no}: nazov zivnosti mimo fakturacnych udajov "
                f"– prevadzka je sukromna materska skola"
            )


def check_images():
    """6. Obrázky musia mať alt aj rozmery, inak stránka pri načítaní skáče."""
    for path in ALL_PAGES:
        for tag in re.findall(r"<img\b[^>]*>", path.read_text(encoding="utf-8")):
            src = re.search(r'src="([^"]+)"', tag)
            src = src.group(1) if src else "?"
            if "alt=" not in tag:
                errors.append(f"{path.name}: <img> bez alt: {src}")
            if "width=" not in tag or "height=" not in tag:
                errors.append(f"{path.name}: <img> bez width/height: {src}")


def main():
    check_sk_typography()
    check_heading_order()
    check_duplicate_paragraphs()
    check_unused_css()
    check_identity()
    check_images()

    line = "=" * 72
    print(line)
    if errors:
        print(f"\n### CHYBY ({len(errors)})\n")
        for item in errors:
            print("  -", item)
    if warnings:
        print(f"\n### UPOZORNENIA ({len(warnings)})\n")
        for item in warnings:
            print("  -", item)
    print("\n" + line)
    if errors:
        print(f"❌ {len(errors)} chýb na opravu.  ({len(warnings)} upozornení)")
        return 1
    print(f"✅ Bez chýb.  ({len(warnings)} upozornení)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
