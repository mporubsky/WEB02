#!/usr/bin/env python3
"""
audit_html.py — statický audit hotového webu pred odovzdaním.

Dopĺňa verify_site.js (ten kontroluje beh v prehliadači). Tento skript číta
zdrojové HTML a hľadá chyby, ktoré sa v prehliadači nemusia prejaviť:

  ERROR (treba opraviť):
    - duplicitné id na stránke
    - data-mh / data-mh-href cesty, ktoré v config.js neexistujú (nenaplní sa!)
    - odkazy na neexistujúce súbory, stránky a kotvy (#sekcia)
    - <img> bez alt
    - iný počet <h1> ako 1
    - target="_blank" bez rel="noopener"
    - nesúlad počtu otváracích a zatváracích tagov
    - ZÁSTUPNÉ TEXTY viditeľné návštevníkovi (XX €, TODO, lorem, odkaz na README)

  WARN (skontrolovať):
    - chýbajúce SEO/OG meta, canonical, lang, theme-color
    - príliš dlhý title / meta description
    - <img> bez width/height (spôsobuje poskakovanie rozloženia)
    - CSS/JS bez ?v= verzie (cache-busting)
    - chýbajúca cookie lišta
    - telefón / e-mail v JSON-LD nesedí s config.js (JSON-LD je statický,
      main.js ho neplní – po doplnení údajov ostane v štruktúrovaných dátach starý)

Vedomé false-positives: `data-mh-href="..."` sa tvári ako href — skript ho
vylučuje. Stránka 404 nepotrebuje canonical/OG (je noindex).

Použitie:
  python audit_html.py [--root .] [--config js/config.js] [--strict]
  --strict : návratový kód != 0 aj pri WARN (inak len pri ERROR)
"""
import re, os, sys, glob, argparse
from collections import Counter, defaultdict

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=".")
ap.add_argument("--config", default="js/config.js")
ap.add_argument("--strict", action="store_true")
a = ap.parse_args()
os.chdir(a.root)

issues = defaultdict(list)
add = lambda sev, f, m: issues[sev].append((f, m))

cfg = open(a.config, encoding="utf-8").read() if os.path.exists(a.config) else ""
if not cfg:
    print(f"⚠  {a.config} sa nenašiel – kontrola data-mh ciest sa preskočí.")


def cfg_has(path):
    """Overí, že vnorená cesta (business.address.full) existuje v config.js."""
    seg = cfg
    for k in path.split("."):
        m = re.search(r"\b" + re.escape(k) + r"\s*:", seg)
        if not m:
            return False
        seg = seg[m.end():]
    return True


# zástupné texty, ktoré sa NIKDY nesmú dostať k návštevníkovi
PLACEHOLDER = re.compile(
    r"(od\s+XX\s*€|XX\s*€|\bTODO\b|\blorem ipsum\b|README\.md|"
    r"vzorová šablóna|zástupn[éý] \(placeholder\)|\{\{[A-Z_]+\}\}|"
    # „x-kové" výplne v e-mailoch a doménach (info@xxxx.sk) – tvária sa ako
    # platný údaj, prejdú kontrolou odkazov aj mailto, ale zákazník ich vidí
    r"[\w.+-]+@[\w.-]*x{3,}|\bx{3,}\.(?:sk|cz|com|eu)\b|"
    # zástupné telefónne číslo typu „+421 9XX XXX XXX"
    r"X{2,}\s+X{3,})", re.I)

pages = sorted(glob.glob("*.html"))
if not pages:
    sys.exit("Nenašiel som žiadne .html súbory v " + os.getcwd())

