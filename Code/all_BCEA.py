import networkx as nx
import itertools
from collections import Counter
import random
rng = random.Random(42)

############################################################################
# Datei mit allen 4 BCEA Arten, mit zunehmend strikterer Kandidatenauswahl #
############################################################################

# BCEA1:
# random y'

# BCEA2:
# 1. y' in BMG.successors(x)
# 2. y' random

# BCEA3: Unterscheidet zwischen weak und strict
# Auswahl für weak:
# 1. reziproger best match (x->z & z->x)
# 2. asymmetrischer best match (x->z)
# 3. asymmetrischer best match (z->x)
# 4. irgendein y' != y
#
# Auswahl für strict:
# Wenn beidseitige Verbesserung beim P-Knoten:
# Verbindung mit safe pair (Paar an Kandidaten, welches im BMG keine Verbindung hat)

# BCEA4: Multilayered approach (nur für weak!!)

def BCEA1(G: nx.DiGraph) -> nx.DiGraph:
    # ASSERTIONS
    ## assert colored digraph
    assert isinstance(G, nx.DiGraph)
    assert all("color" in G.nodes[v] for v in G.nodes)

    ## assert properly colored (no edges between same color)
    colors = nx.get_node_attributes(G,"color")
    for u,v in G.edges():
        assert colors[u] != colors[v]

    ## assert sicor in hub
    ### find all sicors
    color_counts = Counter(colors.values())
    sicor = [v for v,c in colors.items() if color_counts[c]==1]
    ### assert in-hub-ness
    for s in sicor:
        for u in G.nodes():
            if colors[u] != colors[s]:
                assert G.has_edge(u,s)

    # BIC-CHERRY
    ## initialize and root network digraph
    N = nx.DiGraph()
    N.add_node("rho")

    ## extract differently colored leafs from G
    cherrylist = []
    for key1, value1 in colors.items():
        for key2, value2 in colors.items():
            if key1 < key2 and value1 != value2:
                cherrylist.append(frozenset({str(key1), str(key2)}))
    ## add leaves and parent nodes to get uglycherry
    p_nodes = dict()
    for pair in cherrylist:
        x,y = sorted(pair)
        p_name = f"p_{x}_{y}"
        p_nodes[pair] = p_name
        N.add_edge("rho",p_name)
        N.add_edge(p_name, x)
        N.add_edge(p_name, y)
    ## add back color property to nodes
    for node, color in colors.items():
        N.nodes[str(node)]["color"] = color

    # EXTENSION
    ## find all cherrys x,y in N that don't have an edge x,y or y,x in G
    ### find *any* (optimize here? random for now) another x' or y' that has an edge in G
    ### introduce q_xy' or q_yx' below the corresponding p_xy or p_yx
    for pair, p_name in p_nodes.items():
        x,y = sorted(pair)
        if not G.has_edge(x,y):
            y_prime = rng.choice([str(v) for v in G.nodes() if v != y and colors[v]==colors[y]])
            ## insert q_xy' below p_xy
            q_name = f"q_{x}_{y}_{y_prime}"
            N.add_edge(p_name,q_name)
            N.add_edge(q_name, x)
            N.add_edge(q_name, y_prime)
        if not G.has_edge(y,x):
            x_prime = rng.choice([str(v) for v in G.nodes() if v != x and colors[v]==colors[x]])
            ## insert q_yx'' below p_xy
            q_name = f"q_{y}_{x}_{x_prime}"
            N.add_edge(p_name, q_name)
            N.add_edge(q_name, y)
            N.add_edge(q_name, x_prime)

    # return network
    return N


