import numpy as np
import asymmetree.treeevolve as te
import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import pydot

def generateTree(seed:int = None, nSpecies:int = 2):

    if seed:
        # Setze den Seed für Pythons Standard-Zufallsfunktionen
        random.seed(seed)
        # Setze den Seed für NumPys Zufallsfunktionen (wichtig für AsymmeTree)
        np.random.seed(seed)

    # species tree
    speciesTree = te.species_tree_n_age(
        age = 1.0,
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



def visualize_bmg(BMG, ax = None):
    sorted_nodes = sorted(BMG.nodes(), key=lambda n: (BMG.nodes[n].get('color', ''), n))
    pos = nx.circular_layout(sorted_nodes)
    
    # 1. Einzigartige Farb-Attribute (Labels) extrahieren
    unique_colors = sorted(list(set(BMG.nodes[n].get('color', '') for n in BMG.nodes())))
    
    # 2. Integrierte Colormap-Logik basierend auf der Anzahl der Farben
    if len(unique_colors) <= 10:
        cmap = plt.get_cmap("tab10")(np.arange(len(unique_colors), dtype=int))
    else:
        cmap = plt.get_cmap("jet")(np.linspace(0, 1.0, len(unique_colors)))

    # 3. Mapping-Dictionary (color_dict) aufbauen
    color_dict = {}
    for label, color in zip(unique_colors, cmap):
        color_dict[label] = color
        
    # 4. Farben in der korrekten Reihenfolge der sortierten Nodes zuweisen
    node_colors = [color_dict[BMG.nodes[n].get('color', '')] for n in sorted_nodes]

    if ax is None:
        ax = plt.gca()

    nx.draw(
        BMG, 
        pos=pos, 
        ax=ax,
        nodelist=sorted_nodes,      
        node_color=node_colors, 
        with_labels=True,
        node_size=600,
        font_color="black",
        font_weight="bold",
        edge_color="black",
        arrows=True,
        connectionstyle="arc3,rad=0.05"  # Biegt die Kanten
    )
    if ax:
        ax.set_aspect('equal')




def visualize_network(N, ax=None):
    pos = graphviz_layout(N, prog="dot")
    
    # 1. Einzigartige Farb-Attribute nur von den Blättern (out_degree == 0) extrahieren
    leaves = [n for n in N.nodes() if N.out_degree(n) == 0]
    unique_colors = sorted(list(set(N.nodes[n].get('color', '') for n in leaves)))
    
    # 2. Colormap-Logik für die Blätter anwenden
    if len(unique_colors) <= 10:
        cmap = plt.get_cmap("tab10")(np.arange(len(unique_colors), dtype=int))
    else:
        cmap = plt.get_cmap("jet")(np.linspace(0, 1.0, len(unique_colors)))

    color_dict = {label: color for label, color in zip(unique_colors, cmap)}
    
    # 3. Farbzuweisung: Innere Knoten (Grau), Blätter (aus color_dict)
    node_colors = []
    for n in N.nodes():
        if N.out_degree(n) > 0:
            node_colors.append("gray")
        else:
            node_colors.append(color_dict.get(N.nodes[n].get('color', ''), "black"))

    # 4. Graphen zeichnen (geradlinige Kanten, da connectionstyle fehlt)
    if ax is None:
        ax = plt.gca()

    nx.draw(
        N, 
        pos=pos, 
        ax=ax,
        node_color=node_colors, 
        with_labels=True,
        node_size=600,
        font_color="white",
        font_weight="bold",
        edge_color="black",
        arrows=True
    )


def visualize_BCN(BCN, ax=None):
    # 1. Knoten den 4 Ebenen zuordnen
    roots = [n for n in BCN.nodes() if BCN.in_degree(n) == 0]
    rho = roots[0] if roots else "rho"
    
    p_nodes = set(BCN.successors(rho)) if rho in BCN else set()
    leaves = set(n for n in BCN.nodes() if BCN.out_degree(n) == 0)
    q_nodes = set(BCN.nodes()) - set(roots) - p_nodes - leaves

    # 2. Graph in pydot umwandeln und rank="same" für jede Ebene erzwingen
    pydot_graph = nx.nx_pydot.to_pydot(BCN)
    
    for level_nodes in [p_nodes, q_nodes, leaves]:
        if level_nodes:
            subgraph = pydot.Subgraph(rank='same')
            for n in level_nodes:
                subgraph.add_node(pydot.Node(str(n)))
            pydot_graph.add_subgraph(subgraph)

    # 3. Graphviz berechnet die X-Positionen nun unter Berücksichtigung der festen Ebenen
    raw_pos = graphviz_layout(pydot_graph, prog="dot")

    # 4. Y-Koordinaten auf die 4 festen Ebenen zuweisen (3, 2, 1, 0)
    pos = {}
    for node_key, (x, _) in raw_pos.items():
        # pydot wandelt Knotennamen teils in Strings um; hier wieder auf den Originalknoten mappen
        node = node_key
        if node not in BCN:
            for orig_node in BCN.nodes():
                if str(orig_node) == str(node_key):
                    node = orig_node
                    break

        if node in roots:
            y = 3.0
        elif node in p_nodes:
            y = 2.0
        elif node in q_nodes:
            y = 1.0
        else:
            y = 0.0
        pos[node] = (x, y)

    # 5. Colormap-Logik für die Blätter
    unique_colors = sorted(list(set(BCN.nodes[n].get('color', '') for n in leaves)))
    
    if len(unique_colors) <= 10:
        cmap = plt.get_cmap("tab10")(np.arange(len(unique_colors), dtype=int))
    else:
        cmap = plt.get_cmap("jet")(np.linspace(0, 1.0, len(unique_colors)))

    color_dict = {label: color for label, color in zip(unique_colors, cmap)}
    
    # 6. Farben zuweisen: Innere Knoten (grau), Blätter (bunt)
    node_colors = []
    for n in BCN.nodes():
        if n in leaves:
            node_colors.append(color_dict.get(BCN.nodes[n].get('color', ''), "black"))
        else:
            node_colors.append("gray")

    # 7. Graph zeichnen
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 10))

    nx.draw(
        BCN, 
        pos=pos, 
        ax=ax,
        node_color=node_colors, 
        with_labels=True,
        node_size=600,
        font_color="white",
        font_weight="bold",
        edge_color="black",
        arrows=True
    )