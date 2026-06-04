import random
import networkx as nx

def insertHybrid(N:nx.DiGraph) -> nx.DiGraph:
    # n einfügen? um mehrere Hybridization events zuzlassen?

    # max label herausfinden
    label = max(nx.get_node_attributes(N,"label").values())+1

    # über max(dist) den Zeitbereich herausfinden

    timerange = max(nx.get_node_attributes(N,"tstamp").values())

    # random Zeitpunkt auswählen

    time = random.uniform(0,timerange)

    # edges finden, die zu dieser Zeit existiert haben.

    possibleEdges = set(edge for edge in N.edges if N.nodes[edge[0]]["tstamp"] >= time and N.nodes[edge[1]]["tstamp"] <= time)

    # eine zufällige Edge auswählen, diese durch einen Hybrid erweitern.
    # remove_edge(Parent,Child) 
    # add_edges_from((Parent,Hybrid),(Hybrid,Child))

    # eine zweite Edge wählen, die den Zeitpunkt enthält und nicht den gleichen Parent hat.
    # Child2 auswählen aus allen successors der Edge0
    # add_edge(Hybrid,Child2)

    edges = random.sample(sorted(possibleEdges),2)

    # Ausgangsspezies bestimmen
    # parentspecies = [N.nodes[parent[0]]["reconc"] for parent in edges]

    #
    N.add_node(label,
                    label = label,
                    event = 'H',
                    # reconc = 1, # gibt an zu welcher Spezies es gehört
                    tstamp = time,
                    # transferred = ,
                    dist = 0.0
                    )
    
    for parent, child in edges:
        N.remove_edge(parent,child)
        N.add_edge(parent,label)
        N.add_edge(label,child)
    return N