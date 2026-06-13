# Ajoute à chaque coup de lines.json un champ "ev" = évaluation Stockfish APRÈS
# le coup, en centipièces du point de vue des BLANCS. Un cache par position (FEN)
# rend les exécutions suivantes quasi instantanées (seules les positions nouvelles
# sont calculées). À lancer ENTRE gen_lines.py et build.py :
#   python3 gen_lines.py && python3 eval_lines.py && python3 build.py
import json, os, chess, chess.engine

DEPTH = 14                      # suffisant et stable pour une barre d'éval
ENGINE = "/opt/homebrew/bin/stockfish"
CACHE_FILE = "eval_cache.json"

cache = {}
if os.path.exists(CACHE_FILE):
    cache = json.load(open(CACHE_FILE))

if not os.path.exists(ENGINE):
    # pas de moteur (autre machine) : on garde les ev déjà présents, on ne bloque pas le build
    print(f"⚠  Stockfish introuvable ({ENGINE}) — évals inchangées, build poursuivi.")
    raise SystemExit(0)

eng = chess.engine.SimpleEngine.popen_uci(ENGINE)
eng.configure({"Threads": 4, "Hash": 256})
computed = 0

def cp_after(board):
    """Éval (centipièces, point de vue Blancs) de la position courante, avec cache."""
    global computed
    key = board.fen()
    if key in cache:
        return cache[key]
    info = eng.analyse(board, chess.engine.Limit(depth=DEPTH))
    cp = info["score"].white().score(mate_score=100000)
    cache[key] = cp
    computed += 1
    return cp

def annotate(board, moves):
    """Joue les coups et écrit move['ev'] = éval après le coup."""
    for m in moves:
        board.push_san(m["san"])
        m["ev"] = cp_after(board)

data = json.load(open("lines.json"))
for line in data:
    b = chess.Board()
    annotate(b, line["moves"])
    for var in line.get("variations", []):
        vb = chess.Board()
        for entry in line["moves"][:var["at"]]:
            vb.push_san(entry["san"])
        annotate(vb, var["moves"])
eng.quit()

json.dump(cache, open(CACHE_FILE, "w"))
json.dump(data, open("lines.json", "w"), ensure_ascii=False)
print(f"évals ajoutées à lines.json ({computed} position(s) calculée(s), {len(cache)} en cache)")
