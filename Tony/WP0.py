# %% 
import networkx as nx
import matplotlib.pyplot as plt

# %% Aufgabe 0.1
G = nx.Graph()
G.add_nodes_from(["A","B","C","D","E"])
G.add_edges_from([("A","B"), ("B","C"), ("C","D"), ("D","E"), ("B","D"),("A","E")])

print(G.degree(["A","B","C","D","E"]))
for path in (nx.all_simple_paths(G, source="A", target="D")):
    print(f"Path from A to D: {path}")
print(nx.is_connected(G))
subG = G.subgraph(["A","B","D","E"])
print("es gibt folgenden cycle:", nx.cycle_basis(G))
print("Subgraph edges:", sorted(subG.edges()))

pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=True)
#plt.show()


# %% Aufgabe 0.2

G2 = nx.DiGraph()
G2.add_edges_from([(1,2),(1,3),(2,3),(3,4),(4,2)])

for node in G2.nodes():
    print(f"Node {node} has in-degree {G2.in_degree(node)}, out-degree {G2.out_degree(node)} and the following out-neighbours: {sorted(G2.successors(node))}")
    if G2.in_degree(node) == 0:
        print(f"Node {node} is a source node.")
    if G2.out_degree(node) == 0:
        print(f"Node {node} is a sink node.")

print(f"is the graph weakly connected? {nx.is_weakly_connected(G2)}")
print(f"is the graph strongly connected? {nx.is_strongly_connected(G2)}")


#nx.draw(G2, with_labels=True)
#plt.show()

# %%
G3 = nx.DiGraph()

nodes = {'a1':'red','a2':'red','b1':'blue','b2':'blue','c1':'green'}
for name,color in nodes.items():
    G3.add_node(name, color = color)

G3.add_edges_from([
        ('a1','b1'), ('a1','c1'), ('a2','b2'), ('a2','c1'),
    ('b1','a1'), ('b1','c1'), ('b2','a2'), ('b2','c1'),
    ('c1','a1'), ('c1','b1')
])

#print(f"{G3.nodes['a1']['color']}")

def is_color_sink_free(G):
    allColors = set(nx.get_node_attributes(G=G,name = 'color').values())
    sinkFree = True
    for v in G.nodes:
        
        ownColor = G.nodes[v]['color']
        neighborColors = {G.nodes[u]['color'] for u in G.successors(v)}
        missingColors = allColors - {ownColor} - neighborColors
        if missingColors:
            print(f"The Graph is not color sink free, for node {v} arc to color(s) {missingColors} is missing")
            sinkFree = False
    if sinkFree == True:
        return True
    else:
        return False

print("is Graph3 color sink free?", is_color_sink_free(G3))

nodeColorList = [nodes[v] for v in G3.nodes()]
nx.draw(G3,with_labels=True,node_color=nodeColorList)
plt.show()

# %% 0.4

###### Aufgabe "write out the ancestor order" nicht ganz verstanden...

#(b)
#   lca(a1,b1) = u
#   lca(b1,c2) = p
#   lca(b1,b2) = p
#   the lca in p for two different gene types means that there was
#   a gene duplication (b1 and b2) and a gene speciazation (b and c)


G4 = nx.DiGraph()
G4.add_edges_from([('p','u'),('p','v'),
                  ('u','a1'),('u','w'),
                  ('w','b1'),('w','c1'),
                  ('v','b2'),('v','c2')])

def lca(T, root, x, y):
    path_x = nx.shortest_path(T, root, x)
    path_y = nx.shortest_path(T, root, y)
    print(path_x)
    for v in range(len(path_x)):
        if path_x[v] != path_y[v]:
            print(f"the lca of {x} and {y} is {path_x[v-1]}")
            return #path_x[v-1]
        
# first thought was to loop all ancestors of x and in the loop another
# loop for the ancestors of y. if theres a match return the match.
# probably takes longer to compute

lca(G4,'p','a1','b1')
lca(G4,'p','b1','c2')
lca(G4,'p','b1','b2')

# %% 0.5

G5 = nx.DiGraph()
G5.add_edges_from([('p','u'),('p','v'),('u','x'),('u','y'),('v','x')])
print(f"is G5 a DAG? {nx.is_directed_acyclic_graph(G5)}")
print("Topological order:", list(nx.topological_sort(G5)))
print("common ancestors of x and y:", nx.ancestors(G5,'x') & nx.ancestors(G5,'y'))
print("parents of x:", list(G5.predecessors('x')))

# %% 0.6

