import random
import networkx as nx

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