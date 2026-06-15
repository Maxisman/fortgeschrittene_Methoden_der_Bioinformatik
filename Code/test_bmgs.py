import asymmetree.treeevolve as te
from asymmetree.visualization.tree_vis import visualize, assign_colors
import bmg_fun
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from collections import defaultdict
import random
import matplotlib.gridspec as gridspec

S = te.species_tree_n_age(
    10, 1.0, contraction_probability=0.0, contraction_proportion=0.2, contraction_bias="exponential"
)
T = te.dated_gene_tree(
    S, dupl_rate=1.0, loss_rate=0, hgt_rate=0.2, gc_rate=0.2, prohibit_extinction="per_species"
)
# prune all loss branches and the planted root
observable_gene_tree = te.prune_losses(T)

species_colors, gene_colors = assign_colors(S, observable_gene_tree)
print(gene_colors.keys())

#visualize(S, color_dict=species_colors) #, save_as="testfile_speciestree.pdf")
visualize(observable_gene_tree, color_dict=gene_colors) #, save_as="testfile_genetree.pdf")
G = bmg_fun.convert_to_nx(observable_gene_tree)


BMG = bmg_fun.compute_bmg(G, gene_colors)

# reverse dict so every color has a list of leaves attached to it, for visualization
color_to_keys = defaultdict(list)
for key, color in gene_colors.items():
    color_to_keys[tuple(color)].append(key)

# visualize networkx graph and full BMG
fig, axes = plt.subplots(2, 1, figsize=(4, 10))
pos = graphviz_layout(G, prog="dot")
nx.draw(G, pos, nodelist=list(G.nodes) - gene_colors.keys(), ax=axes[0])
for color, node_list in color_to_keys.items():
    nx.draw(G, pos, nodelist=node_list, node_color = color, ax=axes[0], with_labels=True)

for color, node_list in color_to_keys.items():
    nx.draw(BMG, nx.circular_layout(BMG), nodelist=node_list, node_color = color, ax=axes[1], with_labels=True)
#nx.draw(BMG, nx.circular_layout(BMG), ax=axes[1], with_labels=True)
plt.show()

# visualize networkx graph and edges from three randomly selected nodes of BMG
fig = plt.figure(figsize=(12, 10))
gs = gridspec.GridSpec(2, 3, figure=fig)

# Top row: spanning all 3 columns
ax_graph = fig.add_subplot(gs[0, :])  # the colon means "all columns"
pos = graphviz_layout(G, prog="dot")
nx.draw(G, pos, nodelist=list(G.nodes) - gene_colors.keys(), ax=ax_graph)
for color, node_list in color_to_keys.items():
    nx.draw(G, pos, nodelist=node_list, node_color = color, ax=ax_graph, with_labels=True)

# select three random nodes from gene_colors.keys
for i, starting_node in enumerate(random.sample(list(gene_colors.keys()), 3)):
    # create edge list for starting node
    end_nodes = BMG.successors(starting_node)
    edge_list = [(starting_node,b) for b in end_nodes]
    current_ax = fig.add_subplot(gs[1, i])
    current_ax.set_title(f"Best matches of {starting_node}")
    for color, node_list in color_to_keys.items():
        nx.draw(BMG, nx.circular_layout(BMG), edgelist=edge_list, nodelist=node_list, node_color = color, ax=current_ax, with_labels=True)

plt.show()