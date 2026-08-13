#!/usr/bin/env python3
"""
Generuje značkové zástupné SVG obrázky (placeholders) pre nový web.

Používaj, kým klient nedodá reálne fotky — SVG sú self-contained (žiadne
externé requesty), škálovateľné, drobné a v značkových farbách, takže web
vyzerá kompletne od začiatku. Reálne fotky sa neskôr len prekopírujú cez ne
(prípadne s onerror fallbackom, viď references/components.md).

Použitie:
    python gen_placeholder_svgs.py --out assets/img \
        --dark "#2C3E50" --accent "#E67E22" \
        --hero "Hlavný vizuál" \
        --card "produkt-1:Prvá služba" --card "produkt-2:Druhá služba" \
        --og "Názov firmy|Podnadpis|mesto | doména.sk"

Bez argumentov použije rozumné defaulty (neutrálna paleta, pár kariet).
"""
import argparse, os, colorsys


def _lighten(hexc, amt):
    hexc = hexc.lstrip('#')
    r, g, b = (int(hexc[i:i+2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0, min(1, l + amt))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))


def placeholder(w, h, dark, accent, label, uid):
    """Čistý značkový gradient placeholder s jemným motívom a popiskom."""
    top = _lighten(dark, 0.10)
    bot = _lighten(dark, -0.06)
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#bg{uid})"/>
  <circle cx="{int(w*0.82)}" cy="{int(h*0.2)}" r="{int(h*0.28)}" fill="{accent}" opacity="0.16"/>''']
    # jemné vodorovné linky ako neutrálny motív
    for i in range(4):
        y = int(h*0.30) + i*int(h*0.12)
        col = accent if i == 0 else '#ffffff'
        op = 0.9 if i == 0 else 0.14
        parts.append(f'  <rect x="{int(w*0.58)}" y="{y}" width="{int(w*0.30)}" height="6" rx="3" fill="{col}" opacity="{op}"/>')
    if label:
        parts.append(f'''  <rect x="{int(w*0.06)}" y="{h-int(h*0.16)}" rx="10" height="34" width="{12+len(label)*9.3:.0f}" fill="{_lighten(dark,-0.12)}" opacity="0.9"/>
  <text x="{int(w*0.06)+16}" y="{h-int(h*0.16)+23}" font-family="Arial,Helvetica,sans-serif" font-size="16" font-weight="700" fill="#fff">{label}</text>''')
    parts.append('\n</svg>\n')
    return '\n'.join(parts)


def og_banner(dark, accent, lines):
    """OG banner 1200x630. lines = 'H1|podnadpis|spodný riadok'."""
    parts = (lines.split('|') + ['', '', ''])[:3]
    h1, sub, foot = parts
    top = _lighten(dark, 0.06); bot = _lighten(dark, -0.08)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" aria-label="{h1}">
  <defs><linearGradient id="og" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs>
  <rect width="1200" height="630" fill="url(#og)"/>
  <circle cx="1050" cy="120" r="220" fill="{accent}" opacity="0.16"/>
  <g stroke="{accent}" stroke-width="10" stroke-linecap="round" opacity="0.9">
    <line x1="820" y1="250" x2="1120" y2="250"/><line x1="820" y1="300" x2="1120" y2="300"/><line x1="820" y1="350" x2="1120" y2="350"/>
  </g>
  <line x1="820" y1="400" x2="1120" y2="400" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity="0.9"/>
  <text x="90" y="260" font-family="Arial,Helvetica,sans-serif" font-size="72" font-weight="800" fill="#fff">{h1}</text>
  <text x="92" y="330" font-family="Arial,Helvetica,sans-serif" font-size="34" font-weight="600" fill="#c4d1de">{sub}</text>
  <text x="92" y="540" font-family="Arial,Helvetica,sans-serif" font-size="30" font-weight="700" fill="{accent}">{foot}</text>
</svg>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='assets/img')
    ap.add_argument('--dark', default='#2C3E50')
    ap.add_argument('--accent', default='#E67E22')
    ap.add_argument('--hero', default='')
    ap.add_argument('--card', action='append', default=[], help='name:Label (opakovateľné)')
    ap.add_argument('--og', default='', help='H1|podnadpis|spodný riadok')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    def write(name, svg):
        with open(os.path.join(a.out, name + '.svg'), 'w') as f:
            f.write(svg)
        print('wrote', name + '.svg')

    if a.hero:
        write('hero', placeholder(900, 720, a.dark, a.accent, '', 'hero'))
    for i, spec in enumerate(a.card):
        name, _, label = spec.partition(':')
        write(name, placeholder(800, 600, a.dark, a.accent, label or name, f'c{i}'))
    if a.og:
        write('og-image', og_banner(a.dark, a.accent, a.og))
    if not (a.hero or a.card or a.og):
        # defaultná ukážka
        write('hero', placeholder(900, 720, a.dark, a.accent, '', 'hero'))
        for i, lbl in enumerate(['Služba 1', 'Služba 2', 'Služba 3']):
            write(f'card-{i+1}', placeholder(800, 600, a.dark, a.accent, lbl, f'c{i}'))
        write('og-image', og_banner(a.dark, a.accent, 'Názov firmy|Podnadpis|doména.sk'))
    print('done')


if __name__ == '__main__':
    main()
