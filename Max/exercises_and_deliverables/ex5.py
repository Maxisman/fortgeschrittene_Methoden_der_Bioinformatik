import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph([("roh", "v"), ("roh", "u"), ("u", "y"), ("u", "x"), ("v", "x")])

print(nx.is_directed_acyclic_graph(G))
for i in nx.topological_sort(G):
    print(i)
print(nx.ancestors(G, "x"))
for i in (G.predecessors("x")):
    print(i)

nx.draw(G, with_labels=True, node_color=["blue", "blue", "red", "red", "green"])
plt.show()