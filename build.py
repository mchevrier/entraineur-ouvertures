# Injecte lines.json dans template.html -> index.html
lines = open("lines.json").read()
tpl = open("template.html").read()
assert "__LINES__" in tpl
open("index.html", "w").write(tpl.replace("__LINES__", lines))
print("index.html généré")
