# %%
import random
import asymmetree.treeevolve as te
from asymmetree.visualization.tree_vis import visualize, assign_colors
from asymmetree.analysis import orthology_from_tree, bmg_from_tree
import networkx as nx
from tralda.datastructures.tree import TreeNode
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# generate Species Tree

S = te.species_tree_n(n = 2)

# generate Gene Tree

dated_gene_tree = te.dated_gene_tree(
    S,
    dupl_rate=0.5,
    loss_rate=0.1,
    hgt_rate=0,
    dupl_polytomy=0.5
)

full_gene_tree = te.rate_heterogeneity(
    dated_gene_tree,
    S,
    base_rate=0.5,
    autocorr_variance=0.2,
)

# prune all loss branches and the planted root
pruned_gene_tree = te.prune_losses(full_gene_tree)

species_colors, gene_colors = assign_colors(S, dated_gene_tree)

visualize(S, color_dict=species_colors)

# visualize(dated_gene_tree, color_dict=gene_colors)
# visualize(full_gene_tree, color_dict=gene_colors)
visualize(pruned_gene_tree, color_dict=gene_colors)

# bmg, rbmg = bmg_from_tree(full_gene_tree, supply_rbmg=True)
# nx.draw(bmg,with_labels=True)


G, root = pruned_gene_tree.to_nx()


# %%
def insertHybrid(DiGraph):
    # n einfügen? um mehrere Hybridization events zuzlassen?

    # max label herausfinden
    label = max(nx.get_node_attributes(DiGraph,"label").values())+1

    # über max(dist) den Zeitbereich herausfinden

    timerange = max(nx.get_node_attributes(DiGraph,"tstamp").values())

    # random Zeitpunkt auswählen

    time = random.uniform(0,timerange)

    # edges finden, die zu dieser Zeit existiert haben.

    possibleEdges = set(edge for edge in DiGraph.edges if DiGraph.nodes[edge[0]]["tstamp"] >= time and DiGraph.nodes[edge[1]]["tstamp"] <= time)

    # eine zufällige Edge auswählen, diese durch einen Hybrid erweitern.
    # remove_edge(Parent,Child) 
    # add_edges_from((Parent,Hybrid),(Hybrid,Child))

    # eine zweite Edge wählen, die den Zeitpunkt enthält und nicht den gleichen Parent hat.
    # Child2 auswählen aus allen successors der Edge0
    # add_edge(Hybrid,Child2)

    edges = random.sample(sorted(possibleEdges),2)

    # Ausgangsspezies bestimmen
    # parentspecies = [DiGraph.nodes[parent[0]]["reconc"] for parent in edges]

    #
    DiGraph.add_node(label,
                    label = label,
                    event = 'H',
                    # reconc = 1, # gibt an zu welcher Spezies es gehört
                    tstamp = time,
                    # transferred = ,
                    dist = 0.0
                    )
    
    for parent, child in edges:
        DiGraph.remove_edge(parent,child)
        DiGraph.add_edge(parent,label)
        DiGraph.add_edge(label,child)


# Positionsfunktion, wäre schön, wenn die y Achse vom Zeitpunkt abhängig wäre

def hierarchy_pos(G, root, level_gap=1.0, node_gap=1.0):
    pos = {}
    def _pos(node, x, y, width):
        pos[node] = (x, y)
        children = list(G.successors(node))
        if children:
            dx = width / len(children)
            x_start = x - width/2 + dx/2
            for child in children:
                _pos(child, x_start, y - level_gap, dx)
                x_start += dx
    _pos(root, 0, 0, node_gap * len(G.nodes))
    return pos



# %%
insertHybrid(G)

# %%   Diagramm zeichnen und Nodes ausgeben

# ── Labels: node.label Attribut ──────────────────────────
labels = {n: G.nodes[n]['label'] for n in G.nodes}

pos = hierarchy_pos(G, root)

# ── Farben: nach reconc (Spezies) ────────────────────────
# Alle einzigartigen Spezies-IDs sammeln
# species = list(set(G.nodes[n]['reconc'] for n in G.nodes))

# Jeder Spezies eine Farbe zuweisen
# cmap = cm.get_cmap('tab10', len(species))
# species_color = {s: cmap(i) for i, s in enumerate(species)}

# node_colors = [species_color[G.nodes[n]['reconc']] for n in G.nodes]


# ── Plot ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

nx.draw(G,pos= pos,
        labels=labels,
        # node_color=node_colors,
        node_size=600,
        arrows=True,
        ax=ax)

plt.title('Genbaum')
plt.show()

# for node in G.nodes(data=True):
#     print(node)