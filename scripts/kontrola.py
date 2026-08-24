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
  7. hlavička a pätička sa medzi stránkami rozišli — sú v každom súbore
     zvlášť, takže úprava na jednom mieste sa ľahko zabudne inde
  8. ručne písané údaje (blok pre Google, hodiny na anglických stránkach)
     sa rozišli s js/config.js
  9. rozbitý komentár v CSS — prehliadač po ňom ticho zahodí celé pravidlo
     a v prehliadači to vyzerá, akoby ste ho nikdy nenapísali
"""
import collections
import html as htmlmod
import json
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


def page_text(path, skip_lang=None):
    """Vráti viditeľný text stránky bez značiek, skriptov a obrázkov SVG.

    :param path:      cesta k HTML súboru
    :param skip_lang: keď je zadaný (napr. "en"), vynechá text v prvkoch
                      označených týmto jazykom — v pätičke slovenských
                      stránok sú odkazy na anglické stránky a tie sa podľa
                      slovenských pravidiel posudzovať nemajú
    :returns:         text tak, ako ho zhruba vidí návštevník
    """
    source = path.read_text(encoding="utf-8")
    body = source.split("<body", 1)[-1]
    body = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", body, flags=re.S)
    if skip_lang:
        body = re.sub(r'<([a-z]+)[^>]*\blang="' + skip_lang + r'"[^>]*>.*?</\1>',
                      " ", body, flags=re.S)
    return htmlmod.unescape(re.sub(r"<[^>]+>", " ", body))


def check_sk_typography():
    """1. Slovenská typografia na slovenských stránkach."""
    for path in SK_PAGES:
        source = path.read_text(encoding="utf-8")
        name = path.name

        if "—" in source:
            errors.append(f"{name}: dlhá pomlčka U+2014 – v slovenčine patrí pomlčka U+2013")

        text = page_text(path, skip_lang="en")
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


def read_config():
    """Vytiahne zo js/config.js hodnoty, ktoré sa dajú porovnať inde na webe.

    config.js je JavaScript, nie JSON, takže sa nedá načítať priamo. Berú sa
    len jednoduché reťazcové hodnoty; zložitejšie by sa museli vyhodnotiť.

    :returns: slovník, napr. {"phone": "0908 41 40 91", "hours": "7:30 - 17:30"}
    """
    source = (ROOT / "js" / "config.js").read_text(encoding="utf-8")
    values = {}
    for key in ("phone", "phoneHref", "email"):
        m = re.search(key + r'\s*:\s*"([^"]*)"', source)
        if m:
            values[key] = m.group(1)
    m = re.search(r'showroom\s*:\s*\{[^}]*?full\s*:\s*"([^"]*)"', source, re.S)
    if m:
        values["showroom"] = m.group(1)
    m = re.search(r'hours\s*:\s*\[\s*\{[^}]*?h\s*:\s*"([^"]*)"', source, re.S)
    if m:
        values["hours"] = m.group(1)
    return values


def normalize_block(html, is_en):
    """Zjednotí hlavičku alebo pätičku, aby sa dali porovnať medzi stránkami.

    Odstráni to, čo sa medzi stránkami líšiť SMIE: značku aktuálnej položky
    menu, verziu súborov ?v=... a predponu ../ na anglických stránkach.

    :param html:  blok HTML
    :param is_en: či ide o stránku v priečinku en/
    :returns:     text vhodný na porovnanie
    """
    html = re.sub(r'\s*aria-current="page"', "", html)
    html = re.sub(r"\?v=[0-9a-f]+", "", html)
    if is_en:
        html = html.replace('"../', '"')
    return re.sub(r"\s+", " ", html).strip()


def check_shared_blocks():
    """7. Hlavička a pätička sú v každom súbore zvlášť - nesmú sa rozísť."""
    blocks = (("hlavicka", r'<header class="site-header">.*?</header>'),
              ("paticka", r'<footer class="site-footer">.*?</footer>'))
    groups = (("slovenskych", SK_PAGES, False), ("anglickych", EN_PAGES, True))
    for label, pattern in blocks:
        for group_label, pages, is_en in groups:
            variants = {}
            for path in pages:
                m = re.search(pattern, path.read_text(encoding="utf-8"), re.S)
                if not m:
                    errors.append(f"{path.name}: chyba {label}")
                    continue
                variants.setdefault(normalize_block(m.group(0), is_en), []).append(path.name)
            if len(variants) > 1:
                ordered = sorted(variants.values(), key=len, reverse=True)
                odd = ", ".join(name for group in ordered[1:] for name in group)
                errors.append(f"{label} sa medzi {group_label} strankami lisi - "
                              f"odlisne su: {odd} (zhodnych: {len(ordered[0])})")


def check_data_in_sync():
    """8. Ručne písané údaje sa nesmú rozísť s js/config.js."""
    cfg = read_config()
    if not cfg:
        errors.append("js/config.js sa nepodarilo precitat")
        return

    # Blok pre Google je na kazdej stranke, ktora skolku predstavuje. Kontroluju
    # sa VSETKY najdene bloky, nielen ten na uvodnej stranke — inak by sa druhy
    # blok mohol rozist s config.js a nikto by sa to nedozvedel.
    JSONLD_PAGES = ["index.html", "kontakt.html", "en/index.html", "en/contact.html"]
    for name in JSONLD_PAGES:
        page = ROOT / name
        if not page.exists():
            errors.append(f"{name}: subor chyba")
            continue
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>',
                      page.read_text(encoding="utf-8"), re.S)
        if not m:
            errors.append(f"{name}: chyba blok application/ld+json pre Google")
            continue
        block = m.group(1)
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{name}: JSON-LD sa neda precitat ({exc})")
            continue
        for key, want in (("telephone", cfg.get("phoneHref")), ("email", cfg.get("email"))):
            found = re.search(r'"' + key + r'"\s*:\s*"([^"]*)"', block)
            if want and found and found.group(1) != want:
                errors.append(f"{name}: JSON-LD {key} je {found.group(1)}, "
                              f"config.js ma {want}")
        street = cfg.get("showroom", "").split(",")[0].strip()
        if street and street not in block:
            errors.append(f"{name}: JSON-LD nema adresu z config.js ({street})")
        for t in re.findall(r"\d{1,2}:\d{2}", cfg.get("hours", "")):
            if t not in block:
                errors.append(f"{name}: JSON-LD nema cas {t} z config.js")

    for path in EN_PAGES:
        source = path.read_text(encoding="utf-8")
        if "hours-row" not in source:
            continue
        for t in re.findall(r"\d{1,2}:\d{2}", cfg.get("hours", "")):
            if t not in source:
                errors.append(f"{path.name}: rucne pisane hodiny nemaju {t} z config.js")


def check_css_comments():
    """9. Komentáre v CSS musia byť správne uzavreté.

    Keď sa pri úprave komentára stratí alebo zdvojí ``*/``, prehliadač berie
    text komentára ako CSS, narazí na chybu a **zahodí celé nasledujúce
    pravidlo**. Nič sa nezobrazí ako chyba — pravidlo sa jednoducho neuplatní.
    Presne takto raz zmizlo celé ``.brand__tag``.
    """
    css = (ROOT / "css" / "styles.css").read_text(encoding="utf-8")

    opened, closed = css.count("/*"), css.count("*/")
    if opened != closed:
        errors.append(f"styles.css: {opened}x /* ale {closed}x */ - "
                      f"niektory komentar nie je uzavrety")
        return

    # text mimo komentárov, ktorý nezačína ako selektor, deklarácia ani @pravidlo
    outside = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for number, line in enumerate(outside.splitlines(), 1):
        text = line.strip()
        if not text or text in ("{", "}"):
            continue
        if not re.match(r"^[@.#:*\[a-zA-Z0-9>~+&\"'-]", text):
            errors.append(f"styles.css: mimo komentara je text, ktory nie je CSS - "
                          f"{text[:60]}")


def main():
    check_sk_typography()
    check_heading_order()
    check_duplicate_paragraphs()
    check_unused_css()
    check_identity()
    check_images()
    check_shared_blocks()
    check_data_in_sync()
    check_css_comments()

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
