import networkx as nx


def pullup(G:nx.DiGraph,node):
    for children in G.successors(node):
        for child in children:
            G.addEdge(G.predecessor(node),child)

    G.remove_node(node)
# Was ist, wenn node mehr als einen predecessor hat?

def pushdown(G:nx.DiGraph,node):
    # CODE FEHLT NOCH
    return G

def BICCtoTree(G:nx.DiGraph):
    