def BCEA2(G: nx.DiGraph) -> nx.DiGraph:
    # ASSERTIONS
    ## assert colored digraph
    assert isinstance(G, nx.DiGraph)
    assert all("color" in G.nodes[v] for v in G.nodes)

    ## assert properly colored (no edges between same color)
    colors = nx.get_node_attributes(G,"color")
    for u,v in G.edges():
        assert colors[u] != colors[v]

    ## assert sicor in hub
    ### find all sicors
    color_counts = Counter(colors.values())
    sicor = [v for v,c in colors.items() if color_counts[c]==1]
    ### assert in-hub-ness
    for s in sicor:
        for u in G.nodes():
            if colors[u] != colors[s]:
                assert G.has_edge(u,s)

    # BIC-CHERRY
    ## initialize and root network digraph
    N = nx.DiGraph()
    N.add_node("rho")

    ## extract differently colored leafs from G
    cherrylist = []
    for key1, value1 in colors.items():
        for key2, value2 in colors.items():
            if key1 < key2 and value1 != value2:
                cherrylist.append(frozenset({key1, key2}))
    ## add leaves and parent nodes to get uglycherry
    p_nodes = dict()
    for pair in cherrylist:
        x,y = sorted(pair)
        p_name = f"p_{x}_{y}"
        p_nodes[pair] = p_name
        N.add_edge("rho",p_name)
        N.add_edge(p_name, x)
        N.add_edge(p_name, y)
    ## add back color property to nodes
    for node, color in colors.items():
        N.nodes[node]["color"] = color

    # EXTENSION
    ## find all cherrys x,y in N that don't have an edge x,y or y,x in G
    ### find *any* (optimize here? random for now) another x' or y' that has an edge in G
    ### introduce q_xy' or q_yx' below the corresponding p_xy or p_yx
    for pair, p_name in p_nodes.items():
        x,y = sorted(pair)
        if not G.has_edge(x,y):

            # statt random choice, sollte hier der successor gewählt werden, der widerum x als best match hat, sofern vorhanden

            # Alte Auswahl:
            # y_prime = rng.choice([v for v in G.successors(x) if colors[v]==colors[y]])

            # neue Auswahl:
            # 1. reziproger best match (x->z & z->x)
            # 2. asymmetrischer best match (x->z)
            # 3. asymmetrischer best match (z->x)
            # 4. irgendein y' != y
            candidates = []
            candidates = [v for v in G.successors(x) if colors[v] == colors[y]]

            if not candidates:
                candidates = [v for v in G.predecessors(x) if colors[v] == colors[y] and v != y]

            if not candidates:
                candidates = [v for v in G.nodes if colors[v] == colors[y] and v != y]

            y_prime = rng.choice(candidates)


            ## insert q_xy' below p_xy
            q_name = f"q_{x}_{y}_{y_prime}"
            N.add_edge(p_name,q_name)
            N.add_edge(q_name, x)
            N.add_edge(q_name, y_prime)

            # soll man die Edge zwischen p_name und x löschen? diese ist shortcut

            N.remove_edge(p_name,x)

        if not G.has_edge(y,x):
            
            # statt random choice, sollte hier der successor gewählt werden, der widerum x als best match hat

            # Alte Auswahl
            # x_prime = rng.choice([v for v in G.successors(y) if colors[v]==colors[x]])

            # neue Auswahl:
            # 1. reziproger best match (x->z & z->x)
            # 2. asymmetrischer best match (x->z)
            # 3. asymmetrischer best match (z->x)
            # 4. irgendein y' != y


            candidates = []
            candidates = [v for v in G.successors(y) if colors[v] == colors[x]]

            if not candidates:
                candidates = [v for v in G.predecessors(y) if colors[v] == colors[x] and v != x]

            if not candidates:
                candidates = [v for v in G.nodes if colors[v] == colors[x] and v != x]

            x_prime = rng.choice(candidates)


            ## insert q_yx'' below p_xy
            q_name = f"q_{y}_{x}_{x_prime}"
            N.add_edge(p_name, q_name)
            N.add_edge(q_name, y)
            N.add_edge(q_name, x_prime)

            # soll man die Edge zwischen p_name und y löschen? diese ist shortcut

            N.remove_edge(p_name,y)
                          
    # return network
    return N

