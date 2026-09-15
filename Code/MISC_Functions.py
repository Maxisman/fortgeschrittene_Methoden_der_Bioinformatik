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
    speciesTree = te.species_tree_n_age(
        age = 0.5,
        n = nSpecies
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


def biccherry(G: nx.DiGraph):
    BCN = nx.DiGraph()
    BCN.add_node("rho")

    for leaf in G.nodes():
        BCN.add_node(leaf, color=G.nodes[leaf]["color"], label=leaf)

    if len(G.nodes()) == 2:
        for leaf in G.nodes():
            BCN.add_edge("rho", leaf)
        return BCN

    cherryPs = {}
    cherryQs = {}

    for x, y in itertools.combinations(G.nodes(), 2):
        if G.nodes[x]["color"] != G.nodes[y]["color"]:
            p_name = f"p_{x}_{y}"
            BCN.add_edge("rho", p_name)
            BCN.add_edge(p_name, x)
            BCN.add_edge(p_name, y)
            cherryPs[(x, y)] = p_name

    # Q-Extensions
    for (x, y), p_name in cherryPs.items():

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
                q_name = f"q_{x}_{z}"
                BCN.add_edge(p_name, q_name)
                BCN.add_edge(q_name, x)
                BCN.add_edge(q_name, z)
                cherryQs[(x, z)] = q_name

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
                q_name = f"q_{y}_{z}"
                BCN.add_edge(p_name, q_name)
                BCN.add_edge(q_name, y)
                BCN.add_edge(q_name, z)
                cherryQs[(y, z)] = q_name

    for (x, y), q_name in cherryQs.items():
    
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
                    r_name = f"r_{x}_{z}"
                    BCN.add_edge(q_name, r_name)
                    BCN.add_edge(r_name, x)
                    BCN.add_edge(r_name, z)
                    # cherryRs[(x, z)] = r_name
    
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
                    r_name = f"r_{y}_{z}"
                    BCN.add_edge(q_name, r_name)
                    BCN.add_edge(r_name, y)
                    BCN.add_edge(r_name, z)
                    # cherryRs[(y, z)] = q_name

    return BCN


def findCandidate(BMG: nx.DiGraph,x,y):
    # Suche nach einem besseren Match für x als y
    # zunächst wird geschaut, ob es einen Best Match für x gibt, der die egleiche Farbe wie y hat
    # wird davon keiner gefunden, wird Node z gewählt, mit gleicher Farbe wie y und dessen Best Match x ist
    # wenn davon keiner gefunden wird, wird irgendeine Node gewählt, die die gleiche Farbe wie y hat
    
    candidates = [
        z
        for z in BMG.successors(x)
        if BMG.nodes[z]["color"] == BMG.nodes[y]["color"]
    ]
    if not candidates:
        candidates = [
            z
            for z in BMG.predecessors(x)
            if BMG.nodes[z]["color"] == BMG.nodes[y]["color"] and z != y
        ]
    if not candidates:
        candidates = [
            z
            for z in BMG.nodes()
            if BMG.nodes[z]["color"] == BMG.nodes[y]["color"] and z != y
        ]

    z = random.choice(candidates)
    return z

def insertNode(BCN: nx.DiGraph,layer: int, namePrev, x, z):

    # hier muss noch ein umwandeln von layer(int) ind layer(str) stattfunden. 
    nameNew = f"{layer}_{x}_{z}"
    BCN.add_edge(namePrev, nameNew)
    BCN.add_edge(nameNew, x)
    BCN.add_edge(nameNew, z)
    if BCN.has_edge(namePrev,x):
        BCN.remove_edge(namePrev,x)

    return nameNew



def MultiLayerdBICCherry(BMG: nx.DiGraph, maxLayers: int = 20):
    BCN = nx.DiGraph()
    BCN.add_node("rho")

    cherryPs = {}
    currentDict = {}
    nextDict = {}
    for leaf in BMG.nodes():
        BCN.add_node(leaf, color= BMG.nodes[leaf]["color"], label=leaf)
    
    if len(BMG.nodes()) == 2:
        for leaf in BMG.nodes():
            BCN.add_edge("rho", leaf)
        return BCN

    # P-Layer
    for x, y in itertools.combinations(BMG.nodes(), 2):
        if BMG.nodes[x]["color"] != BMG.nodes[y]["color"]:
            p_name = f"p_{x}_{y}"
            BCN.add_edge("rho", p_name)
            BCN.add_edge(p_name, x)
            BCN.add_edge(p_name, y)
            cherryPs[(x, y)] = p_name

    # Q-Extensions
    for (x, y), p_name in cherryPs.items():

        if not BMG.has_edge(x,y):
            z = findCandidate(BMG, x, y)
            nodeName = insertNode(BCN, 1, p_name, x, z)
            currentDict[(x,z)] = nodeName

        if not BMG.has_edge(y,x):
            z = findCandidate(BMG, y, x)
            nodeName = insertNode(BCN, 1, p_name, y, z)
            currentDict[(y,z)] = nodeName

    # lower leayers
    # Es werden die gerade eingefügten Kanten (x->y) untersucht, ob diese einen Best-Match (y->x) generiert haben, der gar nicht da sein sollte.
    # Ist dies der Fall, wird für y->x eine neue Ebene eingefügt um diese zu trennen

    (BMG.edges() - bmg(BCN).edges())
    for layer in range(2,maxLayers):
        if nx.utils.graphs_equal(BMG, bmg(BCN)):
            break

        
        for (x,y), prevName in currentDict.items():
            if not BMG.has_edge(y,x):
                z = findCandidate(BMG, y, x)
                nodeName = insertNode(BCN, layer, prevName, y, z)
                nextDict[(y,z)] = nodeName

        layer += 1
        currentDict = copy.deepcopy(nextDict)

    return BCN
