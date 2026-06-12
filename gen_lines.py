# Génère lines.json : répertoire d'ouvertures validé par python-chess.
# Chaque ligne : san + commentaires ; le script vérifie la légalité de chaque coup,
# l'absence de prise en passant (non gérée par l'appli) et le mat annoncé.
import chess
import json

# (san, commentaire ou None) — les commentaires s'affichent dans l'appli.
LINES = [
    # ------------------------- BLANCS -------------------------
    dict(
        id="italienne-blancs", side="w", emoji="🏛️",
        title="L'Italienne tranquille",
        desc="Ton plan principal avec les Blancs : développement rapide, roque, puis attaque !",
        moves=[
            ("e4", "Tu prends le centre et tu ouvres la voie à ton fou et à ta dame."),
            ("e5", None),
            ("Nf3", "Tu développes en attaquant le pion e5 : un coup, deux idées !", {
                "Qh5": "Le coup du berger ?! Tu sais toi-même le punir (c'est ton module ⚔️ !) : un adversaire préparé chasse ta dame en développant et tu te retrouves en retard partout. Cf3, propre et fort !",
            }),
            ("Nc6", None),
            ("Bc4", "Le fou vise f7, la case la plus fragile des Noirs."),
            ("Bc5", None),
            ("c3", "Tu prépares d4 pour construire un grand centre."),
            ("Nf6", None),
            ("d3", "Solide : tu protèges e4 et tu libères ton fou c1.", {
                "d4": "Trop pressé ! Après ...exd4 cxd4 vient ...Fb4+ ! l'échec qui dérange — exactement le coup que TOI tu joues avec les Noirs contre l'Italienne ! D'abord d3 et le roque, le centre viendra après.",
            }),
            ("d6", None),
            ("O-O", "Le roi à l'abri AVANT d'attaquer. Toujours !"),
            ("O-O", None),
            ("Re1", "La tour soutient le centre et prépare la suite."),
            ("a6", None),
            ("Bb3", "Tu mets ton fou à l'abri de ...Na5 : il reste braqué sur f7."),
            ("Ba7", None),
            ("h3", "Petit coup malin : tu interdis ...Bg4 qui clouerait ton cavalier."),
            ("h6", None),
            ("Nbd2", "Le plan magique : ce cavalier va voyager d2 → f1 → g3 vers le roi noir !"),
        ],
        variations=[
            dict(at=3, name="La Petroff (2...Cf6)", moves=[
                ("Nf6", None),
                ("Nxe5", "Prends ! Et retiens le piège : s'il copiait avec ...Cxe4 ?, De2 ! gagnerait une pièce (échec à la découverte en c6)."),
                ("d6", None),
                ("Nf3", "Recule tranquillement : il va reprendre e4, c'est prévu."),
                ("Nxe4", None),
                ("d4", "Le grand centre, comme toujours."),
                ("d5", None),
                ("Bd3", "Tu développes en visant son cavalier e4 : il devra le défendre encore et encore."),
                ("Nc6", None),
                ("O-O", "Roi à l'abri avant la suite."),
                ("Be7", None),
                ("c4", "Tu grignotes son centre : un peu plus d'espace pour toi, partie facile à jouer."),
            ]),
            dict(at=5, name="Le piège Blackburne-Shilling (3...Cd4 ?!)", moves=[
                ("Nd4", None),
                ("Nxd4", "STOP, c'est un piège célèbre ! Si tu prenais e5 ?? ...Dg5 ! gagnerait la partie (g2 et f2 tombent en même temps). Prends simplement le cavalier."),
                ("exd4", None),
                ("c3", "Tu dissous son pion avancé tout en préparant ton développement."),
                ("dxc3", None),
                ("Nxc3", "Compte les pièces : tu développes en reprenant, lui n'a RIEN développé. Son piège est devenu ton avantage. 😎"),
            ]),
            dict(at=5, name="Les Deux Cavaliers (3...Cf6)", moves=[
                ("Nf6", None),
                ("d3", "Contre les Deux Cavaliers, joue tranquille : d3 protège e4 avant tout."),
                ("Bc5", None),
                ("c3", "Comme dans la ligne principale : tu prépares d4."),
                ("d6", None),
                ("O-O", "Roi à l'abri, comme toujours."),
                ("O-O", None),
                ("Re1", "La tour soutient le centre : tu retrouves TA position habituelle !"),
                ("a6", None),
                ("Bb3", "Même maison, autre chemin : c'est la force d'un vrai répertoire."),
            ]),
        ],
    ),
    dict(
        id="piege-legal", side="w", emoji="🪤",
        title="Le piège de Légal",
        desc="Un piège célèbre quand les Noirs jouent ...d6 et ...Bg4 : tu « sacrifies » ta dame... pour faire mat !",
        moves=[
            ("e4", "Le centre, comme toujours."),
            ("e5", None),
            ("Nf3", "Développement avec attaque sur e5."),
            ("Nc6", None),
            ("Bc4", "Le fou vise f7."),
            ("d6", None),
            ("Nc3", "Tu développes tranquillement... le piège se prépare."),
            ("Bg4", None),
            ("h3", "Tu poses la question au fou : il doit choisir."),
            ("Bh5", None),
            ("Nxe5", "Le coup de tonnerre ! Oui, ta dame est en prise... mais regarde la suite !"),
            ("Bxd1", None),
            ("Bxf7+", "Échec ! Le roi noir est obligé d'avancer."),
            ("Ke7", None),
            ("Nd5#", "ÉCHEC ET MAT avec deux cavaliers et un fou ! La dame n'a même pas servi. 🎉"),
        ],
    ),
    dict(
        id="fried-liver", side="w", emoji="🍳",
        title="La Fried Liver (contre 3...Cf6)",
        desc="L'arme fatale contre les Deux Cavaliers : le sacrifice Cxf7 ! qui arrache le roi noir de sa maison. Alternative musclée à ton tranquille 4.d3.",
        moves=[
            ("e4", "Comme toujours."),
            ("e5", None),
            ("Nf3", "Développement avec attaque sur e5."),
            ("Nc6", None),
            ("Bc4", "Le fou vise f7."),
            ("Nf6", None),
            ("Ng5", "L'attaque ! Deux pièces visent f7 : la menace Cxf7 est immédiate.", {
                "d3": "Très bon coup aussi... mais c'est ta ligne TRANQUILLE (variante Deux Cavaliers de l'Italienne) ! Ici on dégaine l'arme musclée : Cg5 ! et f7 tremble.",
            }),
            ("d5", None),
            ("exd5", "Prends : il doit maintenant décider comment récupérer d5..."),
            ("Nxd5", None),
            ("Nxf7", "LE SACRIFICE du Foie Frit ! Tu donnes un cavalier pour arracher le roi noir au grand jour.", {
                "Bxd5": "Ne reprends pas le pion : après ...Dxd5 ! sa dame se centralise en attaquant ton cavalier g5 ET g2. Le grand moment, c'est le sacrifice Cxf7 !",
            }),
            ("Kxf7", None),
            ("Qf3+", "Échec ! Le roi est obligé d'avancer en e6 pour sauver son cavalier d5 cloué.", {
                "Qh5+": "Mauvais échec : ...g6 ! repousse ta dame et il se consolide. Df3+ ! est LA pointe : il cloue le cavalier d5 et force le roi à s'avancer.",
            }),
            ("Ke6", None),
            ("Nc3", "Encore une pièce sur d5 : tout ton monde converge vers le roi baladeur."),
            ("Nb4", None),
            ("Qe4", "La dame se recentre : pression maximale sur d5 et e5."),
            ("c6", None),
            ("a3", "Tu repousses le cavalier avant l'assaut final."),
            ("Na6", None),
            ("d4", "Ouvre le centre : avec un roi en e6, chaque colonne ouverte est un danger mortel. À toi de conclure ! 🔥"),
        ],
        variations=[
            dict(at=9, name="La bonne défense 5...Ca5", moves=[
                ("Na5", None),
                ("Bb5+", "Il connaît la parade ! Pas grave : échec intermédiaire, tu gardes l'initiative."),
                ("c6", None),
                ("dxc6", "Prends encore : ton pion d5 se transforme en pion c6."),
                ("bxc6", None),
                ("Be2", "Recule au calme : tu as UN PION DE PLUS et une position saine. Il va attaquer pour compenser : défends, échange les pièces, et ta technique fera le reste. 🧮"),
            ]),
        ],
    ),
    dict(
        id="anti-sicilienne", side="w", emoji="🛡️",
        title="Contre la Sicilienne : l'Alapin",
        desc="Si on te joue 1...c5, réponds 2.c3 : tu construis ton grand centre quand même !",
        moves=[
            ("e4", "Ton premier coup, toujours le même."),
            ("c5", None),
            ("c3", "L'idée : préparer d4 et reprendre du pion c. Le grand centre arrive.", {
                "d4": "Bon coup... mais c'est ton MORRA ! 💣 Ici on s'entraîne à l'Alapin : c3 prépare le même grand centre, sans sacrifier de pion.",
            }),
            ("Nf6", None),
            ("e5", "Tu chasses le cavalier en gagnant de l'espace."),
            ("Nd5", None),
            ("d4", "Voilà ton grand centre ! C'est tout l'intérêt de 2.c3."),
            ("cxd4", None),
            ("Nf3", "Développe d'abord, reprends après : pas de précipitation.", {
                "Qxd4": "Ta dame au milieu trop tôt : ...e6 puis ...Cc6 la chasseraient en développant gratuitement. Cf3 d'abord — le pion ne s'envolera pas.",
            }),
            ("Nc6", None),
            ("cxd4", "Tu reprends : deux pions au centre contre zéro, l'espace est pour toi."),
            ("d6", None),
            ("Bc4", "Le fou attaque le cavalier d5 qui n'a plus de bonne case."),
            ("Nb6", None),
            ("Bb5", "Tu cloues le cavalier c6 : la pression monte sur le centre noir."),
        ],
        variations=[
            dict(at=3, name="La riposte 2...d5", moves=[
                ("d5", None),
                ("exd5", "Prends : sa dame va devoir venir au milieu trop tôt."),
                ("Qxd5", None),
                ("d4", "Ton grand centre arrive quand même : c'est tout le plan de 2.c3."),
                ("Nf6", None),
                ("Nf3", "Développement naturel."),
                ("e6", None),
                ("Be2", "Tranquille : le roque approche."),
                ("Nc6", None),
                ("O-O", "Roi en sécurité."),
                ("cxd4", None),
                ("cxd4", "Tu reprends : beau centre, jeu facile."),
                ("Be7", None),
                ("Nc3", "Développe EN attaquant sa dame : tu gagnes un temps gratuit !"),
            ]),
        ],
    ),
    dict(
        id="morra", side="w", emoji="💣",
        title="Le gambit Smith-Morra (anti-Sicilienne)",
        desc="Ton arme surprise contre 1...c5 : un pion sacrifié contre un développement éclair et des pièges partout !",
        moves=[
            ("e4", "On commence pareil."),
            ("c5", None),
            ("d4", "Tu offres un pion tout de suite : c'est le Morra ! En échange, un développement foudroyant."),
            ("cxd4", None),
            ("c3", "Le deuxième coup du gambit : s'il prend, toutes tes pièces vont sortir avec des menaces.", {
                "Qxd4": "Surtout pas : ...Cc6 ! chasserait ta dame en développant — tu offrirais le temps que ton gambit veut justement gagner. Le Morra, c'est c3 !",
            }),
            ("dxc3", None),
            ("Nxc3", "Un pion de moins, mais regarde : cavalier dehors, et les colonnes c et d s'ouvrent pour tes tours."),
            ("Nc6", None),
            ("Nf3", "Pièce après pièce, sans reprendre ton souffle."),
            ("d6", None),
            ("Bc4", "Le fou vise f7, comme d'habitude."),
            ("e6", None),
            ("O-O", "Roi à l'abri : tu es déjà prêt, lui non."),
            ("Nf6", None),
            ("Qe2", "Le secret du Morra : la dame en e2 laisse la colonne d à la tour..."),
            ("Be7", None),
            ("Rd1", "...et voilà ! Ta tour fixe sa dame aux rayons X : d6 va craquer. Toutes tes pièces jouent — c'est ça, un gambit. ⚡"),
        ],
        variations=[
            dict(at=11, name="Le piège 6...Cf6 ? 7.e5 !", moves=[
                ("Nf6", None),
                ("e5", "Le coup de tonnerre du Morra ! Tout s'ouvre d'un coup sur le cavalier f6 et le pion d6."),
                ("dxe5", None),
                ("Qxd8+", "Échange d'abord les dames..."),
                ("Nxd8", None),
                ("Nb5", "...et voilà la pointe : Cc7+ menace, fourchette royale sur le roi et la tour !"),
                ("Rb8", None),
                ("Nxe5", "Pion récupéré, et regarde f7 et c7 trembler sous tes deux cavaliers et ton fou : position de rêve. 🌪️"),
            ]),
            dict(at=5, name="Le refus 3...Cf6", moves=[
                ("Nf6", None),
                ("e5", "Il refuse le gambit ? Chasse le cavalier en gagnant de l'espace."),
                ("Nd5", None),
                ("Nf3", "Développe tranquillement..."),
                ("Nc6", None),
                ("cxd4", "...reprends ton pion..."),
                ("d6", None),
                ("Bc4", "...attaque le cavalier d5..."),
                ("Nb6", None),
                ("Bb5", "...et te voilà EXACTEMENT dans ton Alapin ! Deux ouvertures pour le prix d'une. 😄"),
            ]),
        ],
    ),
    dict(
        id="anti-francaise", side="w", emoji="🥖",
        title="Contre la Française : l'avance",
        desc="Si on te joue 1...e6, pousse e5 : tu gagnes de l'espace et le fou c8 reste enfermé !",
        moves=[
            ("e4", "On commence pareil."),
            ("e6", None),
            ("d4", "Deux pions au centre, profites-en."),
            ("d5", None),
            ("e5", "Tu avances ! Le fou c8 des Noirs est enfermé derrière ses pions."),
            ("c5", None),
            ("c3", "Tu défends d4 : ta chaîne de pions est solide comme un mur.", {
                "dxc5": "Ne gobe pas c5 : tu abandonnerais ton beau centre, et son fou reprend le pion en développant — tu connais la leçon, c'est le piège de la Londres à l'envers ! Soutiens d4 avec c3.",
            }),
            ("Nc6", None),
            ("Nf3", "Développement en protégeant d4 une deuxième fois."),
            ("Qb6", None),
            ("a3", "Coup pro : tu prépares b4 et tu enlèves la case b4 aux pièces noires."),
            ("Nh6", None),
            ("b4", "De l'espace à gauche aussi ! Ton centre tient, tu joues sur tout l'échiquier."),
        ],
    ),
    dict(
        id="anti-caro", side="w", emoji="🏰",
        title="Contre la Caro-Kann : l'avance",
        desc="Si on te joue 1...c6, même recette : pousse e5 et joue simple et solide.",
        moves=[
            ("e4", "Toujours le même premier coup : c'est ça, un répertoire."),
            ("c6", None),
            ("d4", "Le grand centre, sans hésiter."),
            ("d5", None),
            ("e5", "Tu gagnes de l'espace. Ici le fou c8 peut sortir... mais tu as un plan."),
            ("Bf5", None),
            ("Nf3", "Développement simple, tu vises un roque rapide."),
            ("e6", None),
            ("Be2", "Tranquille : le fou sort, le roque arrive au prochain coup."),
            ("Nd7", None),
            ("O-O", "Roi en sécurité. Maintenant tu as l'espace et tout ton temps."),
            ("Ne7", None),
            ("Nbd2", "Dernier développement : tu es prêt, et les Noirs sont tout serrés."),
        ],
    ),
    dict(
        id="anti-scandinave", side="w", emoji="🛶",
        title="Contre la Scandinave",
        desc="1...d5 : très joué chez les jeunes ! Prends, puis harcèle sa dame sortie trop tôt.",
        moves=[
            ("e4", "Toujours pareil."),
            ("d5", None),
            ("exd5", "Prends sans hésiter : sa dame va devoir se montrer beaucoup trop tôt."),
            ("Qxd5", None),
            ("Nc3", "Développe EN attaquant la dame : un temps gratuit pour toi !"),
            ("Qa5", None),
            ("d4", "Le grand centre, pendant que sa dame se promène."),
            ("Nf6", None),
            ("Nf3", "Développement simple : pièce après pièce."),
            ("c6", None),
            ("Bc4", "Le fou vise f7, comme d'habitude."),
            ("Bf5", None),
            ("Bd2", "Coup pro : tu protèges c3 et tu prépares une menace cachée (Cd5 !) et le grand roque."),
            ("e6", None),
            ("Qe2", "Avant-dernière étape : la dame laisse la place au grand roque."),
            ("Bb4", None),
            ("O-O-O", "Grand roque ! Pourquoi pas le petit ? Parce que ta tour atterrit PILE sur d1, la colonne du combat : elle soutient d4 et prépare la percée d4-d5. Et comme leur roi roquera petit, tu lanceras g4 ! (chasse le fou) puis g5 (chasse le cavalier) : une attaque gratuite, loin de ton roi bien gardé derrière a2-b2-c2. 💥"),
        ],
        variations=[
            dict(at=3, name="La moderne 2...Cf6", moves=[
                ("Nf6", None),
                ("d4", "Ne t'accroche pas au pion d5 : prends le centre ! Il reprendra son pion, toi tu développes."),
                ("Nxd5", None),
                ("Nf3", "Développement tranquille : tu as le centre, lui non."),
                ("g6", None),
                ("Be2", "Simple : le roque arrive."),
                ("Bg7", None),
                ("O-O", "Roi à l'abri."),
                ("O-O", None),
                ("c4", "Tu gagnes de l'espace en chassant son cavalier."),
                ("Nb6", None),
                ("Nc3", "Regarde ton centre et compare : l'espace est pour toi, partout. 🏰"),
            ]),
            dict(at=5, name="La retraite 3...Dd8", moves=[
                ("Qd8", None),
                ("d4", "Elle rentre à la maison ? Parfait : il a perdu deux temps, prends le centre."),
                ("Nf6", None),
                ("Nf3", "Développe, simplement : chaque coup compte."),
                ("Bg4", None),
                ("Be2", "Pare le clouage sans te presser."),
                ("e6", None),
                ("O-O", "Roi en sécurité : tu as le centre ET de l'avance au développement."),
                ("Be7", None),
                ("h3", "Pose la question au fou : s'il prend, Fxf3 visera b7 !"),
            ]),
        ],
    ),
    dict(
        id="anti-pirc", side="w", emoji="🐉",
        title="Contre la Pirc (1...d6 et ...g6)",
        desc="Il te laisse tout le centre pour attaquer ton mur plus tard ? Installe-toi solidement, développe tout, et il ne se passera rien pour lui.",
        moves=[
            ("e4", "On commence pareil."),
            ("d6", None),
            ("d4", "Il te laisse le centre ? Prends-le en entier, merci !"),
            ("Nf6", None),
            ("Nc3", "Tu protèges e4 en développant."),
            ("g6", None),
            ("Nf3", "La Pirc ! Pas besoin de se précipiter : développe tout, ton centre est déjà gagné."),
            ("Bg7", None),
            ("Be2", "Simple et solide : le roque approche."),
            ("O-O", None),
            ("O-O", "Roi à l'abri. Ton centre est un mur, le sien n'existe pas."),
            ("Bg4", None),
            ("Be3", "Tu renforces d4 : son fou g7 mord dans la pierre."),
            ("Nc6", None),
            ("Qd2", "Tout est connecté ! Plan : h3 pour chasser le fou, puis avancer au centre quand TU le décides. 🗿"),
        ],
    ),
    # ------------------------- NOIRS -------------------------
    dict(
        id="anti-berger", side="b", emoji="⚔️",
        title="Stopper le coup du berger",
        desc="2.Dh5 ?! Beaucoup d'enfants le jouent. Apprends à punir la sortie de dame trop tôt !",
        moves=[
            ("e4", None),
            ("e5", "Tu prends ta part du centre."),
            ("Qh5", None),
            ("Nc6", "Surtout pas panique : tu défends e5 EN DÉVELOPPANT. Jamais ...g6 tout de suite ici.", {
                "g6": "...g6 ?? tout de suite perd une TOUR : Dxe5+ ! fourchette sur ton roi et ta tour h8 ! D'abord ...Cc6 pour protéger e5, le g6 viendra après.",
                "Nf6": "...Cf6 ?? ne protège pas e5 : Dxe5+ ! gobe ton pion central avec échec. Défends e5 d'abord : ...Cc6 !",
            }),
            ("Bc4", None),
            ("g6", "Maintenant oui : tu chasses la dame en préparant la maison du fou g7.", {
                "Nf6": "STOP ! ...Cf6 ?? laisse Dxf7 ÉCHEC ET MAT — le mat du berger, le vrai ! Chasse d'abord la dame avec ...g6, le cavalier viendra juste après.",
            }),
            ("Qf3", None),
            ("Nf6", "Elle revise f7 ? Tu défends f7 EN DÉVELOPPANT encore. Tu gagnes du temps à chaque coup."),
            ("Ne2", None),
            ("Bg7", "Le fou est superbe sur la grande diagonale."),
            ("Nbc3", None),
            ("d6", "Tu solidifies e5 et tu ouvres la porte au fou c8."),
            ("d3", None),
            ("O-O", "Roi à l'abri. Compte les pièces développées : toi 3 + roque, eux... une dame qui a perdu son temps ! 🎯"),
            ("O-O", None),
            ("Nd4", "Le saut royal ! Tu attaques sa dame pour la TROISIÈME fois — et ton cavalier lorgne aussi c2. Elle n'a jamais eu une seconde de repos."),
            ("Nxd4", None),
            ("exd4", "Reprends tranquillement : ton pion d4 chasse maintenant son cavalier c3 — ENCORE un temps gagné ! Son attaque éclair s'est transformée en leçon de développement. 🎓"),
        ],
        variations=[
            dict(at=4, name="Dame en f3 (3.Df3)", moves=[
                ("Qf3", None),
                ("Nf6", "Elle vise encore f7 ? Ton cavalier bloque le chemin EN se développant."),
                ("Bc4", None),
                ("g6", "Tu prépares la maison du fou : f7 est gardé par ton roi et bloqué par Cf6."),
                ("Ne2", None),
                ("Bg7", "Le fou rayonne sur la grande diagonale."),
                ("Nbc3", None),
                ("d6", "Tu solidifies e5 et libères ton fou c8."),
                ("d3", None),
                ("O-O", "Même punition que dans la ligne principale : tu es développé, sa dame a perdu son temps !"),
                ("O-O", None),
                ("Nd4", "Le saut royal, comme dans la ligne principale : ton cavalier attaque sa dame ENCORE une fois, et il lorgne c2 aussi !"),
                ("Nxd4", None),
                ("exd4", "Reprends : ton pion d4 chasse maintenant son cavalier c3 — encore un temps gagné ! Sa dame baladeuse aura coûté la partie en développement. 🎓"),
            ]),
        ],
    ),
    dict(
        id="italienne-noirs", side="b", emoji="🎯",
        title="Contrer l'Italienne",
        desc="Face à 3.Fc4 : développe-toi, puis frappe au centre avec ...d5 au bon moment !",
        moves=[
            ("e4", None),
            ("e5", "Le centre, symétrique et solide."),
            ("Nf3", None),
            ("Nc6", "Tu défends e5 en développant."),
            ("Bc4", None),
            ("Bc5", "Ton fou prend la même belle diagonale que le sien."),
            ("c3", None),
            ("Nf6", "Tu contre-attaques e4 : pas le temps pour lui de tout faire."),
            ("d4", None),
            ("exd4", "Il pousse ? Tu prends. Ne laisse jamais un grand centre gratuit."),
            ("cxd4", None),
            ("Bb4+", "Échec intermédiaire ! C'est LE coup à connaître : tu gagnes un temps précieux."),
            ("Bd2", None),
            ("Bxd2+", "Tu échanges et il doit reprendre : encore un temps pour toi."),
            ("Nbxd2", None),
            ("d5", "Le coup libérateur ! Tu frappes le centre blanc avant qu'il s'installe."),
            ("exd5", None),
            ("Nxd5", "Égalité parfaite : ton cavalier trône au centre et toutes tes pièces respirent. 💪"),
        ],
        variations=[
            dict(at=6, name="L'attaque hâtive 4.Cg5 ??", moves=[
                ("Ng5", None),
                ("Qxg5", "Il rêve de croquer f7... mais regarde : RIEN ne défend son cavalier, et ta dame le mange tout cru ! (Ça ne marchait que si ton cavalier était en f6.)"),
                ("Bxf7+", None),
                ("Kxf7", "Prends aussi le fou ! Ton roi devra remarcher un peu, mais compte : DEUX pièces de plus, et son attaque n'existe plus. Partie gagnée. 😋"),
            ]),
            dict(at=6, name="Gambit Evans (4.b4)", moves=[
                ("b4", None),
                ("Bb6", "Le gambit Evans ! Refuse poliment le cadeau : recule, et son pion b4 deviendra une faiblesse.", {
                    "Bxb4": "Prendre, c'est accepter SON gambit : après c3 puis d4, ses pièces sortent à toute vitesse — c'est exactement ce qu'il espère. Refuse poliment : recule le fou en b6 !",
                    "Nxb4": "Le pion b4 est un appât ! Après c3 ton cavalier doit fuir, et il construit son grand centre avec d4 en gagnant du temps. Recule plutôt le fou en b6.",
                }),
                ("a4", None),
                ("a6", "Tu donnes de l'air à ton fou : pas question de le laisser se faire piéger par a5. Et toujours pas touche au pion b4 : c'est un appât !", {
                    "Nxb4": "STOP, b4 est empoisonné ! Après ...Cxb4 ? vient a5 ! et ton fou est coincé : sa case a7 est bouchée par ton propre pion ! Puis c3 chasse ton cavalier et tout s'écroule. Joue d'abord a6 pour ouvrir la sortie a7.",
                }),
                ("a5", None),
                ("Ba7", "À l'abri ! Lui pousse des pions, toi tu vas développer des pièces."),
                ("b5", None),
                ("axb5", "Tu ouvres la colonne a... pour TA tour a8 !"),
                ("Bxb5", None),
                ("Nf6", "Développe en attaquant e4 : qui a gagné du temps dans l'histoire ? Toi. 😎"),
                ("Nc3", None),
                ("O-O", "Roi à l'abri ! Et regarde ta tour a8 : la colonne ouverte est à TOI — cadeau de son gambit."),
                ("O-O", None),
                ("d6", "Solidifie e5 et libère ton fou c8. Bilan de l'Evans : lui a éparpillé ses pions, toi tu as la colonne a et un jeu superbe. 🏆"),
            ]),
        ],
    ),
    dict(
        id="espagnole-noirs", side="b", emoji="🇪🇸",
        title="Contrer l'Espagnole",
        desc="Face à 3.Fb5 : la recette classique ...a6, ...b5, ...d6 — solide depuis 150 ans !",
        moves=[
            ("e4", None),
            ("e5", "On commence comme d'habitude."),
            ("Nf3", None),
            ("Nc6", "Défense + développement."),
            ("Bb5", None),
            ("a6", "La question au fou : il doit décider tout de suite."),
            ("Ba4", None),
            ("Nf6", "Tu développes en attaquant e4."),
            ("O-O", None),
            ("Be7", "Tranquille : ton roque arrive, tout est protégé."),
            ("Re1", None),
            ("b5", "Maintenant qu'il défend e4, tu repousses le fou pour de bon."),
            ("Bb3", None),
            ("d6", "Tu bétonnes e5 et tu libères ton fou c8."),
            ("c3", None),
            ("O-O", "Roi à l'abri : tu as tout neutralisé, la partie est égale."),
            ("h3", None),
            ("Na5", "Le plan classique : tu chasses le fameux fou espagnol de sa diagonale !"),
            ("Bc2", None),
            ("c5", "Et tu gagnes de l'espace à l'aile dame. À toi de jouer ! 🚀"),
        ],
        variations=[
            dict(at=6, name="Variante d'échange (4.Fxc6)", moves=[
                ("Bxc6", None),
                ("dxc6", "Reprends avec le pion d : tu ouvres la diagonale de ton fou c8 et tu gardes la paire de fous."),
                ("O-O", None),
                ("f6", "Béton : e5 est solidement défendu, ton mur de pions tient."),
                ("d4", None),
                ("exd4", "Il ouvre le centre ? Prends, tout est calculé."),
                ("Nxd4", None),
                ("c5", "Tu chasses le cavalier en gagnant de l'espace."),
                ("Nb3", None),
                ("Qxd1", "Échange les dames ! Sans dames, son petit avantage s'évapore... et tes deux fous brilleront."),
                ("Rxd1", None),
                ("Bd7", "Développe tranquillement : la paire de fous est ta force pour toute la partie. 🔱"),
            ]),
        ],
    ),
    dict(
        id="ecossaise-noirs", side="b", emoji="🏴",
        title="Contrer l'Écossaise",
        desc="3.d4 tout de suite : réponds 4...Fc5 et harcèle son cavalier d4 — gare à lui s'il prend en c6 !",
        moves=[
            ("e4", None),
            ("e5", "Début habituel."),
            ("Nf3", None),
            ("Nc6", "Défense + développement, comme toujours."),
            ("d4", None),
            ("exd4", "Prends : ne le laisse pas s'installer gratuitement au centre.", {
                "Nxd4": "Pas avec le cavalier ! Après Cxd4 exd4 Dxd4, sa dame trône au centre SANS pouvoir être chassée : ton cavalier c6 n'existe plus. Prends avec le pion.",
            }),
            ("Nxd4", None),
            ("Bc5", "LE coup : tu développes en visant son cavalier d4... et la case f2 derrière !"),
            ("Be3", None),
            ("Qf6", "Encore d4 ! Et ta dame lorgne f2 : il doit rester très prudent."),
            ("c3", None),
            ("Nge7", "Développe SANS bloquer ta dame : e7 est la bonne case ici."),
            ("Bc4", None),
            ("Ne5", "Ton cavalier saute au centre en attaquant son fou : l'initiative est pour toi."),
            ("Be2", None),
            ("Qg6", "Double attaque : le pion g2 ET le pion e4 ! Il doit encore défendre."),
            ("O-O", None),
            ("d6", "Consolide ton superbe cavalier e5. Regarde l'échiquier : c'est TOI qui attaques. ⚡"),
        ],
        variations=[
            dict(at=8, name="La prise 5.Cxc6", moves=[
                ("Nxc6", None),
                ("Qf6", "Surprise : ne reprends pas tout de suite ! Tu menaces Dxf2 ÉCHEC ET MAT (ton fou c5 soutient f2). Il doit parer."),
                ("Qd2", None),
                ("dxc6", "MAINTENANT tu reprends, avec le pion d : fou c8 libéré, paire de fous, développement de rêve. 🌟"),
            ]),
        ],
    ),
    dict(
        id="gambit-roi-noirs", side="b", emoji="👑",
        title="Contrer le gambit du roi",
        desc="2.f4 : les jeunes attaquants adorent ! Refuse poliment avec 2...Fc5 : son roi ne pourra plus roquer tranquille.",
        moves=[
            ("e4", None),
            ("e5", "Début habituel."),
            ("f4", None),
            ("Bc5", "Le refus malin ! Ton fou vise g1 : impossible pour lui de roquer. Et surtout, ne prends PAS f4 tout de suite.", {
                "exf4": "Accepter, c'est entrer dans SA jungle de pièges, qu'il connaît mieux que toi. Le refus malin ...Fc5 ! vise g1 : plus de roque pour lui — et s'il gobe e5 ?? ...Dh4+ fait exploser sa position.",
            }),
            ("Nf3", None),
            ("d6", "Solidifie e5 tranquillement : son f4 ne sert à rien pour l'instant."),
            ("Nc3", None),
            ("Nf6", "Développe en visant e4."),
            ("Bc4", None),
            ("Nc6", "Encore une pièce : tu joues aux échecs, lui attend son attaque."),
            ("d3", None),
            ("Bg4", "Cloue son cavalier : c'est lui le défenseur de son roi resté au centre."),
            ("h3", None),
            ("Bxf3", "Échange : son roi perd son meilleur garde du corps."),
            ("Qxf3", None),
            ("exf4", "MAINTENANT tu prends f4 : au bon moment, pas avant !"),
            ("Bxf4", None),
            ("Nd4", "Fourchette en vue ! Tu attaques sa dame ET tu vises c2 : l'initiative est pour toi. ⚡"),
        ],
        variations=[
            dict(at=4, name="La gourmandise 3.fxe5 ??", moves=[
                ("fxe5", None),
                ("Qh4+", "ÉCHEC ! Voilà pourquoi il ne fallait pas prendre : son roi n'a plus le pion f pour se cacher."),
                ("g3", None),
                ("Qxe4+", "Tu manges e4 avec encore échec : sa partie s'écroule."),
                ("Qe2", None),
                ("Qxh1", "Et tu gagnes la tour h1 ! Une tour entière pour un pion : merci le gambit. 🎁"),
            ]),
        ],
    ),
    dict(
        id="vienne-noirs", side="b", emoji="🎻",
        title="Contrer la Vienne",
        desc="2.Cc3 puis souvent f4 : retiens LE coup magique ...d5 au bon moment !",
        moves=[
            ("e4", None),
            ("e5", "Comme toujours."),
            ("Nc3", None),
            ("Nf6", "La Vienne ! Développe normalement... et prépare la surprise si f4 arrive."),
            ("f4", None),
            ("d5", "LE coup magique contre le gambit viennois : frappe au centre ! (Surtout pas ...exf4 ?)", {
                "exf4": "C'est LE piège viennois ! Après ...exf4 ? e5 ! ton cavalier f6 doit fuir et son attaque déferle toute seule. Réponds au centre : ...d5 !",
            }),
            ("fxe5", None),
            ("Nxe4", "Ton cavalier s'installe au centre. S'il l'échange avec Cxe4, tu reprends ...dxe4 et tu es très bien."),
            ("Nf3", None),
            ("Be7", "Tranquille : développement d'abord, ton cavalier e4 est costaud."),
            ("d4", None),
            ("O-O", "Roi à l'abri pendant que le sien est encore tout nu au centre."),
            ("Bd3", None),
            ("Nxc3", "Échange au bon moment : tu lui laisses des pions doublés en souvenir."),
            ("bxc3", None),
            ("c5", "Attaque son centre : ses pions abîmés vont souffrir toute la partie. 💪"),
        ],
        variations=[
            dict(at=4, name="Le fou d'abord (3.Fc4)", moves=[
                ("Bc4", None),
                ("Nc6", "Développe simplement : pas de précipitation."),
                ("d3", None),
                ("Bc5", "Ton fou prend sa belle diagonale, comme dans l'Italienne."),
                ("f4", None),
                ("d6", "Le voilà, son f4 ! Réponds solide : e5 est bien gardé, ne lui ouvre rien."),
                ("Nf3", None),
                ("Bg4", "Cloue son cavalier : son attaque est gelée sur place. 🧊"),
            ]),
        ],
    ),
    dict(
        id="anti-danois", side="b", emoji="🇩🇰",
        title="Contrer le gambit danois : 3...d5 !",
        desc="2.d4 et 3.c3 : il offre des pions pour attaquer vite. Qu'il soit simple (4.Cxc3) ou double (4.Fc4), la parade ...d5 règle tout !",
        moves=[
            ("e4", None),
            ("e5", "On commence normalement."),
            ("d4", None),
            ("exd4", "Il offre un pion : prends-le sans peur."),
            ("c3", None),
            ("d5", "LE coup anti-gambit : tu rends le pion tout de suite pour casser son centre AVANT que son attaque commence.", {
                "dxc3": "Tout gober ? C'est possible — tu as un module entier pour ça (🍬) ! — mais SEULEMENT en connaissant la suite par cœur. Ici on apprend la parade simple et solide : ...d5 !",
            }),
            ("exd5", None),
            ("Qxd5", "Ta dame est tranquille ici : son cavalier ne peut pas venir en c3... son propre pion occupe la case !"),
            ("cxd4", None),
            ("Nc6", "Développement avec pression sur d4."),
            ("Nf3", None),
            ("Bg4", "Tu cloues le défenseur de d4 : la pression monte."),
            ("Be2", None),
            ("Bb4+", "Échec intermédiaire : tu gênes son développement."),
            ("Nc3", None),
            ("Bxf3", "Tu élimines le défenseur de d4..."),
            ("Bxf3", None),
            ("Qc4", "Le coup de Capablanca ! Tu attaques d4 et tu proposes l'échange des dames : sans dames, son gambit ne vaut plus rien. 🧊"),
        ],
    ),
    dict(
        id="anti-danois-accepte", side="b", emoji="🍬",
        title="Gambit danois : si tu gobes tout...",
        desc="Tu PEUX accepter les deux pions — mais seulement si tu connais cette suite par cœur : ...d5 puis ...Fb4+ !",
        moves=[
            ("e4", None),
            ("e5", "Début classique."),
            ("d4", None),
            ("exd4", "Premier pion : merci !"),
            ("c3", None),
            ("dxc3", "Deuxième pion offert... d'accord, mais reste concentré.", {
                "d5": "...d5 est l'AUTRE chemin : le refus malin, ton module 🇩🇰 ! Ici on s'entraîne à tout gober : ...dxc3, en récitant la suite par cœur.",
            }),
            ("Bc4", None),
            ("cxb2", "Troisième ! Tu peux gober SI tu connais la suite. Sinon, rejoue la ligne 3...d5."),
            ("Bxb2", None),
            ("d5", "Le coup d'or : tu rends UN pion pour couper ses deux fous et libérer ton jeu.", {
                "Nf6": "Développer « normalement » ici = DANGER : e5 ! chasse ton cavalier, et ses deux fous + sa dame foncent sur f7 et g7. Le coup d'or : ...d5 ! rends un pion pour couper leurs diagonales.",
            }),
            ("Bxd5", None),
            ("Nf6", "Tu développes en attaquant son fou. Attention, son Fxf7+ arrive... mais c'est prévu !"),
            ("Bxf7+", None),
            ("Kxf7", "Oui, prends ! Il va capturer ta dame... laisse-le faire, le coup suivant est magique."),
            ("Qxd8", None),
            ("Bb4+", "ÉCHEC ! Voilà l'astuce : sa dame est obligée de revenir s'interposer..."),
            ("Qd2", None),
            ("Bxd2+", "...et tu la captures ! Dame contre dame : échange équitable, et son attaque a disparu."),
            ("Nxd2", None),
            ("Re8", "Compte : matériel égal, plus de dames, et ta tour attaque déjà e4. Son gambit n'a servi à rien — à toi de jouer ! 🔥"),
        ],
    ),
    dict(
        id="gambit-dame-noirs", side="b", emoji="🗿",
        title="Contrer le Gambit Dame",
        desc="Face à 1.d4 et 2.c4 : le Gambit Dame refusé, solide comme un roc.",
        moves=[
            ("d4", None),
            ("d5", "Tu prends le centre toi aussi : pas peur de 1.d4 !"),
            ("c4", None),
            ("e6", "Tu REFUSES le gambit : ton pion d5 sera toujours protégé.", {
                "dxc4": "Prendre c4, c'est lâcher le centre — et il récupère TOUJOURS son pion (e4 puis Fxc4, ou même Da4+ !). Reste roc : ...e6 protège d5 pour toujours.",
            }),
            ("Nc3", None),
            ("Nf6", "Développement naturel."),
            ("Bg5", None),
            ("Be7", "Tu pares le clouage tranquillement."),
            ("e3", None),
            ("O-O", "Roi en sécurité d'abord."),
            ("Nf3", None),
            ("Nbd7", "Ce cavalier soutient son frère et prépare ...c5 ou ...e5 plus tard."),
            ("Rc1", None),
            ("c6", "Béton ! d5 est protégé 3 fois. Ton plan : ...dxc4 puis ...b5 ou ...c5 au bon moment."),
        ],
        variations=[
            dict(at=6, name="Variante d'échange (4.cxd5)", moves=[
                ("cxd5", None),
                ("exd5", "Reprends avec le pion e : ton fou c8 est enfin libre de sortir !"),
                ("Bg5", None),
                ("Be7", "Tu pares le clouage, comme dans la ligne principale."),
                ("e3", None),
                ("O-O", "Roi à l'abri d'abord."),
                ("Bd3", None),
                ("c6", "Béton sur d5 : ta structure est ultra-solide."),
                ("Nf3", None),
                ("Nbd7", "Développement terminé. Ton plan : la tour en e8 et le cavalier vers e4 ! 🐴"),
            ]),
        ],
    ),
    dict(
        id="anti-catalane", side="b", emoji="🐱",
        title="Contrer la Catalane",
        desc="1.d4, 2.c4 puis g3 : son fou veut régner sur la grande diagonale. Construis un mur... puis réponds œil pour œil !",
        moves=[
            ("d4", None),
            ("d5", "Le centre, comme d'habitude."),
            ("c4", None),
            ("e6", "Tu protèges d5 : même début que contre le Gambit Dame."),
            ("Nf3", None),
            ("Nf6", "Développement naturel."),
            ("g3", None),
            ("Be7", "Voilà la Catalane ! Pas de panique : ne prends pas c4, développe-toi tranquillement.", {
                "dxc4": "Contre la Catalane, prendre c4 est risqué : son fou arrive en g2 PILE sur la diagonale pour récupérer le pion avec intérêts (Ce5, Da4+...). Continue ton développement béton.",
            }),
            ("Bg2", None),
            ("O-O", "Roi à l'abri pendant qu'il prépare son grand fou."),
            ("O-O", None),
            ("Nbd7", "Ce cavalier prépare le plan ...c6 puis ...b6."),
            ("Qc2", None),
            ("c6", "Le mur ! Son fou g2 mord dans du béton : d5 est verrouillé."),
            ("b3", None),
            ("b6", "Tu prépares la réponse du berger à la bergère..."),
            ("Bb2", None),
            ("Bb7", "Œil pour œil : TON fou prend la même grande diagonale que le sien ! Plan : ...c5 ou ...Ce4 au bon moment. 😼"),
        ],
        variations=[
            dict(at=8, name="L'échange 5.cxd5", moves=[
                ("cxd5", None),
                ("exd5", "Reprends avec le pion e : ton fou c8 est enfin libre !"),
                ("Bg2", None),
                ("O-O", "Roi en sécurité d'abord, toujours."),
                ("O-O", None),
                ("c6", "Béton sur d5 : son fou g2 ne mange que du granit."),
                ("Nc3", None),
                ("Nbd7", "Développe : ce cavalier visera e4 ou b6 plus tard."),
                ("Qc2", None),
                ("Re8", "Ta tour prend la colonne ouverte : position égale et facile à jouer. 💪"),
            ]),
        ],
    ),
    dict(
        id="anti-londres", side="b", emoji="🎡",
        title="Contrer le système de Londres",
        desc="1.d4 et 2.Ff4 : TRÈS joué chez les jeunes. Attaque b2, le talon d'Achille de la Londres !",
        moves=[
            ("d4", None),
            ("d5", "Tu prends le centre."),
            ("Bf4", None),
            ("c5", "Tu attaques d4 tout de suite : pas question de le laisser s'installer."),
            ("e3", None),
            ("Nc6", "Encore de la pression sur d4."),
            ("c3", None),
            ("Qb6", "LE coup clé : le fou f4 est parti... b2 n'est plus défendu !"),
            ("Qb3", None),
            ("c4", "Tu repousses sa dame en gagnant de l'espace.", {
                "Qxb3": "N'échange pas ! Après axb3, SA tour a1 s'ouvre une autoroute sur la colonne a. Pousse ...c4 ! et sa dame doit encore reculer, toute seule.",
            }),
            ("Qc2", None),
            ("Bf5", "Encore la dame ! Elle n'a plus que la case c1, toute triste."),
            ("Qc1", None),
            ("e6", "Regarde sa dame à c1 et son fou bloqué... Toi tu as l'espace et l'initiative ! 🔥"),
        ],
        variations=[
            dict(at=4, name="La prise 3.dxc5", moves=[
                ("dxc5", None),
                ("e6", "Il a gobé le pion ? Pas de panique : ton FOU va le reprendre. Et s'il essaie de le garder avec b4 ?, joue ...a5 ! et sa chaîne s'écroule."),
                ("e3", None),
                ("Bxc5", "Tu reprends en DÉVELOPPANT : le fou est superbe ici. Et compte le centre : son pion d4 a disparu, ton pion d5 règne tout seul !"),
                ("Nf3", None),
                ("Nc6", "Développement naturel : tu as un temps d'avance et le centre."),
                ("Bd3", None),
                ("Nf6", "Trois pièces dehors, le centre pour toi... sa prise dxc5 t'a rendu service ! Roque, puis prépare ...e5 pour tout ouvrir. 😏"),
            ]),
        ],
    ),
    dict(
        id="anglaise-noirs", side="b", emoji="🇬🇧",
        title="Contrer l'Anglaise",
        desc="1.c4 : ne te laisse pas dérouter. Joue ...e5 : c'est une Sicilienne à l'envers, et le centre est pour toi !",
        moves=[
            ("c4", None),
            ("e5", "Contre l'Anglaise, joue ce que tu connais : le centre ! Tu joues une Sicilienne... à l'envers."),
            ("Nc3", None),
            ("Nf6", "Développement naturel."),
            ("Nf3", None),
            ("Nc6", "Encore une pièce vers le centre."),
            ("g3", None),
            ("d5", "La poussée libératrice : c'est TOI qui joues au centre, pas lui."),
            ("cxd5", None),
            ("Nxd5", "Reprends avec le cavalier : il trône au milieu."),
            ("Bg2", None),
            ("Nb6", "Petit recul malin : tu sors de la diagonale de son fou g2, qui tape dans le vide."),
            ("O-O", None),
            ("Be7", "Développe tranquillement : ta position est confortable."),
            ("d3", None),
            ("O-O", "Roi à l'abri : tu as fait jeu égal au centre, la partie commence bien. ✨"),
        ],
    ),
]