def find_candidate(BMG: nx.DiGraph, x, y, mode: str = "weak"):
    """
    Sucht einen Ersatzkandidaten fuer y (gleiche Farbe wie y), der x's
    fehlenden Match zu y ersetzt.

    mode="weak": Da per schwacher Definition jede Q-Node einen reziproken
    best match einbaut, sollte y' (bzw. z) einen best match zu x aufweisen.
    Gibt es kein solches Blatt, ist der eingegebene BMG mit der schwachen
    best match Definition nicht mit einem Two-layered BCN darstellbar.

    mode="strong": y' muss in diesem Fall nicht x als best match haben, da
    der Q-Knoten nicht unbedingt einen symmetrischen best match erzeugt.
    Der best-match von y' zu x wird durch die Korrektur bei y' selbst auf
    jeden Fall entfernt.
    """
    if mode == "weak":
        candidates = [v for v in BMG.successors(x) if BMG.nodes[v]["color"] == BMG.nodes[y]["color"] and BMG.has_edge(v, x)]
        if candidates:
            return rng.choice(candidates)
        # else:
        #     print("Warning from BCEA: The resulting BMG might differ von the original BMG -> try the multilayered BCEA")

    candidates = [v for v in BMG.successors(x) if BMG.nodes[v]["color"] == BMG.nodes[y]["color"]]

    if not candidates:
        candidates = [v for v in BMG.predecessors(x) if BMG.nodes[v]["color"] == BMG.nodes[y]["color"] and v != y]

    if not candidates:
        candidates = [v for v in BMG.nodes if BMG.nodes[v]["color"] == BMG.nodes[y]["color"] and v != y]

    return rng.choice(candidates)


def find_joint_candidates(BMG: nx.DiGraph, x, y):
    """
    Nur relevant fuer mode="strong", wenn ein Paar (x,y) auf BEIDEN Seiten
    korrigiert werden muss. Waehlt y' und x' gleichzeitig.
 
    Problematik: Werden zwei Blaetter y' und x' durch das einfügen von Q-Knoten
    an beiden Edges eines P-Knotens verbunden, so haben die Blaetter einen neuen
    LCA, welcher nicht in der Menge der niedrigsten LCAs enthalten ist. 
    x' und y' wären Dadurch nach der strikten Definition kein best match mehr.
    Deswegen sollen die beiden so gewählt werden, dass diese im Originalen BMG 
    bereits keine Edges zueinander haben.

 
      Stufe 1 (biologisch bevorzugt): y' aus BMG.successors(x),
               x' aus BMG.successors(y) -- echte Matches.
      Stufe 2 (mathematisch ausreichender Fallback): Alle Blaetter der
               jeweils passenden Farbe (ausser y bzw. x selbst). -- sichere
               Kombinationen allerdings ohne großer biologischer Relevanz(?)
 
    Returns
    -------
    (x_prime, y_prime) oder None, falls schon die volle Knotenmenge einer
    Seite leer ist (kann bei nur einem Blatt einer Farbe vorkommen).
    """

    color_x = BMG.nodes[x]["color"]
    color_y = BMG.nodes[y]["color"]
 
    def is_safe(xp, yp):
        return not BMG.has_edge(xp, yp) and not BMG.has_edge(yp, xp)
 
    def safe_pair(x_pool, y_pool):
        if not x_pool or not y_pool:
            return None
        safe = [(xp, yp) for xp in x_pool for yp in y_pool if is_safe(xp, yp)]
        return rng.choice(safe) if safe else None
 
    # Stufe 1: echte Matches (biologisch bevorzugt)
    x_succ = [v for v in BMG.successors(y) if BMG.nodes[v]["color"] == color_x]
    y_succ = [v for v in BMG.successors(x) if BMG.nodes[v]["color"] == color_y]
    pair = safe_pair(x_succ, y_succ)
    if pair:
        return pair
 
    # Stufe 2: volle Knotenmenge der jeweiligen Farbe
    x_all = [v for v in BMG.nodes if BMG.nodes[v]["color"] == color_x and v != x]
    y_all = [v for v in BMG.nodes if BMG.nodes[v]["color"] == color_y and v != y]
    pair = safe_pair(x_all, y_all)
    if pair:
        return pair
 
    # Kein sicheres Paar -> Bruch unvermeidbar (siehe check_criteria).
    # Bevorzugt trotzdem einen biologisch sinnvollen (Stufe-1) Kandidaten,
    # falls vorhanden.
    # print("the BMG of the BCN likely differs from the original BMG")
    if x_succ and y_succ:
        return rng.choice([(xp, yp) for xp in x_succ for yp in y_succ])
    if x_all and y_all:
        return rng.choice([(xp, yp) for xp in x_all for yp in y_all])
    
    return None


