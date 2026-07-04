import random
import networkx as nx
import matplotlib.cm as cm

def insertHybrid(N:nx.DiGraph, i:int = 1):

    ### Entry Assertions
    assert isinstance(N, nx.DiGraph), "Eingabe muss ein nx.DiGraph sein!"
    assert isinstance(i,int), "Anzahl der Hybridisierungsevents muss int ein"
    assert N.number_of_edges() > 0, "Graph hat keine Kanten!"

    N_mod = N.copy()

    # Es sollte erst eine Edge und eine dazu passende Node für die Hbridisierung gesucht werden
    # nur wenn eine passende Kombination gefunden wurde, sollen veränderungen am Baum gemacht werden

    cached_predecessors = {}

    # Suche nach Edge und Node:
    for _ in range(i):

        # max label herausfinden
        label = max(nx.get_node_attributes(N_mod,"label").values())+1
        foundPair = False

        # Liste mit zufälliger Reihenfolge der Edges und Nodes generieren
        edgeList = list(N_mod.edges)
        random.shuffle(edgeList)

        nodeList = list(N_mod.nodes)
        random.shuffle(nodeList)

        for edge in edgeList:
            edgeParent = edge[0]
            edgeChild = edge[1]

            tstampHybrid = (N_mod.nodes[edgeParent]["tstamp"] + N_mod.nodes[edgeChild]["tstamp"])/2

            for node in nodeList:
                if node not in cached_predecessors:
                    cached_predecessors[node] = list(N_mod.predecessors(node))
        
                nodeParents = cached_predecessors[node]

                if (
                    N_mod.nodes[node]["tstamp"] < tstampHybrid                      # Node "jünger" als Hybrid ###### dist vs. tstamp???
                    and edgeParent not in nodeParents                               # Node hat nicht den parent als parent
                    and edgeChild not in nodeParents                                # Node hat nicht das child als parent
                    and node != edgeChild
                    and node != edgeParent
                    # and N.nodes[node]["reconc"] != N.nodes[label]["reconc"]       # Node andere Spezies als Hybrid; soll das so?
                    ):
                    foundPair = True
                    break

            if foundPair:
                break

        if not foundPair:
            print ("No suitable Edges and Nodes found for hybridization Event")
            return N_mod

        #### Veränderung des Netzwerks:

        # Kante zwischen Parent und Child entfernen
        N_mod.remove_edge(edgeParent,edgeChild)

        # Hybrid zwischen Parent und Child einbauen

        distHybrid = (N_mod.nodes[edgeParent]["dist"] + N_mod.nodes[edgeChild]["dist"])/2

        N_mod.add_node(label,
                    label = label,
                    event = 'H',
                    reconc = N_mod.nodes[edgeParent]["reconc"], # gibt an zu welcher Spezies es gehört nochmal herausfinden, was genau zeine Liste an dieser Stelle bedeutet
                    tstamp = tstampHybrid,
                    # transferred = ,
                    dist = distHybrid
                    )
        
        N_mod.add_edges_from([(edgeParent,label),(label,edgeChild)])
            
        # Node mit Hybrid verbinden

        N_mod.add_edge(label,node)
        
        print(f"Es wurde ein Hybrid zwischen node {N_mod.nodes[edgeParent]["label"]} und node {N_mod.nodes[edgeChild]["label"]} eingefügt und dieser wurde mit Node {N_mod.nodes[node]["label"]} verbunden") 
        
        ### Exit Assertions:
        assert not N_mod.has_edge(edgeParent, edgeChild), "Alte Kante existiert noch!"
        assert N_mod.has_edge(label, node), "Verbindung zum Hybriden fehlt!"
        assert nx.is_directed_acyclic_graph(N_mod), "Zyklus generiert!"

    return N_mod


def convert_to_nx(T) -> nx.DiGraph:
    """
    Converts an Asymmetree Tree into a NetworkX DiGraph.
    Instead of using the node ids (as the corresponding function does in the asymmetree package)
    it stores the node labels as the node names in the NetworkX DiGraph.
    """
    graph = nx.DiGraph()

    # not sure what this does in the original code, commenting it out for now
    #if not self.root:
    #    return graph, None

    for v in T.preorder():
        graph.add_node(v.label)
        for key, value in v.attributes():
            graph.nodes[v.label][key] = value

    for u, v, sibling_nr in T.edges_sibling_order():
        if u is v:
            raise RuntimeError(f"loop at {u} and {v}")
        graph.add_edge(u.label, v.label)
        graph.nodes[v.label]["sibling_nr"] = sibling_nr

    return graph



