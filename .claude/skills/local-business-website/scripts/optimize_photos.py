#!/usr/bin/env python3
"""
optimize_photos.py — pripraví fotky od klienta na web.

Robí to, čo urobí každý slušný web dev pred nasadením fotiek:
  - opraví rotáciu podľa EXIF (telefónne fotky bývajú „naležato"),
  - odstráni EXIF metadáta (GPS, model telefónu…),
  - zmenší veľmi veľké rozmery (default max dlhšia strana 1600 px),
  - prekóduje do úsporného progresívneho JPEG (default kvalita 82).

Voliteľne premenuje súbory podľa mapy (názvy z briefu → výstižné SEO názvy).

Predpoklad: Pillow (`pip install pillow`).

Použitie:
  # optimalizovať na mieste (prepíše):
  python optimize_photos.py assets/img/*.jpg

  # optimalizovať + premenovať podľa mapy (JSON: {"1.jpg":"realizacia-a.jpg", ...}):
  python optimize_photos.py --rename map.json --src-dir assets/img --out-dir assets/img --delete-src

  # vlastné limity:
  python optimize_photos.py --max 1200 --quality 80 assets/img/foto.jpg
"""
import argparse, json, os, sys
from PIL import Image, ImageOps


def optimize(in_path, out_path, max_side, quality):
    im = Image.open(in_path)
    im = ImageOps.exif_transpose(im)          # oprava rotácie
    im = im.convert('RGB')                      # bez alfa, čistý JPEG
    w, h = im.size
    if max(w, h) > max_side:
        if w >= h:
            im = im.resize((max_side, round(h * max_side / w)), Image.LANCZOS)
        else:
            im = im.resize((round(w * max_side / h), max_side), Image.LANCZOS)
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    im.save(out_path, 'JPEG', quality=quality, optimize=True, progressive=True)  # bez EXIF
    return im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='*', help='vstupné fotky (ak nie je --rename)')
    ap.add_argument('--rename', help='JSON mapa {stary_nazov: novy_nazov}')
    ap.add_argument('--src-dir', default='.')
    ap.add_argument('--out-dir', default='.')
    ap.add_argument('--delete-src', action='store_true', help='zmazať pôvodné súbory po premenovaní')
    ap.add_argument('--max', type=int, default=1600)
    ap.add_argument('--quality', type=int, default=82)
    a = ap.parse_args()

    jobs = []
    if a.rename:
        mp = json.load(open(a.rename))
        for src, dst in mp.items():
            jobs.append((os.path.join(a.src_dir, src), os.path.join(a.out_dir, dst)))
    else:
        for f in a.files:
            jobs.append((f, f))  # na mieste
    if not jobs:
        print('Nič na spracovanie. Zadaj súbory alebo --rename map.json.'); sys.exit(1)

    for src, dst in jobs:
        if not os.path.exists(src):
            print('  ! chýba', src); continue
        before = os.path.getsize(src)
        # ak píšeme na to isté miesto, najprv do temp
        tmp = dst + '.tmp' if src == dst else dst
        wsz = optimize(src, tmp, a.max, a.quality)
        if tmp != dst:
            os.replace(tmp, dst)
        after = os.path.getsize(dst)
        print(f'  ✓ {os.path.basename(src)} → {os.path.basename(dst)}: '
              f'{wsz[0]}x{wsz[1]}px, {after//1024} kB (pôvodne {before//1024} kB)')
        if a.delete_src and os.path.abspath(src) != os.path.abspath(dst):
            os.remove(src)
    print('done')


if __name__ == '__main__':
    main()