for p in pages:
    s = open(p, encoding="utf-8").read()
    is404 = p == "404.html"

    for i, c in Counter(re.findall(r'\sid="([^"]+)"', s)).items():
        if c > 1:
            add("ERROR", p, f'duplicitné id="{i}" ({c}×)')

    for attr in ("data-mh", "data-mh-href"):
        for path in sorted(set(re.findall(attr + r'="([^"]+)"', s))):
            if cfg and not cfg_has(path):
                add("ERROR", p, f'{attr}="{path}" neexistuje v config.js – nenaplní sa')

    # lokálne súbory; `data-mh-href="cesta.v.configu"` nie je súborový odkaz
    for m in re.finditer(r'(?<!-mh-)(?:src|href)="(?!https?:|mailto:|tel:|#|data:)([^"]+)"', s):
        ref = m.group(1).split("?")[0].split("#")[0]
        if ref and not os.path.exists(ref):
            add("ERROR", p, f"odkaz na neexistujúci súbor: {ref}")

    for m in re.finditer(r'href="([a-z0-9\-]+\.html)(#[^"]*)?"', s):
        tgt = m.group(1)
        if not os.path.exists(tgt):
            add("ERROR", p, f"odkaz na neexistujúcu stránku {tgt}")
        elif m.group(2):
            anchor = m.group(2)[1:]
            if f'id="{anchor}"' not in open(tgt, encoding="utf-8").read():
                add("ERROR", p, f"kotva {tgt}{m.group(2)} neexistuje")

    for m in re.finditer(r'href="#([^"]+)"', s):
        if m.group(1) and f'id="{m.group(1)}"' not in s:
            add("ERROR", p, f"kotva #{m.group(1)} na stránke neexistuje")

    for m in re.finditer(r"<img\b[^>]*>", s):
        t = m.group(0)
        if "alt=" not in t:
            add("ERROR", p, "<img> bez alt: " + t[:80])
        if "width=" not in t or "height=" not in t:
            add("WARN", p, "<img> bez width/height (poskakovanie rozloženia): " + t[:80])

    for m in re.finditer(r"<a\b[^>]*target=\"_blank\"[^>]*>", s):
        if "noopener" not in m.group(0):
            add("ERROR", p, 'target="_blank" bez rel="noopener": ' + m.group(0)[:70])

    # zástupné texty len vo viditeľnom texte (nie v placeholder="" polí formulára)
    visible = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", s))
    for m in set(PLACEHOLDER.findall(visible)):
        add("ERROR", p, f"ZÁSTUPNÝ TEXT viditeľný návštevníkovi: „{m.strip()}\"")

    n = len(re.findall(r"<h1\b", s))
    if n != 1:
        add("ERROR", p, f"počet <h1> = {n} (má byť práve 1)")

    for tag in ("div", "section", "main", "header", "footer", "nav", "ul", "li", "form", "figure", "picture"):
        o, c = len(re.findall(r"<" + tag + r"\b", s)), len(re.findall(r"</" + tag + r">", s))
        if o != c:
            add("ERROR", p, f"nesúlad <{tag}>: {o} otvorení vs {c} zatvorení")

    if 'lang="' not in s[:200]:
        add("WARN", p, "chýba lang na <html>")
    if '<meta name="theme-color"' not in s:
        add("WARN", p, "chýba theme-color")
    if "cookie-bar" not in s and not is404:
        add("WARN", p, "chýba cookie lišta")
    if not is404:
        for need, label in (('<meta name="description"', "meta description"),
                            ('<link rel="canonical"', "canonical"),
                            ("og:image", "og:image"), ("og:url", "og:url"),
                            ("og:description", "og:description"),
                            ("twitter:card", "twitter:card")):
            if need not in s:
                add("WARN", p, f"chýba {label}")

    md = re.search(r'<meta name="description" content="([^"]*)"', s)
    if md and not 70 <= len(md.group(1)) <= 170:
        add("WARN", p, f"meta description má {len(md.group(1))} znakov (ideál 70–170)")
    mt = re.search(r"<title>([^<]*)</title>", s)
    if mt and len(mt.group(1)) > 65:
        add("WARN", p, f"title má {len(mt.group(1))} znakov (>65 sa v Google odreže)")

    for m in re.finditer(r'(?:src|href)="((?:js|css)/[^"]+)"', s):
        if "?v=" not in m.group(1):
            add("WARN", p, f"bez cache-busting verzie (?v=): {m.group(1)}")

