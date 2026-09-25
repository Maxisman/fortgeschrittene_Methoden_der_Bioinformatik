import networkx as nx
from collections import Counter
import random
rng = random.Random(42)


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



def BCEA(G: nx.DiGraph, mode: str = "strong") -> nx.DiGraph:
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