import numpy as np
import asymmetree.treeevolve as te
import random
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
import pydot

import shlex
import subprocess


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
        font_color="black",
        font_weight="bold",
        edge_color="black",
        arrows=True
    )


def _dot_quote(s) -> str:
    return '"' + str(s).replace('"', '\\"') + '"'
 
 
def _classify_bcn_nodes(BCN: nx.DiGraph):
    """
    Klassifiziert die Knoten eines Standard-BIC-Cherry-Netzwerks (nur P-
    und Q-Ebene) in rho, p_nodes, q_nodes, leaves.
 
    Wirft ValueError, falls die Struktur nicht genau diesem 4-Ebenen-Schema
    entspricht (z.B. bei einem Multi-Layer-BCN mit weiteren R-/S-/...-
    Knoten) -- diese Funktion ist bewusst nur fuer "Standard"-BCNs gedacht.
    """
    roots = [n for n in BCN.nodes() if BCN.in_degree(n) == 0]
    if len(roots) != 1:
        raise ValueError(f"Erwarte genau eine Wurzel (in_degree==0), gefunden: {roots}")
    rho = roots[0]
 
    leaves = {n for n in BCN.nodes() if BCN.out_degree(n) == 0}
    if not leaves:
        raise ValueError("Keine Blaetter (out_degree==0) gefunden.")
 
    p_nodes = set(BCN.successors(rho)) - leaves
    q_nodes = set(BCN.nodes()) - {rho} - p_nodes - leaves
 
    for p in p_nodes:
        for child in BCN.successors(p):
            if child not in leaves and child not in q_nodes:
                raise ValueError(
                    f"P-Knoten {p!r} hat ein Kind {child!r}, das weder Blatt noch "
                    f"Q-Knoten ist -- das ist kein Standard-P+Q-BCN (evtl. Multi-Layer?)."
                )
    for q in q_nodes:
        if any(p not in p_nodes for p in BCN.predecessors(q)):
            raise ValueError(f"Q-Knoten {q!r} haengt nicht ausschliesslich an P-Knoten.")
        for child in BCN.successors(q):
            if child not in leaves:
                raise ValueError(
                    f"Q-Knoten {q!r} hat ein Kind {child!r}, das kein Blatt ist -- "
                    f"das ist kein Standard-P+Q-BCN (evtl. Multi-Layer?)."
                )
 
    return rho, p_nodes, q_nodes, leaves
 
 
def _dot_layout_with_ranks(BCN: nx.DiGraph, rank_groups: list) -> dict:
    """
    Ruft `dot` mit expliziten rank=same-Gruppen auf (top-to-bottom in der
    gegebenen Reihenfolge) und liefert {node: (x, y)} zurueck. `dot`
    uebernimmt dabei sowohl die vorgegebene Ebeneneinteilung als auch die
    kreuzungsarme horizontale Anordnung innerhalb jeder Ebene.
    """
    lines = ["digraph G {", "rankdir=TB;", "nodesep=0.4;", "ranksep=1.1;"]
    for group in rank_groups:
        if not group:
            continue
        names = " ".join(_dot_quote(n) for n in sorted(group, key=str))
        lines.append(f"{{rank=same; {names};}}")
    for u, v in BCN.edges():
        lines.append(f"{_dot_quote(u)} -> {_dot_quote(v)};")
    lines.append("}")
    dot_source = "\n".join(lines)
 
    result = subprocess.run(
        ["dot", "-Tplain"], input=dot_source, capture_output=True, text=True, check=True
    )
 
    pos = {}
    for line in result.stdout.splitlines():
        parts = shlex.split(line)
        if parts and parts[0] == "node":
            name = parts[1]
            pos[name] = (float(parts[2]), float(parts[3]))
    return pos
 
 
