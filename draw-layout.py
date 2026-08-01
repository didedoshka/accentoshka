#!/usr/bin/env python3
"""Draw an ANSI keyboard SVG from a macOS .keylayout (textual parse; entities tolerated).

Regenerates accentoshka.svg from the bundle keylayout.
"""
import re, html

path, out, bi, oi, wl = "Accentoshka.bundle/Contents/Resources/Accentoshka.keylayout", "accentoshka.svg", 0, 2, "éèêëàâîïôùûüçœ«»"
text = open(path, encoding="utf-8").read()

maps = {}
for m in re.finditer(r'<keyMap index="(\d)">\n(.*?)\n        </keyMap>', text, re.S):
    d = {}
    for k in re.finditer(r'<key code="(\d+)" output="([^"]*)"/>', m.group(2)):
        v = k.group(2)
        v = re.sub(r"&#x([0-9A-Fa-f]+);", lambda mm: chr(int(mm.group(1), 16)), v)
        v = v.replace("&#x0026;", "&").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'")
        d[int(k.group(1))] = v
    maps[int(m.group(1))] = d

base, opt = maps[bi], maps[oi]
whitelist = set(wl)

# letter keys only, with the physical ANSI row stagger
ROWS = [
    (10, 10, [12, 13, 14, 15, 17, 16, 32, 34, 31, 35]),    # q w e r t y u i o p
    (70, 25, [0, 1, 2, 3, 5, 4, 38, 40, 37]),              # a s d f g h j k l
    (130, 55, [6, 7, 8, 9, 11, 45, 46]),                   # z x c v b n m
]

esc = lambda s: html.escape(s, quote=False)
L = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 616 196" font-family="Helvetica, Arial, sans-serif">',
     '<style>.key{fill:#fdfdfd;stroke:#444;stroke-width:1.2;rx:6;}.main{font-size:20px;fill:#111;}'
     '.shift{font-size:12px;fill:#666;}</style>']
for y, x0, codes in ROWS:
    for i, code in enumerate(codes):
        x = x0 + 60 * i
        cx = x + 28
        L.append(f'<rect class="key" x="{x}" y="{y}" width="56" height="56" rx="6"/>')
        main = base[code].upper()
        # QWERTY letter small in the corner; on accent keys the accent is the big centered legend
        L.append(f'<text class="shift" x="{x+10}" y="{y+18}" text-anchor="middle">{esc(main)}</text>')
        o = opt.get(code, "")
        if o and o in whitelist:
            L.append(f'<text class="main" x="{cx}" y="{y+40}" text-anchor="middle">{esc(o)}</text>')
L.append("</svg>")
open(out, "w", encoding="utf-8").write("\n".join(L))
print("wrote", out)
