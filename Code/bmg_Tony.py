import networkx as nx

def bmg(G: nx.DiGraph, mode = "weak") -> nx.DiGraph:
    if mode not in ("weak", "strong"):
        raise ValueError(f"mode must be 'weak' or 'strong', got {mode!r}")

    BMG = nx.DiGraph()

    # Alle Blätter identifizieren 
    leaves = [node for node in G.nodes() if G.out_degree(node) == 0]

    # sigma generieren und leaves in BMG einfügen, LeafAncestors Dict generieren
    sigma = {}
    leafAncestors = {}

    for leaf in leaves:
        sigma[leaf] = G.nodes[leaf]["color"]
        BMG.add_node(leaf, color = sigma[leaf])
        leafAncestors[leaf] = nx.ancestors(G,leaf) | {leaf}

    # Durch Blätter iterieren
    for x in leaves:
        xAncestors = leafAncestors[x]
        color_x = sigma[x]
    
        # andere Spezies definieren
        otherColors = set(sigma.values()) - {color_x}

        # durch andere Spezies iterieren um pro Spezies den best match zu finden
        for targetColor in otherColors:
            lcaDict ={}
            candidates = [y for y in leaves if sigma[y] == targetColor] # and y != x
            
            # Alle Nodes der targetColor iterieren, gemeinsame Vorfahren suchen und ein dict aufbauen, das für jede Node der aktuellen Farbe die LCAs ausgibt
            for y in candidates:
                
                yAncestors = leafAncestors[y]
                commonAncestors = xAncestors & yAncestors

                # Subgraph der Schnittmenge von ancestors(x) und ancestors(y). Leaves dieses Subgraphs liefert die LCAs
                subgraph = G.subgraph(commonAncestors)
                lcaDict[y] = {node for node in subgraph.nodes if subgraph.out_degree(node) == 0}

            # Vergleich der LCAs zwischen x und allen y

            #### hier kann zwischen weak und strong BMGs unterschieden werden
            if mode == "weak":
                # weak best matches: es reicht, wenn ein LCA zwischen x und y niedriger liegt als die LCAs zwischen x und y'
                # kein best match, wenn alle lcas von lcaxy höher liegen, als ein lca von lcaxz

                for y, lcasxy in lcaDict.items():
                    isBestMatch = False

                    for lcaxy in lcasxy:
                        any_lcaxz_lower = False

                        for z, lcasxz in lcaDict.items():
                            if y == z:
                                continue

                            for lcaxz in lcasxz:

                                # Algorthmus schaut für jeden lcaxy ob dieser einen lcaxz hat, der niedirger ist.
                                # Wenn für einen lcaxy kein lcaxz gefunden wird, der niedriger steht, so ist y ein best
                                # match zu x

                                if lcaxy != lcaxz and nx.has_path(G, lcaxy, lcaxz):
                                    any_lcaxz_lower = True
                                    break
                            
                            if any_lcaxz_lower:
                                break

                        if not any_lcaxz_lower:
                            isBestMatch = True
                            break

                    if isBestMatch:
                        BMG.add_edge(x,y)

            elif mode == "strong":
            # Strong Best Matches:
            # Alle LCAs zwischen x und y müssen niedriger sein als LCA von x und y'

                for y, lcasxy in lcaDict.items():
                    isBestMatch = True

                    for z, lcasxz in lcaDict.items():
                        if y == z:
                            continue
                        
                        for lcaxy in lcasxy:
                            for lcaxz in lcasxz:

                                # Algorthmus schaut für jeden lcaxy ob dieser einen lcaxz hat, der niedirger ist.
                                # Wenn für nur ein lcaxy ein lcaxz gefunden wird, der niedriger liegt, so liegt kein best match vor

                                if lcaxy != lcaxz and nx.has_path(G, lcaxy, lcaxz):
                                    isBestMatch = False
                                    break

                            if not isBestMatch:
                                break
                        if not isBestMatch:
                            break

                    if isBestMatch:
                        BMG.add_edge(x,y)
    return BMG



def bmg_fast(G: nx.DiGraph, mode: str = "weak") -> nx.DiGraph:
    if mode not in ("weak", "strong"):
        raise ValueError(f"mode must be 'weak' or 'strong', got {mode!r}")

    BMG = nx.DiGraph()

    # 1. Blätter & Spezies-Zuordnung (sigma)
    leaves = [node for node in G.nodes() if G.out_degree(node) == 0]
    sigma = {leaf: G.nodes[leaf]["color"] for leaf in leaves}
    
    for leaf, color in sigma.items():
        BMG.add_node(leaf, color=color)

    # 2. Vorfahren inklusive Eigenknoten vorausberechnen
    leaf_ancestors = {leaf: nx.ancestors(G, leaf) | {leaf} for leaf in leaves}
    colors = set(sigma.values())

    # 3. Best Matches berechnen
    for x in leaves:
        x_anc = leaf_ancestors[x]
        color_x = sigma[x]

        for target_color in (colors - {color_x}):
            target_leaves = [y for y in leaves if sigma[y] == target_color]
            if not target_leaves:
                continue

            # --- Menge M(x, B) direkt bestimmen ---
            # Gemeinsame Vorfahren von x und ALLEN Blättern der Zielspezies B
            all_target_anc = set().union(*(leaf_ancestors[y] for y in target_leaves))
            common_species_anc = x_anc & all_target_anc

            # M(x, B) sind die tiefsten Knoten (out_degree == 0 im Teilgraphen)
            sub_M = G.subgraph(common_species_anc)
            M_xB = {node for node in sub_M.nodes if sub_M.out_degree(node) == 0}

            # --- Vergleiche für jedes y in B via Mengenoperationen ---
            for y in target_leaves:
                common_xy = x_anc & leaf_ancestors[y]
                sub_xy = G.subgraph(common_xy)
                lcas_xy = {node for node in sub_xy.nodes if sub_xy.out_degree(node) == 0}

                if mode == "weak":
                    # LCA(x, y) ∩ M(x, B) ≠ ∅
                    if lcas_xy & M_xB:
                        BMG.add_edge(x, y)

                elif mode == "strong":
                    # LCA(x, y) ⊆ M(x, B)
                    if lcas_xy.issubset(M_xB):
                        BMG.add_edge(x, y)

    return BMG