def visualize_BCN(
    BCN: nx.DiGraph,
    ax=None,
    figsize=(14, 8),
    leaf_font_size=9,
    internal_font_size=6,
    show_internal_labels=True,
    save_path=None,
):
    """
    Zeichnet ein STANDARD-BIC-Cherry-Netzwerk (nur P- und Q-Ebene) in
    exakt vier vertikalen Ebenen: rho (zentriert), P-Knoten, Q-Knoten,
    farbige Blaetter -- horizontal kreuzungsarm via `dot` mit expliziten
    rank=same-Vorgaben angeordnet.
 
    Fuer Multi-Layer-BCNs (mit R-/S-/...-Knoten, siehe MLBCEA) wirft diese
    Funktion einen ValueError -- dafuer braeuchte es eine Variante mit
    variabler Ebenenzahl.
 
    Parameters
    ----------
    BCN : networkx.DiGraph
        Das zu zeichnende BIC-Cherry-Netzwerk. Blaetter brauchen ein
        "color"-Attribut.
    ax : matplotlib.axes.Axes, optional
        Falls gegeben, wird darauf gezeichnet statt eine neue Figure zu
        erstellen.
    show_internal_labels : bool
        Ob P-/Q-Knotennamen mit angezeigt werden (meist unleserlich lang,
        daher Default False).
    save_path : str, optional
        Falls gegeben, wird die Figure dorthin gespeichert.
 
    Returns
    -------
    ax : matplotlib.axes.Axes
    """
    rho, p_nodes, q_nodes, leaves = _classify_bcn_nodes(BCN)
 
    rank_groups = [[rho], p_nodes, q_nodes, leaves]
    pos = _dot_layout_with_ranks(BCN, rank_groups)
 
    if ax is None:
        _, ax = plt.subplots(figsize=figsize)
 
    # --- Farben fuer Blaetter ---
    leaf_colors_raw = sorted({BCN.nodes[l]["color"] for l in leaves}, key=str)
    palette = plt.cm.tab10.colors
    color_map = {c: palette[i % len(palette)] for i, c in enumerate(leaf_colors_raw)}
 
    # --- Kanten zeichnen ---
    for u, v in BCN.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        ax.plot([x1, x2], [y1, y2], color="#999999", linewidth=0.8, zorder=1)
 
    # --- Knoten zeichnen ---
    def draw_nodes(nodes, color, size, label_fn=None, font_size=8):
        for n in nodes:
            x, y = pos[n]
            ax.scatter(x, y, s=size, color=color, edgecolors="black",
                       linewidths=0.6, zorder=2)
            if label_fn is not None:
                ax.annotate(label_fn(n), (x, y), textcoords="offset points",
                            xytext=(0, -size ** 0.5 - 6), ha="center",
                            va="top", fontsize=font_size, zorder=3)
 
    draw_nodes([rho], "black", 120)
    draw_nodes(p_nodes, "#DDDDDD", 90,
               label_fn=(lambda n: n) if show_internal_labels else None,
               font_size=internal_font_size)
    draw_nodes(q_nodes, "#AAAAAA", 90,
               label_fn=(lambda n: n) if show_internal_labels else None,
               font_size=internal_font_size)
    for leaf in leaves:
        x, y = pos[leaf]
        ax.scatter(x, y, s=260, color=color_map[BCN.nodes[leaf]["color"]],
                   edgecolors="black", linewidths=0.8, zorder=2)
        ax.annotate(str(leaf), (x, y), ha="center", va="center",
                    fontsize=leaf_font_size, fontweight="bold", zorder=3)
 
    # --- Legende fuer Blattfarben ---
    handles = [
        plt.Line2D([0], [0], marker="o", linestyle="", markersize=10,
                   markerfacecolor=color_map[c], markeredgecolor="black", label=str(c))
        for c in leaf_colors_raw
    ]
 
    ax.set_axis_off()
    plt.tight_layout()
 
    if save_path:
        plt.savefig(save_path, dpi=150)
 
    return ax
