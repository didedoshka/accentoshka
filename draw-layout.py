#!/usr/bin/env python3
"""Draw an ANSI keyboard SVG from a macOS .keylayout (textual parse; entities tolerated).

Regenerates accentoshka.svg from the bundle keylayout.
"""
import re, html

path, out, bi, si, oi, wl = "Accentoshka.bundle/Contents/Resources/Accentoshka.keylayout", "accentoshka.svg", 0, 1, 2, "éèêëàâîïôùûüçœ«»"
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

base, shift, opt = maps[bi], maps[si], maps[oi]
whitelist = set(wl)

LABELS = {"Bksp": "⌫", "Tab": "⇥", "Caps": "⇪", "Enter": "⏎", "Shift": "⇧"}
ROWS = [
    (10, [(10, 56, 50), (70, 56, 18), (130, 56, 19), (190, 56, 20), (250, 56, 21), (310, 56, 23),
          (370, 56, 22), (430, 56, 26), (490, 56, 28), (550, 56, 25), (610, 56, 29), (670, 56, 27),
          (730, 56, 24), (790, 116, "Bksp")]),
    (70, [(10, 86, "Tab"), (100, 56, 12), (160, 56, 13), (220, 56, 14), (280, 56, 15), (340, 56, 17),
          (400, 56, 16), (460, 56, 32), (520, 56, 34), (580, 56, 31), (640, 56, 35), (700, 56, 33),
          (760, 56, 30), (820, 86, 42)]),
    (130, [(10, 101, "Caps"), (115, 56, 0), (175, 56, 1), (235, 56, 2), (295, 56, 3), (355, 56, 5),
           (415, 56, 4), (475, 56, 38), (535, 56, 40), (595, 56, 37), (655, 56, 41), (715, 56, 39),
           (775, 131, "Enter")]),
    (190, [(10, 131, "Shift"), (145, 56, 6), (205, 56, 7), (265, 56, 8), (325, 56, 9), (385, 56, 11),
           (445, 56, 45), (505, 56, 46), (565, 56, 43), (625, 56, 47), (685, 56, 44), (745, 161, "Shift")]),
]

esc = lambda s: html.escape(s, quote=False)
L = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 912 256" font-family="Helvetica, Arial, sans-serif">',
     '<style>.key{fill:#fdfdfd;stroke:#444;stroke-width:1.2;rx:6;}.main{font-size:20px;fill:#111;}'
     '.shift{font-size:12px;fill:#666;}.altgr{font-size:20px;fill:#c0392b;}.label{font-size:17px;fill:#999;}</style>']
for y, keys in ROWS:
    for x, w, code in keys:
        cx = x + w / 2
        L.append(f'<rect class="key" x="{x}" y="{y}" width="{w}" height="{56}" rx="6"/>')
        if isinstance(code, str):
            L.append(f'<text class="label" x="{cx:g}" y="{y+35}" text-anchor="middle">{LABELS[code]}</text>')
            continue
        b = base.get(code, "")
        main = b.upper() if b.isalpha() else b
        o = opt.get(code, "")
        if o and o in whitelist:
            # accent keys: the accented letter is the big legend, the QWERTY letter sits small above
            L.append(f'<text class="altgr" x="{cx:g}" y="{y+40}" text-anchor="middle">{esc(o)}</text>')
            L.append(f'<text class="shift" x="{cx:g}" y="{y+18}" text-anchor="middle">{esc(main)}</text>')
            continue
        L.append(f'<text class="main" x="{cx:g}" y="{y+40}" text-anchor="middle">{esc(main)}</text>')
        s = shift.get(code, "")
        if s and s != main:
            L.append(f'<text class="shift" x="{cx:g}" y="{y+18}" text-anchor="middle">{esc(s)}</text>')
L.append("</svg>")
open(out, "w", encoding="utf-8").write("\n".join(L))
print("wrote", out)
