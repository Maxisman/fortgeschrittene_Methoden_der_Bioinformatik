import numpy as np
import asymmetree.treeevolve as te
import random
import networkx as nx
import matplotlib.pyplot as plt
import pydot
import shlex
import subprocess
import itertools

from collections import defaultdict
from networkx.drawing.nx_pydot import graphviz_layout
from bmg_Tony import bmg


# ======================================================================================
#  generateGeneTree_max_leaves - generiert einen zufälligen Genbaum mit maximaler Anzahl an Blättern
# ======================================================================================

def generateGeneTree_maxLeaves(seed: int = None, nSpecies: int = 2, max_leaves: int = 5):

    if seed:
        # Setze den Seed für Pythons Standard-Zufallsfunktionen
        random.seed(seed)
        # Setze den Seed für NumPys Zufallsfunktionen (wichtig für AsymmeTree)
        np.random.seed(seed)

    while True:

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

        nLeaves = len(list(geneTree.leaves()))
        if nLeaves < max_leaves and nLeaves > 2 and nLeaves >= nSpecies:  #wenn es nur zwei Blätter (oder nSpezies?????) gibt, so lassen sich keine Hybriden einfügen
            break

    return speciesTree, geneTree




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


def lcas_multiple_nodes(N: nx.DiGraph, nodes: set) -> set:
    if not nodes:
        return set()

    # Vorfahren jedes Knotens (inkl. des Knotens selbst)
    ancestor_sets = [nx.ancestors(N, node) | {node} for node in nodes]

    # Gemeinsame Vorfahren aller Knoten
    common_ancestors = set.intersection(*ancestor_sets)

    # Teilgraph der gemeinsamen Vorfahren
    sub = N.subgraph(common_ancestors)

    # LCAs: gemeinsame Vorfahren ohne ausgehende Kanten im Teilgraphen,
    # d.h. kein anderer gemeinsamer Vorfahre liegt "unter" ihnen
    return {anc for anc in common_ancestors if sub.out_degree(anc) == 0}




def contract_nodes(RBC: nx.DiGraph):

    bmg_RBC = bmg(RBC,'weak')
    inner_nodes = [node for node in RBC.nodes if RBC.out_degree(node) > 0 and RBC.in_degree(node) > 0]
    for node1, node2 in itertools.combinations(inner_nodes, 2):

        # Knoten könnte durch eine frühere, akzeptierte Änderung schon entfernt worden sein
        if not RBC.has_node(node1) or not RBC.has_node(node2):
            continue

        if (set(RBC.predecessors(node1)) == set(RBC.predecessors(node2))
                and RBC.out_degree(node1) > 0
                and RBC.out_degree(node2) > 0):

            RBC2 = RBC.copy()   # echte, unabhängige Kopie

            for successor in RBC.successors(node1):
                RBC2.add_edge(node2, successor)
            RBC2.remove_node(node1)

            bmg_RBC2 = bmg(RBC2, 'weak')

            if nx.utils.graphs_equal(bmg_RBC, bmg_RBC2):
                RBC = RBC2              # Änderung übernehmen

            # sonst: RBC2 wird einfach verworfen
    return RBC




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
 
    return _draw_bcn(
        BCN, pos, rho, p_nodes, q_nodes, leaves, ax, figsize,
        leaf_font_size, internal_font_size, show_internal_labels, save_path,
    )
 
 
