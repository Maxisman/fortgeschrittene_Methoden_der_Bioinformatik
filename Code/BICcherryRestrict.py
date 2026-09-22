import networkx as nx
from collections import Counter
import random
rng = random.Random(42)

def BICcherryRestrict(G: nx.DiGraph) -> nx.DiGraph:
    # ASSERTIONS
    ## assert colored digraph
    assert isinstance(G, nx.DiGraph)
    assert all("color" in G.nodes[v] for v in G.nodes)

    ## assert properly colored (no edges between same color)
    colors = nx.get_node_attributes(G,"color")
    for u,v in G.edges():
        assert colors[u] != colors[v]

    ## assert sicor in hub
    ### find all sicors
    color_counts = Counter(colors.values())
    sicor = [v for v,c in colors.items() if color_counts[c]==1]
    ### assert in-hub-ness
    for s in sicor:
        for u in G.nodes():
            if colors[u] != colors[s]:
                assert G.has_edge(u,s)

    # BIC-CHERRY
    ## initialize and root network digraph
    N = nx.DiGraph()
    N.add_node("rho")

    ## extract differently colored leafs from G
    cherrylist = []
    for key1, value1 in colors.items():
        for key2, value2 in colors.items():
            if key1 < key2 and value1 != value2:
                cherrylist.append(frozenset({key1, key2}))
    ## add leaves and parent nodes to get uglycherry
    p_nodes = dict()
    for pair in cherrylist:
        x,y = sorted(pair)
        p_name = f"p_{x}_{y}"
        p_nodes[pair] = p_name
        N.add_edge("rho",p_name)
        N.add_edge(p_name, x)
        N.add_edge(p_name, y)
    ## add back color property to nodes
    for node, color in colors.items():
        N.nodes[node]["color"] = color

    # EXTENSION
    ## find all cherrys x,y in N that don't have an edge x,y or y,x in G
    ### find *any* (optimize here? random for now) another x' or y' that has an edge in G
    ### introduce q_xy' or q_yx' below the corresponding p_xy or p_yx
    for pair, p_name in p_nodes.items():
        x,y = sorted(pair)
        if not G.has_edge(x,y):

            # statt random choice, sollte hier der successor gewählt werden, der widerum x als best match hat, sofern vorhanden

            # Alte Auswahl:
            # y_prime = rng.choice([v for v in G.successors(x) if colors[v]==colors[y]])

            # neue Auswahl:
            # 1. reziproger best match (x->z & z->x)
            # 2. asymmetrischer best match (x->z)
            # 3. asymmetrischer best match (z->x)
            # 4. irgendein y' != y
            candidates = []
            candidates = [v for v in G.successors(x) if colors[v] == colors[y] and G.has_edge(v,x)]

            if not candidates:
                candidates = [v for v in G.successors(x) if colors[v] == colors[y]]

            if not candidates:
                candidates = [v for v in G.predecessors(x) if colors[v] == colors[y] and v != y]

            if not candidates:
                candidates = [v for v in G.nodes if colors[v] == colors[y] and v != y]

            y_prime = rng.choice(candidates)


            ## insert q_xy' below p_xy
            q_name = f"q_{x}_{y}_{y_prime}"
            N.add_edge(p_name,q_name)
            N.add_edge(q_name, x)
            N.add_edge(q_name, y_prime)

            # soll man die Edge zwischen p_name und x löschen? diese ist shortcut

            N.remove_edge(p_name,x)

        if not G.has_edge(y,x):
            
            # statt random choice, sollte hier der successor gewählt werden, der widerum x als best match hat

            # Alte Auswahl
            # x_prime = rng.choice([v for v in G.successors(y) if colors[v]==colors[x]])

            # neue Auswahl:
            # 1. reziproger best match (x->z & z->x)
            # 2. asymmetrischer best match (x->z)
            # 3. asymmetrischer best match (z->x)
            # 4. irgendein y' != y


            candidates = []
            candidates = [v for v in G.successors(y) if colors[v] == colors[x] and G.has_edge(v,y)]

            if not candidates:
                candidates = [v for v in G.successors(y) if colors[v] == colors[x]]

            if not candidates:
                candidates = [v for v in G.predecessors(y) if colors[v] == colors[x] and v != x]

            if not candidates:
                candidates = [v for v in G.nodes if colors[v] == colors[x] and v != x]

            x_prime = rng.choice(candidates)


            ## insert q_yx'' below p_xy
            q_name = f"q_{y}_{x}_{x_prime}"
            N.add_edge(p_name, q_name)
            N.add_edge(q_name, y)
            N.add_edge(q_name, x_prime)

            # soll man die Edge zwischen p_name und y löschen? diese ist shortcut

            N.remove_edge(p_name,y)
                          
    # return network
    return N