def BCEA3(G: nx.DiGraph, mode: str) -> nx.DiGraph:
    # ASSERTIONS
    assert mode in ("weak", "strong"), f"mode must be 'weak' or 'strong', got {mode!r}"
    assert isinstance(G, nx.DiGraph)
    assert all("color" in G.nodes[v] for v in G.nodes)

    colors = nx.get_node_attributes(G, "color")
    for u, v in G.edges():
        assert colors[u] != colors[v]

    ## assert sicor in hub
    color_counts = Counter(colors.values())
    sicor = [v for v, c in colors.items() if color_counts[c] == 1]
    for s in sicor:
        for u in G.nodes():
            if colors[u] != colors[s]:
                assert G.has_edge(u, s)

    # BIC-CHERRY
    N = nx.DiGraph()
    N.add_node("rho")

    cherrylist = []
    for leaf1, color1 in colors.items():
        for leaf2, color2 in colors.items():
            if leaf1 < leaf2 and color1 != color2:
                cherrylist.append(frozenset({leaf1, leaf2}))

    p_nodes = dict()
    for pair in cherrylist:
        x, y = sorted(pair)
        p_name = f"p_{x}_{y}"
        p_nodes[pair] = p_name
        N.add_edge("rho", p_name)
        N.add_edge(p_name, x)
        N.add_edge(p_name, y)

    for node, color in colors.items():
        N.nodes[node]["color"] = color

    # EXTENSION
    for pair, p_name in p_nodes.items():
        x, y = sorted(pair)
        needs_x = not G.has_edge(x, y)   # x braucht Korrektur (Ersatz fuer y)
        needs_y = not G.has_edge(y, x)   # y braucht Korrektur (Ersatz fuer x)

        y_prime = x_prime = None
        if needs_x and needs_y and mode == "strong":
            joint = find_joint_candidates(G, x, y)
            if joint is not None:
                x_prime, y_prime = joint

        if needs_x and y_prime is None:
            y_prime = find_candidate(G, x, y, mode)
        if needs_y and x_prime is None:
            x_prime = find_candidate(G, y, x, mode)

        if needs_x:
            q_name = f"q_{x}_{y}_{y_prime}"
            N.add_edge(p_name, q_name)
            N.add_edge(q_name, x)
            N.add_edge(q_name, y_prime)
            N.remove_edge(p_name, x)

        if needs_y:
            q_name = f"q_{y}_{x}_{x_prime}"
            N.add_edge(p_name, q_name)
            N.add_edge(q_name, y)
            N.add_edge(q_name, x_prime)
            N.remove_edge(p_name, y)

    return N

def _has_reciprocal_option(BMG: nx.DiGraph, node, target_color) -> bool:
    """
    Ein-Schritt-Vorschau: prueft, ob 'node' mindestens einen Kandidaten der
    Farbe target_color hat, der 'node' reziprok erwidert. Wird 'node' also
    als (nicht-reziproker) Kandidat gewaehlt, koennte seine EIGENE
    Korrektur auf der naechsten Ebene sofort reziprok abgeschlossen werden,
    statt die Kette weiter zu verlaengern.

    Könnte für weitere Ebenen umgesetzt werden, was die Lösbarkeit verbessert
    den Rechenaufwand allerdings erhöht
    """
    return any(
        BMG.nodes[v]["color"] == target_color and BMG.has_edge(v, node)
        for v in BMG.successors(node)
    )