def color_leaves(N):
    # Alle Blätter identifizieren
    leaves = [node for node in N.nodes() if N.out_degree(node) == 0]

    # Einzigartige Spezies der Blätter sammeln und ihnen Farben zuweisen
    # Wir nutzen ein Set, um Duplikate zu vermeiden
    unique_species = list(set(N.nodes[node]["reconc"] for node in leaves))

    # Farbpalette generieren (z. B. 'Set1', 'tab10' oder 'viridis')
    cmap = cm.get_cmap("Set1", len(unique_species))
    species_to_color = {
        spec: cmap(i) for i, spec in enumerate(unique_species)
    }

    # 4. Farbliste für ALLE Knoten im Graphen erstellen
    node_colors = []
    default_color = (
        "#A0CBE2"  # Eine neutrale Farbe (z.B. Hellblau) für innere Knoten
    )

    for node in N.nodes():
        if node in leaves:
            species = N.nodes[node]["reconc"]
            node_colors.append(species_to_color[species])
        else:
            node_colors.append(default_color)

    return node_colors 

def calculate_time_tree_layout(G: nx.DiGraph):
    """Berechnet ein perfektes Time-Tree-Layout.

    Die Y-Achse spiegelt exakt den tstamp wider.
    Die X-Achse ordnet Blätter kollisionsfrei nebeneinander an.
    """
    pos = {}

    # 1. Finde die Root des Baums (Node ohne Parents)
    roots = [n for n in G.nodes if G.in_degree(n) == 0]
    if not roots:
        # Falls es ein Netzwerk ist und keine klare Root existiert,
        # nehmen wir die Node mit dem höchsten Timestamp als Startpunkt
        root = max(G.nodes, key=lambda n: G.nodes[n].get("tstamp", 0))
    else:
        root = roots[0]

    # 2. Finde alle Blätter (Leaves) im Graphen
    # Bei Netzwerken: Nodes ohne ausgehende Kanten
    leaves = [n for n in G.nodes if G.out_degree(n) == 0]

    # Trick: Wir sortieren die Blätter basierend auf einer Tiefensuche (DFS) von der Root aus.
    # Das sorgt dafür, dass geschwisterliche Blätter auf der X-Achse auch nebeneinander landen!
    dfs_order = list(nx.dfs_preorder_nodes(G, source=root))
    ordered_leaves = [n for n in dfs_order if n in leaves]

    # 3. Weise den Blättern gleichmäßige X-Koordinaten zu (z.B. von 0 bis len(leaves)-1)
    for index, leaf in enumerate(ordered_leaves):
        pos[leaf] = (float(index), float(G.nodes[leaf].get("tstamp", 0.0)))

    # 4. Berechne die X-Koordinaten für alle inneren Knoten von unten nach oben
    # Wir wiederholen das, bis alle Knoten eine Position haben (wichtig für komplexe Netzwerke)
    remaining_nodes = set(G.nodes) - set(ordered_leaves)

    while remaining_nodes:
        nodes_to_remove = set()
        for node in remaining_nodes:
            children = list(G.successors(node))

            # Ein innerer Knoten kann seine X-Position bestimmen, sobald alle seine Kinder eine Position haben
            if children and all(child in pos for child in children):
                # Die X-Position ist das exakte Mittelmaß der X-Positionen aller Kinder
                avg_x = sum(pos[child][0] for child in children) / len(children)
                y = float(G.nodes[node].get("tstamp", 0.0))

                pos[node] = (avg_x, y)
                nodes_to_remove.add(node)

        # Falls in einem Durchlauf nichts gelöst wurde (z.B. wegen verbleibender Loops in komplexen Netzwerken),
        # brechen wir ab und weisen den Resten Standardwerte zu, um Endlosschleifen zu verhindern.
        if not nodes_to_remove:
            for node in remaining_nodes:
                pos[node] = (
                    random.uniform(0, len(leaves)),
                    float(G.nodes[node].get("tstamp", 0.0)),
                )
            break

        remaining_nodes -= nodes_to_remove

    return pos

