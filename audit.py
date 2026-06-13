# Audit Stockfish des lignes/variantes de lines.json.
# Rejoue chaque ligne et variante, évalue chaque position, et signale les coups
# DU CAMP ENTRAÎNÉ (line.side) qui perdent trop d'évaluation. Les coups adverses
# et les pièges (traps) ne sont pas jugés : ils n'ont pas à être optimaux.
#
# Usage : python3 audit.py [depth]   (depth par défaut 16, suffisant <2000 ELO)
import json
import sys
import chess
import chess.engine

DEPTH = int(sys.argv[1]) if len(sys.argv) > 1 else 16
ENGINE = "/opt/homebrew/bin/stockfish"
INACC, MISTAKE, BLUNDER = 100, 200, 300  # seuils en centipièces (perte du camp entraîné)

eng = chess.engine.SimpleEngine.popen_uci(ENGINE)
eng.configure({"Threads": 4, "Hash": 256})
cache = {}

def whitepov_cp(board):
    """Éval de la position (centipièces, point de vue des Blancs), avec cache par FEN."""
    key = board.board_fen() + (" w" if board.turn else " b") + " " + (board.castling_xfen())
    if key in cache:
        return cache[key]
    info = eng.analyse(board, chess.engine.Limit(depth=DEPTH))
    cp = info["score"].white().score(mate_score=100000)
    cache[key] = cp
    return cp

def severity(drop):
    if drop >= BLUNDER: return "GAFFE  "
    if drop >= MISTAKE: return "erreur "
    if drop >= INACC:   return "imprécis"
    return None

def audit_sequence(san_moves, side, label):
    """side = couleur entraînée ('w'/'b'). Rejoue et juge les coups de ce camp."""
    sign = 1 if side == "w" else -1
    board = chess.Board()
    findings = []
    before = whitepov_cp(board)
    for i, san in enumerate(san_moves):
        mover_is_trained = (board.turn == chess.WHITE) == (side == "w")
        try:
            board.push_san(san)
        except Exception as e:
            return [(99, f"  !! coup illégal {san} : {e}")], None
        after = whitepov_cp(board)
        if mover_is_trained:
            drop = sign * (before - after)   # >0 = le camp entraîné a perdu de l'éval
            sev = severity(drop)
            if sev:
                movenum = i // 2 + 1
                dots = "." if board.turn == chess.BLACK else "..."  # qui vient de jouer
                findings.append((drop, f"  {sev}  {movenum}{dots}{san:6s}  perd {drop/100:+.2f}  (éval {sign*before/100:+.2f} -> {sign*after/100:+.2f})"))
        before = after
    final = sign * before / 100
    return findings, final

data = json.load(open("lines.json"))
print(f"=== AUDIT Stockfish (profondeur {DEPTH}) — perte du camp entraîné ===\n")
total_flags = 0
for line in data:
    side = line["side"]
    # ligne principale
    sans = [m["san"] for m in line["moves"]]
    print(f"### {line['id']}  ({'Blancs' if side=='w' else 'Noirs'})  — {line['title']}")
    f, final = audit_sequence(sans, side, line["id"])
    for _, msg in sorted(f, reverse=True):
        print(msg); total_flags += 1
    print(f"  ligne principale -> éval finale {final:+.2f} pour {'Blancs' if side=='w' else 'Noirs'}")
    # variantes
    for var in line.get("variations", []):
        at = var["at"]
        prefix = [m["san"] for m in line["moves"][:at]]
        vsans = prefix + [m["san"] for m in var["moves"]]
        fv, finalv = audit_sequence(vsans, side, f"{line['id']}/{var['name']}")
        head = f"  └ variante « {var['name']} »"
        flagged = [msg for _, msg in sorted(fv, reverse=True)]
        if flagged:
            print(head)
            for msg in flagged: print("  " + msg); total_flags += 1
            print(f"     -> éval finale {finalv:+.2f}")
        else:
            print(f"{head} : OK  (éval finale {finalv:+.2f})")
    print()

eng.quit()
print(f"=== {total_flags} coup(s) signalé(s) (imprécis/erreur/gaffe) du camp entraîné ===")
