# Injecte lines.json et les pièces SVG dans template.html -> index.html
# Pièces : jeu standard "cburnett" de Colin M.L. Burnett (Wikimedia Commons,
# licence GPLv2+/BSD), embarquées en data-URI pour un rendu identique partout.
import base64
import json
import os

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
open("index.html", "w").write(out)
print(f"index.html généré ({len(out) // 1024} Ko)")