def aho_build(leaves, triples):
    """
    leaves:  a set of leaf labels
    triples: a list of tuples (a, b, c) meaning "ab|c"
    Returns: a nested tuple representing the tree, or None if inconsistent.
    """
    if len(leaves) <= 2:
        return tuple(sorted(leaves))
    
    # Step 1: Build the cluster graph (undirected) on these leaves.
    # For each triple (a,b,c) where all three are in `leaves`,
    # add an undirected edge between a and b.
    # YOUR CODE HERE

    cluster = nx.Graph()
    cluster.add_nodes_from(leaves)
    relevant = [(a,b,c) for (a,b,c) in triples if a in leaves and b in leaves and c in leaves]
    
    for (a,b,c) in relevant:
        cluster.add_edge(a,b)
    
    # Step 2: Find connected components.
    # If only one component → inconsistent, return None.
    # YOUR CODE HERE

    components = list(nx.connected_components(cluster))

    if len(components) == 1:
        return None
    
    # Step 3: Recurse on each component.
    # Only pass triples whose three leaves all belong to that component.
    # Collect the results as children of the current node.
    # YOUR CODE HERE

    child = []
    for comp in components:
        subtree = aho_build(comp,triples)
        if subtree is None:
            return None
        child.append(subtree)
    return tuple(child)

print("Test 1:", aho_build({'a','b','c','d'}, [('a','b','c'), ('a','b','d')]))
print("Test 2:", aho_build({'a','b','c','d'},
                           [('a','b','c'), ('a','b','d'), ('c','d','a')]))
print("Test 3:", aho_build({'a','b','c'},
                           [('a','b','c'), ('b','c','a'), ('c','a','b')]))

# %%

def lcaWithDepth(T, root, x, y):
    path_x = nx.shortest_path(T, root, x)
    path_y = nx.shortest_path(T, root, y)

    lca = root
    depth = 0

    for v in range(min(len(path_x), len(path_y))):
        if path_x[v] == path_y[v]:
            lca = path_x[v]
            depth = v
        else:
            break

    return lca, depth

def getLeaves(T):
    leaves = []
    for v in T.nodes():
        if not list(T.successors(v)):
            leaves.append(v)
    return leaves     

        
def compute_bmg(T):
    """
    T:     a nx.DiGraph representing a rooted tree (edges parent→child)
    root:  the root vertex
    sigma: dict mapping each leaf to its color
    Returns: a nx.DiGraph representing the BMG
    """
    BMG = nx.DiGraph()
    leaves = []
    colors = []


    for v in T.nodes():

        # Alle Knoten finden, die keine Nachfolger haben -> Blätter
        if not list(T.successors(v)):
            leaves.append(v)
            colors.append(T.nodes[v]['color'])
        
        # Der Knoten ohne Eltern ist die Wurzel
        if not list(T.predecessors(v)):
            root = v

    colors=set(colors)
    
    for leaf in leaves:

        leafColor = T.nodes[leaf]['color']
        BMG.add_node(leaf, color=leafColor)


        for color in colors:
            if leafColor == color:
                continue
            candidates = [y for y in leaves if T.nodes[y]['color'] == color]
            bestDepth = max(lcaWithDepth(T, root, leaf, y)[1] for y in candidates)
            for y in candidates:
                if lcaWithDepth(T, root, leaf, y)[1] == bestDepth:
                    BMG.add_edge(leaf,y)

    return BMG


        # candidates = [y for y in leaves if sigma[y] == s]
        # best_depth = max(lca_depth(T, root, x, y) for y in candidates)
        # for y in candidates:
        #     if lca_depth(T, root, x, y) == best_depth:
        #         BMG.add_edge(x, y)

            
    
    # For each leaf x, for each color s ≠ σ(x):
    #   1. Find all leaves y with σ(y) = s (the "candidates").
    #   2. Compute lca_depth(x, y) for each candidate.
    #      (lca_depth = distance from root to lca(x,y) — deeper = closer relative)
    #   3. Find the maximum depth among candidates.
    #   4. Add arc x→y for every candidate achieving that maximum.
    # YOUR CODE HERE (use your lca function from 0.4)

    
    return root, leaves, colors

nodes = {'a1':'red','b1':'blue','b2':'blue','c1':'green','c2':'green'}
T = nx.DiGraph()

for name,color in nodes.items():
    T.add_node(name, color = color)
T.add_edges_from([('p','u'),('u','v'),('u','a1'),('v','b1'),('v','c1'),('p','w'),('w','b2'),('w','c2')])


BMG1 = compute_bmg(T)


nodeColorList = [nodes[v] for v in BMG1.nodes()]
nx.draw(BMG1,    with_labels=True,node_color=nodeColorList)
# plt.show()




# %%
