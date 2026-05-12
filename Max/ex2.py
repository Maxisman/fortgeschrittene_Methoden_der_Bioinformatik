import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph([(1,2), (1,3), (2,3), (3,4), (4,2)])
D.in_degree()

nx.draw(G, with_labels=True)
plt.show()