def find_candidate(BMG: nx.DiGraph, x, y):
    """
    Sucht einen Ersatzkandidaten fuer y (gleiche Farbe wie y), der x's
    fehlenden Match zu y ersetzt.

    Da unter der WEAK-Definition jeder neu eingefuegte Knoten (Q, R, S, ...)
    strukturell einen BEIDSEITIGEN Best Match erzwingt, wird bevorzugt ein
    Kandidat gewaehlt, der x auch TATSAECHLICH als eigenen Best Match hat
    (reziprok). Gibt es keinen solchen, wird unter den verbleibenden
    Kandidaten bevorzugt einer gewaehlt, der SELBST einen reziproken
    Kandidaten haette (1-Schritt-Vorschau) -- das garantiert Aufloesung
    spaetestens eine Ebene spaeter, statt die Korrektur-Kette potenziell
    beliebig zu verlaengern, falls eine solche Wahl existiert.

    Returns
    -------
    z : Kandidat (gleiche Farbe wie y)
    reciprocal : bool -- True, wenn z tatsaechlich x als Best Match hat.
    """
    color_x = BMG.nodes[x]["color"]
    color_y = BMG.nodes[y]["color"]

    reciprocal_candidates = [
        v for v in BMG.successors(x)
        if BMG.nodes[v]["color"] == color_y and BMG.has_edge(v, x)
    ]
    if reciprocal_candidates:
        return random.choice(reciprocal_candidates), True

    any_successor = [v for v in BMG.successors(x) if BMG.nodes[v]["color"] == color_y]
    if not any_successor:
        # Unter der Sink-free-Eigenschaft (jeder Knoten hat mindestens ein
        # Best Match pro anderer Farbe) darf das fuer ein gueltiges
        # weak-BMG nie eintreten -- unabhaengig davon, an welcher Stelle
        # der Rekursion find_candidate aufgerufen wird, da die Eigenschaft
        # fuer jedes (Knoten, Farbe)-Paar im Ziel-BMG gilt. Ein Erreichen
        # dieser Stelle deutet auf ein nicht sink-free bzw. fehlerhaftes
        # Eingabe-BMG hin -- daher explizit fehlschlagen statt still einen
        # willkuerlichen Knoten zu waehlen.
        raise ValueError(
            f"{x!r} hat keinen einzigen Best Match der Farbe {color_y!r} -- "
            f"Sink-free-Eigenschaft verletzt (ungueltiges weak-BMG?)."
        )

    self_resolving = [v for v in any_successor if _has_reciprocal_option(BMG, v, color_x)]
    pool = self_resolving if self_resolving else any_successor
    return random.choice(pool), False


def insertNode(BCN: nx.DiGraph, layer: int, parent_name, leaf, candidate, counter):
    """
    Fuegt einen neuen Knoten unter parent_name ein, mit leaf und candidate
    als Kinder, und entfernt die alte, direkte Kante parent_name->leaf.

    counter (ein gemeinsam durchgereichter itertools.count()) garantiert
    Eindeutigkeit des Namens auch dann, wenn dasselbe (leaf, candidate)
    -Paar in DERSELBEN Ebene mehrfach vorkommt -- z.B. wenn x gegenueber
    mehreren gleichfarbigen Zielen korrigiert werden muss und dabei
    zufaellig zweimal derselbe Kandidat gezogen wird. Ohne den Zaehler
    wuerden beide Aufrufe denselben Knotennamen erzeugen; networkx wuerde
    dann keinen zweiten Knoten anlegen, sondern beide Korrekturen an
    einem gemeinsamen Knoten mit zwei Eltern verschmelzen -- was
    nachfolgende Korrekturen an dieser Stelle unnoetig dupliziert.
    """
    node_name = f"L{layer}_{leaf}_{candidate}_{next(counter)}"
    BCN.add_edge(parent_name, node_name)
    BCN.add_edge(node_name, leaf)
    BCN.add_edge(node_name, candidate)
    if BCN.has_edge(parent_name, leaf):
        BCN.remove_edge(parent_name, leaf)
    return node_name


