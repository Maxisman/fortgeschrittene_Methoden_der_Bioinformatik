import random
import networkx as nx

def insertHybrid(DiGraph):
    # n einfügen? um mehrere Hybridization events zuzlassen?

    # max label herausfinden
    label = max(nx.get_node_attributes(DiGraph,"label").values())+1

    # über max(dist) den Zeitbereich herausfinden

    timerange = max(nx.get_node_attributes(DiGraph,"tstamp").values())

    # random Zeitpunkt auswählen

    time = random.uniform(0,timerange)

    # edges finden, die zu dieser Zeit existiert haben.

    possibleEdges = set(edge for edge in DiGraph.edges if DiGraph.nodes[edge[0]]["tstamp"] >= time and DiGraph.nodes[edge[1]]["tstamp"] <= time)

    # eine zufällige Edge auswählen, diese durch einen Hybrid erweitern.
    # remove_edge(Parent,Child) 
    # add_edges_from((Parent,Hybrid),(Hybrid,Child))

    # eine zweite Edge wählen, die den Zeitpunkt enthält und nicht den gleichen Parent hat.
    # Child2 auswählen aus allen successors der Edge0
    # add_edge(Hybrid,Child2)

    edges = random.sample(sorted(possibleEdges),2)

    # Ausgangsspezies bestimmen
    # parentspecies = [DiGraph.nodes[parent[0]]["reconc"] for parent in edges]

    #
    DiGraph.add_node(label,
                    label = label,
                    event = 'H',
                    # reconc = 1, # gibt an zu welcher Spezies es gehört
                    tstamp = time,
                    # transferred = ,
                    dist = 0.0
                    )
    
    for parent, child in edges:
        DiGraph.remove_edge(parent,child)
        DiGraph.add_edge(parent,label)
        DiGraph.add_edge(label,child)
    return DiGraph