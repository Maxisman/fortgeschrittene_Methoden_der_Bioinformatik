import random
import networkx as nx

def insertHybrid(N:nx.DiGraph):
    # n einfügen? um mehrere Hybridization events zuzlassen?

    # max label herausfinden

    label = max(nx.get_node_attributes(N,"label").values())+1

    # eine zufällige Edge auswählen, diese durch einen Hybrid erweitern.

    randomEdge = random.choice(list(N.edges))

    N.remove_edge(randomEdge[0],randomEdge[1])

    tstampHybrid = (N.nodes[randomEdge[0]]["tstamp"] + N.nodes[randomEdge[1]]["tstamp"])/2
    distHybrid = (N.nodes[randomEdge[0]]["dist"] + N.nodes[randomEdge[1]]["dist"])/2

    N.add_node(label,
                label = label,
                event = 'H',
                reconc = N.nodes[randomEdge[0]]["reconc"], # gibt an zu welcher Spezies es gehört nochmal herausfinden, was genau zeine Liste an dieser Stelle bedeutet
                tstamp = tstampHybrid,
                # transferred = ,
                dist = distHybrid
                )
    
    N.add_edges_from([(randomEdge[0],label),(label,randomEdge[1])])

    # Zufällige Node auswählen, die Anforderungen erfüllt.

    randomNode = random.choice(list(node for node in N.nodes 
                                if N.nodes[node]["dist"]>0                                  # Node "jünger" als Hybrid ###### dist vsa. tstamp???
                                and N.nodes[node]["reconc"] != N.nodes[label]["reconc"]     # Node andere Spezies als Hybrid
                                and N.predecessors(node) != randomEdge[0]                   # Node hat nicht den parent als parent
                                and N.predecessors(node) != randomEdge[1]                   # Node hat nicht das child als parent ###### scheint noch nicht zu funktionieren
                                and node != randomEdge[1]))  
    
    if not randomNode:
        print("es wurde keine passende Node gefunden")

        
    # Node mit Hybrid verbinden

    N.add_edge(label,randomNode)

    return f"Es wurde ein Hybrid zwischen node {N.nodes[randomEdge[0]]["label"]} und node {N.nodes[randomEdge[1]]["label"]} eingefügt und dieser wurde mit Node {N.nodes[randomNode[0]]["label"]} verbunden"  # Funktion gibt das Netzwerk aus, verändert aber das Netzwerk sowieso. Sollte man den ursprünglichen Baum unverändert lassen?? Dann müsste man erst eine Kopie machen