def BCEA4(BMG: nx.DiGraph, maxLayers: int = None):
    """
    Multilayered BIC-Cherry-Expansion-Algorithmus -- NUR fuer die
    WEAK-Definition (siehe Docstring-Hinweis im Original: unter strong
    entfernen weitere Ebenen tendenziell echte Best Matches, statt
    falsche zu reparieren -- dort ist der andere, in vorherigen Antworten
    entwickelte Ansatz richtig).

    Mechanismus
    -----------
    Jeder eingefuegte Knoten (Q auf Ebene 1, weitere auf Ebene 2, 3, ...)
    erzwingt strukturell einen BEIDSEITIGEN Best Match zwischen seinen
    beiden Kindern (Singleton-LCA unter weak). Wird ein Kandidat gewaehlt,
    der die urspruengliche Seite NICHT reziprok erwidert, entsteht dadurch
    eine falsche Kante -- genau DIESE wird auf der naechsten Ebene wie ein
    eigenstaendiges Korrektur-Problem behandelt: der faelschlich
    verbundene Knoten wird durch einen neuen, echten Kandidaten ersetzt,
    und falls DIESER wieder nicht reziprok ist, geht es eine Ebene tiefer
    -- bis entweder alles reziprok aufgeloest ist oder maxLayers erreicht
    wird.

    Manche BMGs sind so NICHT darstellbar (zwei Blaetter koennen sich
    gegenseitig als jeweils fehlenden Kandidaten "die Schuld zuschieben" --
    ein echter Zyklus, den keine Ebenenzahl aufloest). maxLayers ist daher
    eine echte Notbremse, keine reine Performance-Grenze.

    Parameters
    ----------
    BMG : networkx.DiGraph
        Ziel-BMG (mode="weak").
    maxLayers : int, optional
        Maximale Anzahl zusaetzlicher Korrektur-Ebenen (zusaetzlich zur
        P- und Q-Ebene). Default: len(BMG.nodes()) -- eine Korrektur, die
        laenger braucht, ist mit hoher Wahrscheinlichkeit zyklisch.

    Returns
    -------
    BCN : networkx.DiGraph
        Das resultierende (ggf. noch unvollstaendig korrigierte)
        BIC-Cherry-Netzwerk.
    resolved : bool
        True, wenn alle Korrekturen reziprok aufgeloest werden konnten.
    unresolved : list[dict]
        Verbleibende, nicht aufgeloeste Korrekturen (leer, falls resolved).
        Je ein Eintrag mit "leaf", "wrong_match", "parent".
    """
    if maxLayers is None:
        maxLayers = len(BMG.nodes())

    BCN = nx.DiGraph()
    BCN.add_node("rho")
    node_counter = itertools.count(1)  # frisch pro Aufruf -> reproduzierbare Namen bei festem seed

    for leaf in BMG.nodes():
        BCN.add_node(leaf, color=BMG.nodes[leaf]["color"], label=leaf)

    if len(BMG.nodes()) == 2:
        for leaf in BMG.nodes():
            BCN.add_edge("rho", leaf)
        return BCN, True, []

    # --- P-Layer ---
    cherryPs = {}
    for x, y in itertools.combinations(BMG.nodes(), 2):
        if BMG.nodes[x]["color"] != BMG.nodes[y]["color"]:
            p_name = f"p_{x}_{y}"
            BCN.add_edge("rho", p_name)
            BCN.add_edge(p_name, x)
            BCN.add_edge(p_name, y)
            cherryPs[(x, y)] = p_name

    # --- Q-Layer (Ebene 1) ---
    # pending als LISTE (nicht als dict, das nach Blatt oder (Blatt,Kandidat)
    # geschluesselt ist!): dasselbe Blatt kann gleichzeitig an MEHREREN
    # unabhaengigen Stellen (unterschiedliche Elternknoten) ein Korrektur-
    # problem haben, z.B. wenn x gegenueber mehreren gleichfarbigen Zielen
    # korrigiert werden muss und dabei zufaellig derselbe Kandidat gezogen
    # wird -- ein inhaltlich geschluesseltes dict wuerde solche Faelle
    # stillschweigend ueberschreiben und eine Korrektur verlieren.
    pending = []

    for (x, y), p_name in cherryPs.items():
        if not BMG.has_edge(x, y):
            z, reciprocal = find_candidate(BMG, x, y)
            node_name = insertNode(BCN, 1, p_name, x, z, node_counter)
            if not reciprocal:
                pending.append({"leaf": z, "wrong_match": x, "parent": node_name})

        if not BMG.has_edge(y, x):
            z, reciprocal = find_candidate(BMG, y, x)
            node_name = insertNode(BCN, 1, p_name, y, z, node_counter)
            if not reciprocal:
                pending.append({"leaf": z, "wrong_match": y, "parent": node_name})

    # --- weitere Ebenen (2, 3, ...) ---
    layer = 2
    while pending and layer <= maxLayers:
        next_pending = []
        for item in pending:
            leaf, wrong_match, parent_name = item["leaf"], item["wrong_match"], item["parent"]
            # leaf hat wrong_match faelschlich als Best Match; wir suchen
            # fuer leaf einen echten Ersatz fuer wrong_match (exakt dieselbe
            # Logik wie in der P/Q-Ebene, nur eine Stufe tiefer angesetzt).
            w, reciprocal = find_candidate(BMG, leaf, wrong_match)
            node_name = insertNode(BCN, layer, parent_name, leaf, w, node_counter)
            if not reciprocal:
                next_pending.append({"leaf": w, "wrong_match": leaf, "parent": node_name})
        pending = next_pending
        layer += 1

    resolved = not pending
    return BCN  #, resolved, pending
