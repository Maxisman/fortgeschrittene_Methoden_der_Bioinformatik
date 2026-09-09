import numpy as np
import asymmetree.treeevolve as te
import matplotlib.pyplot as plt
import networkx as nx
import random
import copy

from networkx.drawing.nx_pydot import graphviz_layout
from asymmetree.visualization.tree_vis import assign_colors
from insert_hybrid import insertHybrid
from bmg_Tony import bmg, bmg_fast
from BICcherryRestrict import BICcherryRestrict
from bmg_fun import convert_to_nx

def generateTree(seed:int = None, nSpecies:int = 2):

    if seed:
        # Setze den Seed für Pythons Standard-Zufallsfunktionen
        random.seed(seed)
        # Setze den Seed für NumPys Zufallsfunktionen (wichtig für AsymmeTree)
        np.random.seed(seed)

    # species tree
    speciesTree = te.species_tree_n(
        n= nSpecies
        #, contraction_probability=0.0, contraction_proportion=0.2, contraction_bias="exponential"
    )
    # gene tree
    T = te.dated_gene_tree(
        speciesTree, dupl_rate=1.0, loss_rate=0, hgt_rate=0.2, gc_rate=0.2, prohibit_extinction="per_species", dupl_polytomy=0.5
    )
    # prune all loss branches and the planted root
    geneTree = te.prune_losses(T)
    
    return speciesTree, geneTree


def breakBMG(seed:int,nSpecies:int=2,mode:str = "weak"):

    speciesTree, geneTree = generateTree(seed,nSpecies)

    # get color dicts
    species_colors, gene_colors = assign_colors(speciesTree, geneTree)

    # convert to networkx
    Tree = convert_to_nx(geneTree)

    # Original BMG:
    BMG = bmg(Tree)
    BC = BICcherryRestrict(BMG)
    BMGBC = bmg(BC)

    # Testen, wie viele Hybride man einfügen kann, bevor die beiden BMGs nicht mehr übereinstimmen
    random.seed(seed)
    count = 0
    Network = copy.deepcopy(Tree)
    BMG = bmg(Tree)
    BC = BICcherryRestrict(BMG)
    BMGBC = bmg(BC)

    while nx.utils.graphs_equal(BMG, BMGBC) and count < 1000:
        Network = insertHybrid(Network)
        BMG = bmg(Network, mode = mode)
        BC = BICcherryRestrict(BMG)
        BMGBC = bmg(BC, mode = mode)
        count += 1
        if count % 10 == 0:
            print("Count = ",count)

    print("Es konnten",count,"Hybride eingefügt werden, bevor die BMGs nicht mehr übereinstimmten")

    # gene color dict turn keys to strings
    gene_colors_str = {str(k): v for k, v in gene_colors.items()}

    # visualize tree and network
    fig, axes = plt.subplots(2, 2, figsize=(25, 20))

    pos = graphviz_layout(Network, prog="dot")
    nodes_list = [v for v in Network.nodes()]
    nodes_colors = [gene_colors_str.get(v, "grey") for v in nodes_list]

    nx.draw(Network, pos, nodelist=nodes_list, node_color= nodes_colors, with_labels = True, ax=axes[0,0])
    axes[0,0].set_title("Network")

    pos = graphviz_layout(BC, prog="dot")
    nodes_list = [v for v in BC.nodes()]
    nodes_colors = [gene_colors_str.get(v, "grey") for v in nodes_list]
    nx.draw(BC, pos, nodelist=nodes_list, node_color= nodes_colors, with_labels = True, ax=axes[0,1])
    axes[0,1].set_title("BC")


    nodes_list = [v for v in BMG.nodes()]
    nodes_colors = [gene_colors_str.get(v, "grey") for v in nodes_list]
    axes[1,0].set_title("BMG")
    nx.draw(BMG, nx.circular_layout(BMG), nodelist=nodes_list, node_color= nodes_colors, ax=axes[1,0], with_labels=True)


    nodes_list = [v for v in BMGBC.nodes()]
    nodes_colors = [gene_colors_str.get(v, "grey") for v in nodes_list]
    axes[1,1].set_title("BMGBC")
    nx.draw(BMGBC, nx.circular_layout(BMG), nodelist=nodes_list, node_color= nodes_colors, ax=axes[1,1], with_labels=True)


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
            y_prime = rng.choice([v for v in G.successors(x) if colors[v]==colors[y]])
            ## insert q_xy' below p_xy
            q_name = f"q_{x}_{y}_{y_prime}"
            N.add_edge(p_name,q_name)
            N.add_edge(q_name, x)
            N.add_edge(q_name, y_prime)

            
            ### Test ob das was verbessert oder alles kaputt macht
            if N.has_edge(p_name,x):
                N.remove_edge(p_name,x)

            if nx.utils.graphs_equal(G,bmg_fast(N)):
                return N


        if not G.has_edge(y,x):
            x_prime = rng.choice([v for v in G.successors(y) if colors[v]==colors[x]])
            ## insert q_yx'' below p_xy
            q_name = f"q_{y}_{x}_{x_prime}"
            N.add_edge(p_name, q_name)
            N.add_edge(q_name, y)
            N.add_edge(q_name, x_prime)

            
            ### Test ob das was verbessert oder alles kaputt macht
            if N.has_edge(p_name,y):
                N.remove_edge(p_name,y)

            if nx.utils.graphs_equal(G,bmg_fast(N)):
                return N

    if not nx.utils.graphs_equal(G,bmg_fast(N)):
        print("leider konnte nicht der Richtige BMG generiert werden")
    # return network
    return N