import networkx as nx
import matplotlib.pyplot as plt

def aho_build(leaves, triples):
    """
    leaves:  a set of leaf labels
    triples: a list of tuples (a, b, c) meaning "ab|c"
    Returns: a nested tuple representing the tree, or None if inconsistent.
    """
    if len(leaves) <= 2:
        return str(tuple(sorted(leaves)))
    
    # Step 1: Build the cluster graph (undirected) on these leaves.
    # For each triple (a,b,c) where all three are in `leaves`,
    # add an undirected edge between a and b.

    Cluster_Graph = nx.Graph()
    for leaf in leaves:
        Cluster_Graph.add_node(leaf)

    for triple in triples:
        Cluster_Graph.add_edge(triple[0], triple[1])

    # Step 2: Find connected components.
    # If only one component → inconsistent, return None.
    
    if nx.is_connected(Cluster_Graph):
        return None
    
    # Step 3: Recurse on each component.
    # Only pass triples whose three leaves all belong to that component.
    # Collect the results as children of the current node.
    
    representation = "("
    for component in nx.connected_components(Cluster_Graph):
        new_triples = []
        for triple in triples:
            if triple[0] in component and triple[1] in component and triple[2] in component:
                new_triples.append(triple)
        representation += aho_build(component, new_triples) + ", "
    pass

    return representation[0:-2] + ")"

print(aho_build({'a','b','c','d'}, [('a','b','c'), ('a','b','d')]))
print(aho_build({'a','b','c','d'}, [('a','b','c'), ('a','b','d'), ('c','d','a')]))
print(aho_build({'a','b','c'}, [('a','b','c'), ('b','c','a'), ('c','a','b')]))