import numpy as np
import asymmetree.treeevolve as te
import matplotlib.pyplot as plt
import networkx as nx
import random
import copy
import itertools

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


def extend_cherry(
    BCN: nx.DiGraph, p_name: str, x: str, z: str, q_counter: int) -> int:
    current_parent = None
    for pred in BCN.predecessors(x):
        if pred == p_name or nx.has_path(BCN, p_name, pred):
            current_parent = pred
            break

    if current_parent is None:
        return q_counter

    q_name = f"q_{x}_{z}_{q_counter}"

    BCN.add_edge(current_parent, q_name)
    BCN.add_edge(q_name, x)
    BCN.add_edge(q_name, z)

    BCN.remove_edge(current_parent, x)

    # if BCN.has_edge(pred,z):
    #     BCN.remove_edge(pred,z)

    return q_counter + 1


def biccherry(G: nx.DiGraph):
    BCN = nx.DiGraph()
    BCN.add_node("rho")

    for leaf in G.nodes():
        BCN.add_node(leaf, color=G.nodes[leaf]["color"], label=leaf)

    if len(G.nodes()) == 2:
        for leaf in G.nodes():
            BCN.add_edge("rho", leaf)
        return BCN

    cherryParents = {}
    q_counter = 0

    for x, y in itertools.combinations(G.nodes(), 2):
        if G.nodes[x]["color"] != G.nodes[y]["color"]:
            p_name = f"p_{x}_{y}"
            BCN.add_edge("rho", p_name)
            BCN.add_edge(p_name, x)
            BCN.add_edge(p_name, y)
            cherryParents[(x, y)] = p_name

    for (x, y), p_name in cherryParents.items():

        # --- Richtung x -> y ---
        if not G.has_edge(x, y):
            candidates = [
                z
                for z in G.successors(x)
                if G.nodes[z]["color"] == G.nodes[y]["color"]
            ]
            if not candidates:
                candidates = [
                    z
                    for z in G.predecessors(x)
                    if G.nodes[z]["color"] == G.nodes[y]["color"] and z != y
                ]
            if not candidates:
                candidates = [
                    z
                    for z in G.nodes()
                    if G.nodes[z]["color"] == G.nodes[y]["color"] and z != y
                ]

            if candidates:
                z = random.choice(candidates)
                q_counter = extend_cherry(BCN, p_name, x, z, q_counter)

        # --- Richtung y -> x ---
        if not G.has_edge(y, x):
            candidates = [
                z
                for z in G.successors(y)
                if G.nodes[z]["color"] == G.nodes[x]["color"]
            ]
            if not candidates:
                candidates = [
                    z
                    for z in G.predecessors(y)
                    if G.nodes[z]["color"] == G.nodes[x]["color"] and z != x
                ]
            if not candidates:
                candidates = [
                    z
                    for z in G.nodes()
                    if G.nodes[z]["color"] == G.nodes[x]["color"] and z != x
                ]

            if candidates:
                z = random.choice(candidates)
                q_counter = extend_cherry(BCN, p_name, y, z, q_counter)

    return BCN