def visualize_easyBCN(
    BCN: nx.DiGraph,
    ax=None,
    figsize=(14, 8),
    leaf_font_size=9,
    internal_font_size=6,
    show_internal_labels=True,
    save_path=None,
    min_gap=None,
):
    """
    Variante von visualize_BCN fuer "einfache" BCNs: rho, P-Knoten und
    Blaetter werden weiterhin wie gehabt ueber `dot` (kreuzungsminimiert)
    positioniert -- aber die Q-Knoten werden NICHT von `dot` platziert,
    sondern explizit auf den x-Mittelpunkt ihrer beiden Kinder (Blaetter)
    gesetzt. Dadurch sitzt jeder Q-Knoten optisch direkt zwischen den
    beiden Blaettern, die er verbindet, statt an einer von `dot` frei
    gewaehlten Position irgendwo in der Q-Reihe.
 
    Ueberlappungen zwischen Q-Knoten werden per Links-nach-rechts-Sweep
    vermieden: Q-Knoten werden nach ihrem gewuenschten Mittelpunkt
    sortiert und, falls noetig, minimal nach rechts verschoben (Mindest-
    abstand min_gap, per Default automatisch aus dem Blattabstand
    abgeleitet).
 
    Bei sehr dichten Netzwerken (viele Q-Knoten mit aehnlichen Mittel-
    punkten) kann diese Sweep-Korrektur einzelne Q-Knoten spuerbar von
    ihrem "idealen" Mittelpunkt wegschieben -- siehe visualize_BCN fuer
    eine Variante, die stattdessen komplett auf dots eigene Kreuzungs-
    minimierung fuer die Q-Ebene setzt (dort gibt es dieses Problem
    strukturell nicht, dafuer sitzen Q-Knoten nicht zwingend mittig).
 
    Parameters
    ----------
    min_gap : float, optional
        Mindestabstand zwischen zwei Q-Knoten. Default: automatisch als
        60% des minimalen Blattabstands in der untersten Ebene.
 
    Returns
    -------
    ax : matplotlib.axes.Axes
    """
    rho, p_nodes, q_nodes, leaves = _classify_bcn_nodes(BCN)
 
    rank_groups = [[rho], p_nodes, q_nodes, leaves]
    pos = _dot_layout_with_ranks(BCN, rank_groups)
 
    if q_nodes:
        q_row_y = pos[next(iter(q_nodes))][1]
 
        if min_gap is None:
            leaf_xs = sorted(pos[l][0] for l in leaves)
            gaps = [b - a for a, b in zip(leaf_xs, leaf_xs[1:]) if b - a > 1e-9]
            min_gap = 0.6 * (min(gaps) if gaps else 50.0)
 
        # Sortierschluessel: (1) Blattpaar-Mittelpunkt -- Q-Knoten fuer
        # unterschiedliche Blattpaare werden dadurch schon grob in der
        # richtigen Reihenfolge einsortiert. (2) x-Position des Eltern-
        # P-Knotens als Tie-Breaker: haengen mehrere Q-Knoten am SELBEN
        # Blattpaar (weil ein Blatt gegenueber mehreren gleichfarbigen
        # Zielen korrigiert werden musste und dabei zufaellig derselbe
        # Kandidat gezogen wurde), werden sie in der horizontalen
        # Reihenfolge ihrer jeweiligen Eltern-P-Knoten angeordnet -- das
        # vermeidet unnoetige Kreuzungen der P->Q-Kanten. (3) q selbst
        # nur als letzter, rein deterministischer Tie-Breaker.
        def sort_key(q):
            children = list(BCN.successors(q))
            mid_x = sum(pos[c][0] for c in children) / len(children)
            parent = next(iter(BCN.predecessors(q)))
            return (mid_x, pos[parent][0], str(q))
 
        desired = sorted(((sort_key(q)[0], q) for q in q_nodes), key=lambda t: sort_key(t[1]))
 
        prev_x = None
        for mid_x, q in desired:
            x = mid_x if prev_x is None else max(mid_x, prev_x + min_gap)
            pos[q] = (x, q_row_y)
            prev_x = x
 
    return _draw_bcn(
        BCN, pos, rho, p_nodes, q_nodes, leaves, ax, figsize,
        leaf_font_size, internal_font_size, show_internal_labels, save_path,
    )
 
 
def _draw_bcn(
    BCN, pos, rho, p_nodes, q_nodes, leaves, ax, figsize,
    leaf_font_size, internal_font_size, show_internal_labels, save_path,
):
    """Gemeinsame Zeichenlogik fuer visualize_BCN und visualize_easyBCN --
    erwartet fertige (x,y)-Positionen fuer alle Knoten in `pos`."""
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
        ax.scatter(x, y, s=600, color=color_map[BCN.nodes[leaf]["color"]],
                   # edgecolors="black", linewidths=0.8,
                   zorder=2)
        ax.annotate(str(leaf), (x, y), ha="center", va="center",
                    fontsize=leaf_font_size, fontweight="bold", zorder=3)
 
    # --- Legende fuer Blattfarben ---
    handles = [
        plt.Line2D([0], [0], marker="o", linestyle="", markersize=10,
                   markerfacecolor=color_map[c], markeredgecolor="black", label=str(c))
        for c in leaf_colors_raw
    ]
    # ax.legend(handles=handles, title="Farbe", loc="upper right", fontsize=9)
 
    ax.set_axis_off()
    # ax.set_title(
    #     f"BIC-Cherry-Netzwerk  (rho=1, P={len(p_nodes)}, Q={len(q_nodes)}, "
    #     f"Blaetter={len(leaves)})"
    # )
    plt.tight_layout()
 
    if save_path:
        plt.savefig(save_path, dpi=150)
 
    return ax