def process_moves(board, moves, ctx):
    """Valide une séquence de coups SAN sur `board` et renvoie les dicts pour le JSON.
    Une entrée peut avoir un 3e élément {san_erreur: explication} : les pièges
    typiques tentés À LA PLACE de ce coup, expliqués au moment de l'erreur."""
    out = []
    for entry in moves:
        san, comment = entry[0], entry[1]
        traps_in = entry[2] if len(entry) > 2 else {}
        try:
            move = board.parse_san(san)
        except ValueError as e:
            raise SystemExit(f"[{ctx}] coup illégal {san}: {e}")
        traps = []
        for tsan, ttext in traps_in.items():
            try:
                tmove = board.parse_san(tsan)
            except ValueError as e:
                raise SystemExit(f"[{ctx}] piège illégal {tsan}: {e}")
            assert tmove != move, f"[{ctx}] le piège {tsan} est identique au bon coup"
            traps.append(dict(
                san=tsan,
                from_=chess.square_name(tmove.from_square),
                to=chess.square_name(tmove.to_square),
                text=ttext,
            ))
        if board.is_en_passant(move):
            raise SystemExit(f"[{ctx}] {san} est une prise en passant (non gérée)")
        castle = None
        if board.is_kingside_castling(move):
            castle = "K"
        elif board.is_queenside_castling(move):
            castle = "Q"
        color = "w" if board.turn == chess.WHITE else "b"
        d = dict(
            san=san,
            from_=chess.square_name(move.from_square),
            to=chess.square_name(move.to_square),
            castle=castle,
            color=color,
            comment=comment,
        )
        if traps:
            d["traps"] = traps
        out.append(d)
        board.push(move)
        if san.endswith("#"):
            assert board.is_checkmate(), f"[{ctx}] {san} n'est pas mat !"
    return out


