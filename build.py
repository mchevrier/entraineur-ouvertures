# Injecte lines.json et les pièces SVG dans template.html -> index.html
# Pièces : jeu standard "cburnett" de Colin M.L. Burnett (Wikimedia Commons,
# licence GPLv2+/BSD), embarquées en data-URI pour un rendu identique partout.
# Bump aussi automatiquement la version du cache dans sw.js quand index.html
# change, pour déclencher la bannière de mise à jour sur les appareils.
import base64
import json
import os
import re

lines = open("lines.json").read()

pieces = {}
for color_js, color_file in (("w", "l"), ("b", "d")):
    for piece in "kqrbnp":
        svg = open(os.path.join("pieces", f"{piece}{color_file}.svg"), "rb").read()
        b64 = base64.b64encode(svg).decode()
        pieces[color_js + piece.upper()] = f"data:image/svg+xml;base64,{b64}"
pieces_js = json.dumps(pieces)

tpl = open("template.html").read()
assert "__LINES__" in tpl and "__PIECES__" in tpl
out = tpl.replace("__LINES__", lines).replace("__PIECES__", pieces_js)

# index.html a-t-il changé ? (sinon inutile de bumper la version du cache)
changed = not os.path.exists("index.html") or open("index.html").read() != out
open("index.html", "w").write(out)

if changed:
    sw = open("sw.js").read()
    m = re.search(r'("ouvertures-v)(\d+)(")', sw)
    assert m, "sw.js : version de cache introuvable"
    new_ver = int(m.group(2)) + 1
    sw = sw[: m.start()] + f"{m.group(1)}{new_ver}{m.group(3)}" + sw[m.end() :]
    open("sw.js", "w").write(sw)
    print(f"index.html généré ({len(out) // 1024} Ko) — cache bumpé en v{new_ver}")
else:
    print(f"index.html généré ({len(out) // 1024} Ko) — inchangé, version du cache conservée")