# Zástupné hodnoty priamo v config.js. Do HTML ich dopĺňa až JS za behu, takže
# v zdroji stránky ich nevidno — a pritom sú to práve tie údaje (telefón, e-mail),
# ktoré sa zobrazia na každej stránke a cez ktoré má zákazník firmu kontaktovať.
if cfg:
    for _k, _v in re.findall(r'^\s*(\w+):\s*"([^"]*)"', cfg, re.M):
        if _k in ("web3formsKey", "ga4Id", "gtmId", "customEndpoint"):
            continue                     # tieto smú byť prázdne / technické
        if _v and PLACEHOLDER.search(_v):
            add("ERROR", os.path.basename(a.config),
                f'zástupná hodnota v config.js: {_k} = "{_v}" – zobrazí sa návštevníkom')

# JSON-LD (štruktúrované dáta) je STATICKÝ – main.js doň nič nedopĺňa. Keď
# majiteľ neskôr doplní telefón/e-mail do config.js, v JSON-LD ostane pôvodná
# (často zástupná) hodnota a Google si prečíta nesprávny kontakt. Porovnáme ich.
if cfg:
    def _cfg_val(key):
        m = re.search(r'\b' + key + r':\s*"([^"]*)"', cfg)
        return m.group(1) if m else ""
    _norm = lambda v: re.sub(r"[^\dxX+]", "", v or "").upper()
    _c_email = _cfg_val("email")
    _c_tel = _cfg_val("phoneHref") or _cfg_val("phone")
    for p in pages:
        s = open(p, encoding="utf-8").read()
        for block in re.findall(r'(?is)application/ld\+json[^>]*>(.*?)</script>', s):
            jt = re.search(r'"telephone"\s*:\s*"([^"]*)"', block)
            je = re.search(r'"email"\s*:\s*"([^"]*)"', block)
            if jt and _c_tel and _norm(jt.group(1)) != _norm(_c_tel):
                add("WARN", p, f'JSON-LD telephone „{jt.group(1)}" nesedí s config.js '
                               f'(business.phoneHref) – JSON-LD je statický, oprav ho ručne')
            if je and _c_email and je.group(1).lower() != _c_email.lower():
                add("WARN", p, f'JSON-LD email „{je.group(1)}" nesedí s config.js '
                               f'(business.email) – JSON-LD je statický, oprav ho ručne')

# Verzia musí zodpovedať OBSAHU css/js. Ak nie, návštevníkom sa k novému HTML
# doručí starý štýl alebo staré údaje — a stránka sa im rozsype.
import hashlib
_assets = sorted(glob.glob("css/*.css") + glob.glob("js/*.js"))
if _assets:
    _h = hashlib.sha256()
    for f in _assets:
        _h.update(f.encode()); _h.update(open(f, "rb").read())
    _ocakavana = _h.hexdigest()[:8]
    _vhtml = set()
    for p in pages:
        _vhtml |= set(re.findall(r'(?:css|js)/[^"?]+\?v=([^"]*)', open(p, encoding="utf-8").read()))
    if _vhtml and _vhtml != {_ocakavana}:
        add("ERROR", "(všetky stránky)",
            f"verzia ?v= nezodpovedá obsahu css/js (v HTML: {', '.join(sorted(_vhtml))}, "
            f"malo by byť {_ocakavana}) – spusti scripts/bump_assets_version.py")

print("=" * 72)
for sev in ("ERROR", "WARN"):
    lst = issues[sev]
    print(f"\n### {sev}  ({len(lst)})")
    cur = None
    for f, m in sorted(lst):
        if f != cur:
            print(f"\n  {f}:")
            cur = f
        print(f"    - {m}")

ne, nw = len(issues["ERROR"]), len(issues["WARN"])
print("\n" + "=" * 72)
print(f"{'✅ Bez chýb.' if not ne else f'❌ {ne} chýb na opravu.'}  ({nw} upozornení)")
sys.exit(1 if ne or (a.strict and nw) else 0)
