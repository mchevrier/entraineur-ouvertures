# Audit n°2 : "mon fils est-il prêt face au MEILLEUR coup adverse ?"
# Pour chaque coup de l'ADVERSAIRE dans chaque ligne/variante, on regarde si un
# moteur réglé à un horizon de club (profondeur 12, ~niveau des utilisateurs)
# préfère un coup nettement plus fort que celui enseigné — ET qui n'est pas déjà
# couvert par une variante. Si oui, l'enfant risque de ne pas savoir répondre.
#
# Usage : python3 audit2.py [depth]   (défaut 12)
import json, sys, chess, chess.engine

DEPTH = int(sys.argv[1]) if len(sys.argv) > 1 else 12
GAP = 120          # centipièces : écart mini pour considérer le coup adverse "bien meilleur"
ENGINE = "/opt/homebrew/bin/stockfish"

eng = chess.engine.SimpleEngine.popen_uci(ENGINE)
eng.configure({"Threads": 4, "Hash": 256})
cache = {}

def best_opppov(board):
    """(meilleur coup SAN, éval pov trait) à DEPTH, avec cache."""
    key = board.fen()
    if key in cache: return cache[key]
    info = eng.analyse(board, chess.engine.Limit(depth=DEPTH))
    san = board.san(info["pv"][0])
    cp = info["score"].pov(board.turn).score(mate_score=100000)
    cache[key] = (san, cp); return cache[key]

def move_eval_opppov(board, san):
    """éval (pov de celui qui vient de jouer 'san') après le coup."""
    turn = board.turn
    b2 = board.copy(); b2.push_san(san)
    info = eng.analyse(b2, chess.engine.Limit(depth=DEPTH))
    return info["score"].pov(turn).score(mate_score=100000)

def scan(seq_sans, opp_color, covered_at, label, findings, start=0):
    """seq_sans : coups SAN ; opp_color : 'w'/'b' = l'adversaire ; covered_at : dict ply->set(san couverts).
    start : on ne signale qu'à partir de cet indice (évite de re-scanner le préfixe commun)."""
    b = chess.Board()
    for i, san in enumerate(seq_sans):
        is_opp = (b.turn == chess.WHITE) == (opp_color == "w")
        if is_opp and i >= start:
            best_san, best_cp = best_opppov(b)
            played_cp = best_cp if best_san == san else move_eval_opppov(b, san)
            covered = covered_at.get(i, {san})
            if best_san not in covered and (best_cp - played_cp) >= GAP:
                movenum = i // 2 + 1
                dots = "." if b.turn == chess.WHITE else "..."
                findings.append(
                    f"  {movenum}{dots} enseigné: {san:6s} | l'adversaire a plus fort: {best_san} "
                    f"(+{(best_cp-played_cp)/100:.2f}) — non couvert")
        b.push_san(san)

data = json.load(open("lines.json"))
print(f"=== AUDIT n°2 — coups adverses (profondeur {DEPTH}, ~niveau club) ===\n")
total = 0
for line in data:
    opp = "b" if line["side"] == "w" else "w"      # l'adversaire = couleur opposée à l'enfant
    main = [m["san"] for m in line["moves"]]
    # cases couvertes sur la ligne principale = coup principal + 1er coup de chaque variante au point 'at'
    covered_main = {}
    for i in range(len(main)):
        covered_main[i] = {main[i]}
    for v in line.get("variations", []):
        covered_main.setdefault(v["at"], set()).update({main[v["at"]], v["moves"][0]["san"]})
    f = []
    scan(main, opp, covered_main, line["id"], f)
    # variantes : leurs propres coups adverses (pas de sous-variante)
    for v in line.get("variations", []):
        vs = [m["san"] for m in line["moves"][:v["at"]]] + [m["san"] for m in v["moves"]]
        scan(vs, opp, {}, f"{line['id']}/{v['name']}", f, start=v["at"])
    if f:
        print(f"### {line['id']}  ({'Blancs' if line['side']=='w' else 'Noirs'}) — {line['title']}")
        for msg in f: print(msg); total += 1
        print()
eng.quit()
print(f"=== {total} coup(s) adverse(s) plus fort(s) non couvert(s) (profondeur {DEPTH}, écart ≥ {GAP/100:.1f}) ===")