# Ordre d'affichage (du plus classique au plus original, par couleur) et niveau de chaque module
ORDER_LEVELS = {
    # ------- Blancs -------
    "italienne-blancs":     "debutant",
    "anti-scandinave":      "debutant",
    "anti-francaise":       "debutant",
    "anti-caro":            "inter",
    "anti-sicilienne":      "inter",
    "anti-pirc":            "inter",
    "piege-legal":          "debutant",
    "fried-liver":          "avance",
    "morra":                "avance",
    # ------- Noirs -------
    "anti-berger":          "debutant",
    "italienne-noirs":      "debutant",
    "espagnole-noirs":      "inter",
    "ecossaise-noirs":      "inter",
    "gambit-dame-noirs":    "inter",
    "anti-londres":         "inter",
    "vienne-noirs":         "inter",
    "gambit-roi-noirs":     "inter",
    "anti-danois":          "inter",
    "anti-danois-accepte":  "avance",
    "anglaise-noirs":       "avance",
    "anti-catalane":        "avance",
}


def main():
    ids = [l["id"] for l in LINES]
    assert sorted(ids) == sorted(ORDER_LEVELS), \
        f"ORDER_LEVELS désynchronisé : {set(ids) ^ set(ORDER_LEVELS)}"
    rank = list(ORDER_LEVELS)
    out = []
    for line in sorted(LINES, key=lambda l: rank.index(l["id"])):
        board = chess.Board()
        moves_out = process_moves(board, line["moves"], line["id"])
        # le dernier coup doit être joué par l'enfant (= la couleur de la ligne)
        assert moves_out[-1]["color"] == line["side"], f"[{line['id']}] dernier coup pas au trait de l'enfant"
        vars_out = []
        for var in line.get("variations", []):
            at = var["at"]
            # le point de divergence doit être un coup de l'adversaire, différent du coup principal
            assert moves_out[at]["color"] != line["side"], f"[{line['id']}/{var['name']}] 'at' ne pointe pas un coup adverse"
            assert var["moves"][0][0] != moves_out[at]["san"], f"[{line['id']}/{var['name']}] même coup que la ligne principale"
            vboard = chess.Board()
            for entry in line["moves"][:at]:
                vboard.push_san(entry[0])
            vmoves = process_moves(vboard, var["moves"], f"{line['id']}/{var['name']}")
            assert vmoves[0]["color"] != line["side"], f"[{line['id']}/{var['name']}] doit commencer par un coup adverse"
            assert vmoves[-1]["color"] == line["side"], f"[{line['id']}/{var['name']}] dernier coup pas au trait de l'enfant"
            vars_out.append(dict(at=at, name=var["name"], moves=vmoves))
        out.append(dict(
            id=line["id"], side=line["side"], emoji=line["emoji"], level=ORDER_LEVELS[line["id"]],
            title=line["title"], desc=line["desc"], moves=moves_out, variations=vars_out,
        ))
        print(f"OK  {line['id']:24s} {len(moves_out):2d} demi-coups, {len(vars_out)} variante(s)")
    with open("lines.json", "w") as f:
        json.dump(out, f, ensure_ascii=False)
    print(f"\n{len(out)} lignes validées -> lines.json")


if __name__ == "__main__":
    main()
