#!/usr/bin/env python3
"""Generate home-screen icons from cross.png.

cross.png is transparent, which is wrong for an app icon: iOS composites a
transparent icon onto a background of its own choosing and Android will letter
it into whatever shape the launcher uses. So the app's own background is baked
in and the cross is centred on its opaque bounds rather than the image's — the
source has more empty space on one side than the other, and centring the file
would leave the cross visibly off-centre on the home screen.

Usage: build_icons.py
"""
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
OUT = os.path.join(ROOT, 'icons')
BG = (18, 18, 18, 255)            # --bg in the dark theme

# A launcher may crop a maskable icon to a circle, so that one keeps the cross
# well inside the safe area.
SIZES = [
    ('icon-180.png', 180, 0.62, False),
    ('icon-192.png', 192, 0.62, False),
    ('icon-512.png', 512, 0.62, False),
    ('icon-maskable-512.png', 512, 0.46, True),
]


def main():
    src = Image.open(os.path.join(ROOT, 'cross.png')).convert('RGBA')
    box = src.getchannel('A').getbbox()
    cross = src.crop(box)

    os.makedirs(OUT, exist_ok=True)
    for name, size, scale, maskable in SIZES:
        canvas = Image.new('RGBA', (size, size), BG)
        target = int(size * scale)
        w, h = cross.size
        ratio = min(target / w, target / h)
        art = cross.resize((max(1, int(w * ratio)), max(1, int(h * ratio))),
                           Image.LANCZOS)
        canvas.alpha_composite(art, ((size - art.width) // 2,
                                     (size - art.height) // 2))
        path = os.path.join(OUT, name)
        canvas.convert('RGB').save(path, 'PNG', optimize=True)
        print('%-24s %4dpx  %5.1f KB%s'
              % (name, size, os.path.getsize(path) / 1024,
                 '  (maskable)' if maskable else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
