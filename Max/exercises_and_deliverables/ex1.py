# Build the graph from the paper exercise
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph([("a","b"), ("b","c"), ("c","a"), ("d", "d")])
#nx.draw(G, with_labels=True)
#plt.show()

print(G.degree())
G = G.subgraph(["a", "b", "c"])
print(nx.is_connected(G.subgraph(["a", "b", "c"])))
nx.draw(G, with_labels=True)
plt.show()