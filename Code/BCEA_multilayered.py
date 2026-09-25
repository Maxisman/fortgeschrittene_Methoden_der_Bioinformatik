import itertools
import random

import networkx as nx


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


def MLBCEA(BMG: nx.DiGraph, maxLayers: int = None):
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
    return BCN, resolved, pending







#################
# Erster Ansatz #
#################

# def find_candidate(BMG: nx.DiGraph,x,y):
#     """
#     Sucht einen Ersatzkandidaten fuer y (gleiche Farbe wie y), der x's
#     fehlenden Match zu y ersetzt.

#     Da per schwacher Definition jede Q-Node einen reziproken
#     best match einbaut, sollte y' (bzw. z) einen best match zu x aufweisen.
#     Gibt es kein solches Blatt, muss hier eine neue Ebene erstellt werden
#     den durch den Q-Knoten fälschlich generierte best match wieder zu brechen.
#     """
#     candidates = []
#     reciprog_match = True
#     candidates = [v for v in BMG.successors(x) if BMG.nodes[v]['color'] == BMG.nodes[y]['color'] and BMG.has_edge(v,x)]

#     if not candidates:
#         reciprog_match = False
#         candidates = [v for v in BMG.successors(x) if BMG.nodes[v]['color'] == BMG.nodes[y]['color']]

#     if not candidates:
#         candidates = [v for v in BMG.nodes if BMG.nodes[v]['color'] == BMG.nodes[y]['color'] and v != y]

#     return random.choice(candidates),reciprog_match





# def insertNode(BCN: nx.DiGraph,layer: int, namePrev, x, z):

#     # hier muss noch ein umwandeln von layer(int) in layer(str) stattfunden. 
#     nameNew = f"{layer}_{x}_{z}"
#     BCN.add_edge(namePrev, nameNew)
#     BCN.add_edge(nameNew, x)
#     BCN.add_edge(nameNew, z)
#     if BCN.has_edge(namePrev,x):
#         BCN.remove_edge(namePrev,x)

#     return nameNew



# def MLBCEA(BMG: nx.DiGraph, maxLayers: int = 10):

#     """
#     Funktion für den BIC-Cherry-Expansion-Algorithmus, mit der Möglichkeit,
#     weitere Ebenen einzufügen.
#     Dies macht nur Sinn, wenn man die schwache Definition der best-matches
#     betrachtet, da weitere Ebenen tendenziell best matches entfernen und
#     BCNs basierend im Kontext der strikten Definition eher darunter leiden,
#     zu wenige best matches zu zeigen.
 
#     Parameter
#     ----------
#     BMG : networkx.DiGraph
#         Das zu erklärende Ziel-BMG (i.d.R. mode="weak").
 
#     Returns
#     -------
#     BCN : networkx.DiGraph
#         Das resultierende BIC-Cherry-Netzwerk
#     """

#     BCN = nx.DiGraph()
#     BCN.add_node("rho")

#     cherryPs = {}
#     falseBestMatches = {}
#     nextDict = {}

#     for leaf in BMG.nodes():
#         BCN.add_node(leaf, color= BMG.nodes[leaf]["color"], label=leaf)
    
#     if len(BMG.nodes()) == 2:
#         for leaf in BMG.nodes():
#             BCN.add_edge("rho", leaf)
#         return BCN

#     # P-Layer
#     for x, y in itertools.combinations(BMG.nodes(), 2):
#         if BMG.nodes[x]["color"] != BMG.nodes[y]["color"]:
#             p_name = f"p_{x}_{y}"
#             BCN.add_edge("rho", p_name)
#             BCN.add_edge(p_name, x)
#             BCN.add_edge(p_name, y)
#             cherryPs[(x, y)] = p_name

#     # Q-Extensions
#     for (x, y), p_name in cherryPs.items():

#         if not BMG.has_edge(x,y):
#             z, rec_match = find_candidate(BMG, x, y)
#             nodeName = insertNode(BCN, 1, p_name, x, z)
#             if not rec_match:
#                 falseBestMatches[(x,z)] = nodeName

#         if not BMG.has_edge(y,x):
#             z, rec_match = find_candidate(BMG, y, x)
#             nodeName = insertNode(BCN, 1, p_name, y, z)
#             if not rec_match:
#                 falseBestMatches[(y,z)] = nodeName

#     # lower leayers
#     # Es werden die gerade eingefügten Kanten (x->y) untersucht, ob diese einen Best-Match (y->x) generiert haben, der gar nicht da sein sollte.
#     # Ist dies der Fall, wird für y->x eine neue Ebene eingefügt um diese zu trennen

#     if falseBestMatches:
#         for (x,y) in falseBestMatches:
#             if not BMG.has_edge(x,y):
#                 z, rec_match = find_candidate(BMG, x, y)



#     return BCN
